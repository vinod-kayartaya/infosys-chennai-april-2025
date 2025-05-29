# Horizontal Pod Autoscaler (HPA)

Autoscaling is one of Kubernetes' most powerful features — letting you adjust the number of pod replicas based on demand, automatically. **HPA** is a Kubernetes controller that automatically scales the number of pods in a **Deployment**, **ReplicaSet**, or **StatefulSet** based on observed metrics like:

- CPU utilization (default)
- Memory usage
- Custom metrics (via Prometheus Adapter)

This ensures your app has just the right number of pods — not too few to fail under load, and not too many to waste resources.

## Prerequisites

To follow along, you'll need:

- A working Kubernetes cluster (Minikube, KIND, EKS, GKE, etc.)
- `kubectl` configured
- The **metrics-server** installed and running

## How HPA Works

HPA operates through a control loop that:

1. **Queries metrics** from the Metrics Server or custom metrics APIs
2. **Calculates desired replica count** using the formula:
   ```
   desiredReplicas = ceil[currentReplicas * (currentMetricValue / desiredMetricValue)]
   ```
3. **Compares** with current replica count
4. **Scales** the target resource if needed
5. **Waits** for the cooldown period before next evaluation

### HPA Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   HPA Controller│────│  Metrics Server  │────│   Kubelet       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                                               │
         │                                               │
         ▼                                               ▼
┌─────────────────┐                              ┌─────────────────┐
│   Deployment    │                              │     Pods        │
└─────────────────┘                              └─────────────────┘
```

The diagram shows the key components involved in Kubernetes Horizontal Pod Autoscaling:

1. **HPA Controller**

   - The central component that manages autoscaling
   - Periodically checks metrics and makes scaling decisions
   - Communicates with the Metrics Server to get resource utilization data
   - Updates the Deployment when scaling is needed

2. **Metrics Server**

   - Collects resource metrics from Kubelets
   - Aggregates CPU and memory usage data
   - Exposes metrics via the Metrics API
   - Acts as the data source for HPA decisions

3. **Kubelet**

   - Runs on each node in the cluster
   - Collects resource usage statistics from containers
   - Reports metrics to the Metrics Server
   - Manages container lifecycle

4. **Deployment**

   - The workload being scaled by HPA
   - Contains the pod template and replica count
   - Gets updated by HPA to scale replicas up/down

5. **Pods**
   - The actual running containers
   - Resource usage is monitored by Kubelet
   - Number of replicas changes based on HPA decisions

The arrows show the flow of:

- Metrics data from Pods → Kubelet → Metrics Server → HPA Controller
- Scaling commands from HPA Controller → Deployment → Pods

This creates a complete feedback loop where resource usage drives automated scaling decisions.

## Installing the Metrics Server

The Metrics Server is a cluster-wide aggregator of resource usage data that:

- Collects CPU and memory usage metrics from all nodes and pods in your cluster
- Exposes these metrics through the Kubernetes Metrics API
- Enables core Kubernetes features like HPA and `kubectl top`
- Stores metrics in memory (not for long-term storage)
- Scrapes metrics every 15 seconds by default
- Is designed to be lightweight and scalable

Without the metrics-server, HPA won't have the data it needs to make scaling decisions.

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

If you're using **Minikube, KIND**, or a self-managed cluster, the metrics server may not work out of the box. You'll see errors like:

```
Error from server (ServiceUnavailable): the server is currently unable to handle the request (get nodes.metrics.k8s.io)
```

### Fix: Patch the Metrics Server

Use this command to patch the deployment:

```bash
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[
  {"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"},
  {"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname"}
]'
```

This enables metrics scraping even if TLS certificates are self-signed or the kubelet endpoint isn't using the default DNS name.

Verify it works:

```bash
kubectl top nodes
kubectl top pods
```

## Deploy a Sample Application

We'll use an NGINX deployment with CPU resource limits.

### `nginx-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          resources:
            limits:
              cpu: 200m
            requests:
              cpu: 100m
          ports:
            - containerPort: 80
```

Apply it:

```bash
kubectl apply -f nginx-deployment.yaml
```

## Create a Service

To access the NGINX pod from inside the cluster, create a ClusterIP service.

### `nginx-service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

Apply it:

```bash
kubectl apply -f nginx-service.yaml
```

## Create the HPA

Now let's configure the HPA to maintain CPU usage at 50%.

```bash
kubectl autoscale deployment nginx-deployment --cpu-percent=50 --min=1 --max=5
```

The command `kubectl autoscale deployment nginx-deployment --cpu-percent=50 --min=1 --max=5` creates a Horizontal Pod Autoscaler with the following arguments:

- `--cpu-percent=50`: Target CPU utilization percentage. HPA will try to maintain average CPU usage across all pods at 50%. If usage exceeds this, it scales up.

- `--min=1`: Minimum number of replicas. HPA will never scale below this number, even if CPU usage is very low.

- `--max=5`: Maximum number of replicas. HPA will never scale above this number, even if CPU usage is very high.

This is equivalent to creating an HPA manifest:

Check HPA status:

```bash
kubectl get hpa
kubectl describe hpa nginx-deployment
```

## Simulate Load

To trigger HPA scaling, we need to generate CPU load.

Launch a busybox pod:

```bash
kubectl run -i --tty load-generator --image=busybox /bin/sh
```

Then run:

```sh
while true; do wget -q -O- http://nginx-service; done
```

Leave it running for a few minutes, then in another terminal:

```bash
kubectl get hpa -w
```

You should see `REPLICAS` increase as the average CPU exceeds 50%.

## Observe Automatic Scale-Down

When you stop the load generator (`Ctrl+C`), the CPU usage drops. HPA doesn't immediately scale down — by default, it waits for a cooldown period (~5 minutes), then reduces the number of replicas.

HPA will never scale **below `minReplicas`**.

```bash
kubectl get hpa -w
```

Eventually, replicas should return to 1 (or your configured min).

## How Scaling Decisions Are Made

### HPA Formula:

```
desiredReplicas = ceil[currentReplicas * (currentUtilization / targetUtilization)]
```

Example:

- Current replicas = 2
- Current CPU = 80%
- Target CPU = 50%

```
desiredReplicas = ceil[2 * (80 / 50)] = ceil[3.2] = 4
```

## Advanced HPA: YAML with autoscaling/v2

HPA v2 lets you define multiple metrics (CPU, memory, or custom):

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

Apply it:

```bash
kubectl apply -f nginx-hpa.yaml
```

## Cleanup

```bash
kubectl delete deployment nginx-deployment
kubectl delete service nginx-service
kubectl delete hpa nginx-deployment
kubectl delete pod load-generator
```

## Final Tips & Best Practices

- Always define CPU/memory **requests and limits** on your containers.
- Use **HPA + Cluster Autoscaler** for true elasticity (scale pods and nodes).
- Use **Prometheus Adapter** for scaling on custom application metrics.
- Monitor scaling activity with tools like **Grafana**, `kubectl top`, or `kubectl describe hpa`.

## Further Reading

- [Kubernetes HPA Official Docs](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Metrics Server GitHub](https://github.com/kubernetes-sigs/metrics-server)
- [Prometheus Adapter for Custom Metrics](https://github.com/kubernetes-sigs/prometheus-adapter)

### Conclusion

HPA is essential for building scalable, cost-effective applications on Kubernetes. With this hands-on demo, you now understand not just the theory, but how to **implement and test HPA in your own clusters.**

Have questions or want the full setup as a script or GitHub repo? Drop a comment!
