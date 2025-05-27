# Events, Hooks, Resource Handling, Health Checks & Operators

In this tutorial, we'll explore essential Kubernetes concepts using a practical Spring Boot application deployment. We'll work through each concept step by step, using commands and examples you can try yourself.

## Prerequisites

Before we start, make sure you have:

- A running Kubernetes cluster (minikube, kind, or cloud cluster)
- kubectl configured to connect to your cluster

Let's verify your setup:

```bash
kubectl cluster-info
kubectl get nodes
```

## Our Example Application

We'll use this deployment configuration throughout the tutorial:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nw-categories-dep
  labels:
    app: nw-categories-dep
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nw-categories-pod
  template:
    metadata:
      labels:
        app: nw-categories-pod
    spec:
      containers:
        - name: contact-container
          image: learnwithvinod/nw-categories
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: '250m'
              memory: '256Mi'
            limits:
              cpu: '500m'
              memory: '512Mi'
          lifecycle:
            postStart:
              exec:
                command: ['/bin/sh', '-c', "echo 'PostStart hook triggered'"]
            preStop:
              exec:
                command: ['/bin/sh', '-c', "echo 'PreStop hook triggered'"]
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 15
            timeoutSeconds: 5
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            timeoutSeconds: 5
          startupProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            failureThreshold: 30
            periodSeconds: 10
```

Save this as `deployment.yaml` and let's get started!

## 1. Resource Handling

Resource handling ensures your applications get the computing resources they need while preventing them from consuming too much.

### Understanding Resource Requests and Limits

In our YAML, look at the `resources` section:

```yaml
resources:
  requests:
    cpu: '250m' # 250 millicores (0.25 CPU cores)
    memory: '256Mi' # 256 Mebibytes of RAM
  limits:
    cpu: '500m' # Maximum 500 millicores
    memory: '512Mi' # Maximum 512 Mebibytes
```

- **Requests**: Kubernetes guarantees these minimum resources
- **Limits**: Maximum resources the container can use

### Deploy and Test Resource Handling

1. **Deploy the application:**

```bash
kubectl apply -f deployment.yaml
```

2. **Check resource allocation:**

```bash
kubectl describe pod -l app=nw-categories-pod
```

Look for the "Requests" and "Limits" sections in the output.

3. **Monitor resource usage:**

```bash
kubectl top pod -l app=nw-categories-pod
```

4. **View resource quotas (if any):**

```bash
kubectl describe resourcequota
```

### Experiment: What happens without resource limits?

Create a version without limits and compare:

```bash
# Remove the limits section from your YAML and redeploy
kubectl apply -f deployment-no-limits.yaml
kubectl describe pod -l app=nw-categories-pod
```

## 2. Lifecycle Hooks

Hooks let you run custom code at specific points in a container's lifecycle.

### Understanding the Hooks in Our Example

```yaml
lifecycle:
  postStart:
    exec:
      command: ['/bin/sh', '-c', "echo 'PostStart hook triggered'"]
  preStop:
    exec:
      command: ['/bin/sh', '-c', "echo 'PreStop hook triggered'"]
```

### See Hooks in Action

1. **Deploy the application:**

```bash
kubectl apply -f deployment.yaml
```

2. **Check the postStart hook output:**

```bash
kubectl logs -l app=nw-categories-pod
```

3. **Trigger the preStop hook by deleting the pod:**

```bash
# Get the pod name
kubectl get pods -l app=nw-categories-pod

# Delete the pod to trigger preStop hook
kubectl delete pod <pod-name>

# Check logs before the pod is fully terminated
kubectl logs <pod-name>
```

### Practical Use Cases for PostStart Hook

The **postStart** hook runs immediately after a container is created. Here are common real-world scenarios:

**Why use PostStart hooks?** These hooks are perfect for tasks that need to happen right after container creation but before your application starts serving traffic. Think of it as your container's initialization phase.

#### 1. Configuration File Setup

**Use Case**: Your application needs configuration files that are generated from templates or environment-specific settings.

**Real-world scenario**: A microservice that needs different database connection strings for dev, staging, and production environments.

```yaml
postStart:
  exec:
    command:
      [
        '/bin/sh',
        '-c',
        'cp /config-template/* /app/config/ && chmod 600 /app/config/*',
      ]
```

#### 2. Database Migration/Schema Setup

**Use Case**: Ensure your database schema is up-to-date before your application starts processing requests.

**Real-world scenario**: A Spring Boot application that needs to run Flyway migrations on startup.

```yaml
postStart:
  exec:
    command: ['/bin/sh', '-c', 'java -jar /app/migration.jar --migrate']
```

#### 3. Service Registration

**Use Case**: Register your service instance with a service discovery system like Consul or Eureka.

**Real-world scenario**: A microservice in a distributed system that needs to announce its availability to other services.

```yaml
postStart:
  exec:
    command:
      [
        '/bin/sh',
        '-c',
        'curl -X POST http://service-registry:8080/register -d ''{"service":"nw-categories-dep","host":"${HOSTNAME}"}''',
      ]
```

#### 4. Cache Warming

**Use Case**: Pre-populate caches with frequently accessed data to improve initial response times.

**Real-world scenario**: An e-commerce API that loads popular product data into Redis cache on startup.

```yaml
postStart:
  exec:
    command: ['/bin/sh', '-c', 'wget -q http://localhost:8080/admin/cache/warm']
```

#### 5. Log Directory Preparation

**Use Case**: Set up logging directories with proper permissions before your application starts writing logs.

**Real-world scenario**: A web server that needs specific log directories with correct ownership for security compliance.

```yaml
postStart:
  exec:
    command:
      ['/bin/sh', '-c', 'mkdir -p /var/log/app && chown app:app /var/log/app']
```

Let's test the configuration setup example:

```bash
# Create a ConfigMap with template files
kubectl create configmap app-config-template --from-literal=app.properties="server.port=8080"

# Update your deployment to mount the ConfigMap and use the postStart hook
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nw-categories-dep-with-config
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nw-categories-pod-with-config
  template:
    metadata:
      labels:
        app: nw-categories-pod-with-config
    spec:
      containers:
      - name: contact-container
        image: learnwithvinod/nw-categories
        volumeMounts:
        - name: config-template
          mountPath: /config-template
        - name: app-config
          mountPath: /app/config
        lifecycle:
          postStart:
            exec:
              command: ["/bin/sh", "-c", "cp /config-template/* /app/config/ && ls -la /app/config/"]
      volumes:
      - name: config-template
        configMap:
          name: app-config-template
      - name: app-config
        emptyDir: {}
EOF

# Check if the postStart hook worked
kubectl exec deployment/nw-categories-pod-with-config -- ls -la /app/config/
```

### Practical Use Cases for PreStop Hook

The **preStop** hook runs before a container is terminated, giving you time for graceful shutdown.

**Why use PreStop hooks?** These hooks ensure your application shuts down cleanly, prevents data loss, and maintains service availability during deployments or scaling operations.

#### 1. Graceful Application Shutdown

**Use Case**: Allow your application to finish processing current requests before shutting down.

**Real-world scenario**: A REST API server that needs to complete in-flight HTTP requests to avoid returning 500 errors to clients.

```yaml
preStop:
  exec:
    command: ['/bin/sh', '-c', 'kill -TERM $(pgrep java) && sleep 30']
```

#### 2. Service Deregistration

**Use Case**: Remove your service instance from load balancers and service discovery systems.

**Real-world scenario**: Ensuring a microservice is removed from Consul or AWS ELB before shutdown to prevent traffic routing to a dead instance.

```yaml
preStop:
  exec:
    command:
      [
        '/bin/sh',
        '-c',
        'curl -X DELETE http://service-registry:8080/deregister/${HOSTNAME}',
      ]
```

#### 3. Connection Draining

**Use Case**: Stop accepting new connections while allowing existing connections to complete naturally.

**Real-world scenario**: A web server during a rolling update that needs to drain existing user sessions without dropping them.

```yaml
preStop:
  exec:
    command:
      [
        '/bin/sh',
        '-c',
        'curl -X POST http://localhost:8080/admin/drain && sleep 15',
      ]
```

#### 4. Data Backup Before Shutdown

**Use Case**: Create a backup of critical data before the container is destroyed.

**Real-world scenario**: A database container or data processing service that needs to backup its state before termination.

```yaml
preStop:
  exec:
    command:
      [
        '/bin/sh',
        '-c',
        'pg_dump mydb > /backup/$(date +%Y%m%d_%H%M%S)_backup.sql',
      ]
```

#### 5. Cache Flush

**Use Case**: Persist in-memory cache data to disk before shutdown.

**Real-world scenario**: A Redis instance that needs to save its dataset to disk to prevent data loss during container restart.

```yaml
preStop:
  exec:
    command: ['/bin/sh', '-c', 'redis-cli BGSAVE && sleep 5']
```

#### 6. Log Rotation and Upload

**Use Case**: Archive and upload logs to external storage before container termination.

**Real-world scenario**: A logging service that needs to upload log files to S3 or another storage system before the container is destroyed.

```yaml
preStop:
  exec:
    command:
      [
        '/bin/sh',
        '-c',
        'logrotate /etc/logrotate.conf && aws s3 cp /var/log/ s3://my-logs/ --recursive',
      ]
```

Let's test the graceful shutdown example:

```bash
# Deploy with graceful shutdown hook
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: graceful-shutdown-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: graceful-shutdown-demo
  template:
    metadata:
      labels:
        app: graceful-shutdown-demo
    spec:
      containers:
      - name: app
        image: nginx
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "echo 'Starting graceful shutdown...' && nginx -s quit && sleep 10 && echo 'Graceful shutdown completed'"]
        terminationGracePeriodSeconds: 60
EOF

# Watch the pod
kubectl get pods -l app=graceful-shutdown-demo -w

# In another terminal, delete the pod and check logs
kubectl delete pod -l app=graceful-shutdown-demo
kubectl logs -l app=graceful-shutdown-demo --previous
```

### Real-World Example: Web Application with Database

Here's a comprehensive example combining both hooks for a web application:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-with-hooks
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webapp-with-hooks
  template:
    metadata:
      labels:
        app: webapp-with-hooks
    spec:
      containers:
      - name: webapp
        image: nginx
        lifecycle:
          postStart:
            exec:
              command: ["/bin/sh", "-c", |
                echo "Initializing application..." &&
                mkdir -p /var/log/app &&
                curl -X POST http://loadbalancer/register -d "{\"instance\":\"$HOSTNAME\",\"port\":80}" &&
                echo "Application initialized successfully"
              ]
          preStop:
            exec:
              command: ["/bin/sh", "-c", |
                echo "Starting graceful shutdown..." &&
                curl -X DELETE http://loadbalancer/deregister/$HOSTNAME &&
                sleep 20 &&
                echo "Graceful shutdown completed"
              ]
        terminationGracePeriodSeconds: 45
```

### Testing Hook Timing

To understand when hooks execute, try this experiment:

```bash
# Create a deployment with logging hooks
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hook-timing-test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hook-timing-test
  template:
    metadata:
      labels:
        app: hook-timing-test
    spec:
      containers:
      - name: test-container
        image: busybox
        command: ["/bin/sh"]
        args: ["-c", "echo 'Container started' && sleep 3600"]
        lifecycle:
          postStart:
            exec:
              command: ["/bin/sh", "-c", "echo 'PostStart hook executed at' $(date) > /tmp/poststart.log"]
          preStop:
            exec:
              command: ["/bin/sh", "-c", "echo 'PreStop hook executed at' $(date) > /tmp/prestop.log && sleep 5"]
EOF

# Check the postStart log
kubectl exec deployment/hook-timing-test -- cat /tmp/poststart.log

# Delete the pod to trigger preStop
kubectl delete pod -l app=hook-timing-test

# Quickly check the preStop log before pod terminates
kubectl exec deployment/hook-timing-test -- cat /tmp/prestop.log
```

### Important Hook Considerations

**PostStart Hook Tips:**

- Doesn't guarantee execution before the main container process starts
- If it fails, the container is killed
- Should complete quickly to avoid blocking pod startup
- Use for non-critical initialization tasks

**PreStop Hook Tips:**

- Has a limited time window (terminationGracePeriodSeconds)
- Should complete before the grace period expires
- Perfect for cleanup tasks and graceful shutdowns
- Always include appropriate sleep/wait times

## 3. Health Checks (Probes)

Health checks ensure your application is running correctly and ready to serve traffic.

### Understanding the Three Types of Probes

Our example uses all three probe types:

#### Startup Probe

```yaml
startupProbe:
  httpGet:
    path: /actuator/health
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

- **Purpose**: Protects slow-starting containers
- **Behavior**: Disables other probes until this succeeds
- **Our example**: 30 attempts × 10 seconds = 5 minutes maximum startup time

#### Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 15
  timeoutSeconds: 5
```

- **Purpose**: Detects if container is running properly
- **Behavior**: Restarts container if it fails
- **Our example**: Checks every 15 seconds after 10-second delay

#### Readiness Probe

```yaml
readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 5
```

- **Purpose**: Determines if container can accept traffic
- **Behavior**: Removes pod from service endpoints if it fails

### Test the Probes

1. **Deploy and watch the startup process:**

```bash
kubectl apply -f deployment.yaml
kubectl get pods -l app=nw-categories-pod -w
```

2. **Check probe status:**

```bash
kubectl describe pod -l app=nw-categories-pod
```

Look for the "Conditions" section to see Ready, PodScheduled, etc.

3. **Test the health endpoints directly:**

```bash
# Port forward to access the health endpoints
kubectl port-forward deployment/nw-categories-dep 8080:8080

# In another terminal, test the endpoints
curl http://localhost:8080/actuator/health
curl http://localhost:8080/actuator/health/liveness
curl http://localhost:8080/actuator/health/readiness
```

4. **Simulate a failing probe:**

```bash
# Exec into the pod and break the health endpoint
kubectl exec -it deployment/nw-categories -- /bin/sh

# Inside the pod, you could modify files or stop processes
# to make health checks fail (be careful in production!)
```

### Monitor Probe Failures

```bash
# Watch for probe-related events
kubectl get events --watch

# Check probe failure details
kubectl describe pod -l app=nw-categories-pod | grep -A 10 "Conditions"
```

## 4. Events

Events are Kubernetes' way of telling you what's happening in your cluster.

### Viewing Events

1. **See all recent events:**

```bash
kubectl get events
```

2. **Filter events for our application:**

```bash
kubectl get events --field-selector involvedObject.name=nw-categories-dep
```

3. **Watch events in real-time:**

```bash
kubectl get events --watch
```

4. **Get detailed event information:**

```bash
kubectl describe events
```

### Trigger Some Events

Let's create some events to observe:

```bash
# Scale the deployment (creates events)
kubectl scale deployment nw-categories-dep --replicas=3

# Update the image (creates events)
kubectl set image deployment/nw-categories-dep nw-categories-container=learnwithvinod/nw-categproes:latest

# Rollback (creates events)
kubectl rollout undo deployment/nw-categories-dep

# Check events after each command
kubectl get events --sort-by='.lastTimestamp'
```

### Understanding Event Types

Events you'll commonly see:

- **Scheduled**: Pod assigned to a node
- **Pulling**: Downloading container image
- **Pulled**: Image download complete
- **Created**: Container created
- **Started**: Container started
- **Killing**: Container being terminated
- **Unhealthy**: Probe failures

## 6. Putting It All Together

Let's create a comprehensive example that demonstrates all concepts:

### Step 1: Deploy with Monitoring

```bash
# Apply our deployment
kubectl apply -f deployment.yaml

# Create a service to expose it
kubectl expose deployment nw-categories-dep --port=80 --target-port=8080
```

### Step 2: Monitor Everything

```bash
# Watch pods and their status
kubectl get pods -l app=nw-categories-pod -w

# In another terminal, watch events
kubectl get events --watch

# In a third terminal, check resources
watch kubectl top pods -l app=nw-categories-pod
```

### Step 3: Test Failure Scenarios

```bash
# Simulate high CPU usage
kubectl exec -it deployment/nw-categories-dep -- stress --cpu 2 --timeout 60s

# Watch how Kubernetes responds to resource limits
# and probe failures
```

### Step 4: Cleanup

```bash
kubectl delete deployment nw-categories-dep
kubectl delete service nw-categories-service
```

## Key Takeaways

1. **Resource Management**: Always set requests and limits to ensure predictable performance
2. **Lifecycle Hooks**: Use for initialization and graceful shutdown procedures
3. **Health Checks**: Implement all three probes for robust application lifecycle management
4. **Events**: Monitor events to understand what's happening in your cluster

# Services and Networking in Kubernetes with Practical Example

When deploying applications in Kubernetes, understanding how **services and networking** work is essential to ensure your applications are discoverable and accessible. This article walks you through a real-world example using a Spring Boot app, demonstrating how to expose it within and outside the cluster.

## Kubernetes Deployment and Service Definition

Let's start by defining our application deployment and its service.

### `deployment.yaml`

We deploy a simple Spring Boot app using the image `learnwithvinod/springboot-sqlite-contact-service`. The app listens on port `8080`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: contact-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: p3
  template:
    metadata:
      name: p3
      labels:
        app: p3
    spec:
      containers:
        - name: c3
          image: learnwithvinod/springboot-sqlite-contact-service
          ports:
            - containerPort: 8080
```

### `service.yaml`

To make this app accessible within and outside the cluster, we define a `NodePort` service.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: contact-service-service
spec:
  selector:
    app: p3
  ports:
    - protocol: TCP
      port: 1234 # Service port (internal to cluster)
      targetPort: 8080 # Pod's port (container)
      nodePort: 30000 # Node port (external access)
  type: NodePort
```

## Understanding the Ports

Kubernetes `Service` uses **three different port numbers**:

| Field        | Meaning                                                                              |
| ------------ | ------------------------------------------------------------------------------------ |
| `port`       | Port exposed by the service **inside the cluster** (e.g., `1234`)                    |
| `targetPort` | The actual **port on the container (Pod)** where the app is listening (e.g., `8080`) |
| `nodePort`   | A port on the **node's IP address** exposed externally (e.g., `30000`)               |

These ports enable Kubernetes to route traffic:

```text
User → NodePort (30000) → Service Port (1234) → Pod Port (8080)
```

## Verifying the Deployment

Check the service:

```bash
kubectl get services
```

Example output:

```
NAME                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
contact-service-service   NodePort    10.105.41.125   <none>        1234:30000/TCP   5m
```

Check the nodes:

```bash
kubectl get nodes -o wide
```

Example output:

```
NAME             STATUS   ROLES           AGE     INTERNAL-IP     OS-IMAGE
vincluster       Ready    control-plane   3h55m   192.168.58.2    Ubuntu 22.04
```

## Accessing the Service

To access the API from outside the cluster, use the **node IP** and the **NodePort**.

```bash
curl http://192.168.58.2:30000/api/contacts
```

Alternatively, open it in a browser:

```
http://192.168.58.2:30000/api/contacts
```

## Types of Kubernetes Services

Kubernetes offers different types of services depending on how you want your application to be accessed:

### 1. `ClusterIP` (Default)

- **Scope**: Internal to the cluster.
- **Use case**: App-to-app communication within the cluster (e.g., frontend → backend).
- **External Access**: Not directly accessible from outside.
- **Example**:

  ```yaml
  type: ClusterIP
  ```

### 2. `NodePort`

- **Scope**: Exposes the service on a static port (range `30000–32767`) on each node's IP.
- **Use case**: Simple external access in dev/test environments.
- **External Access**: Yes, via `NodeIP:NodePort`.
- **Example**:

  ```yaml
  type: NodePort
  ```

### 3. `LoadBalancer`

- **Scope**: Provisions an external load balancer via cloud provider (e.g., AWS ELB).
- **Use case**: Production-grade public access.
- **External Access**: Yes, with a public IP or DNS.
- **Example**:

  ```yaml
  type: LoadBalancer
  ```

  > Works only in cloud environments or with load-balancer-capable clusters.

### 4. `ExternalName`

- **Scope**: Maps service to an external DNS name.
- **Use case**: Connect to an external service as if it were internal.
- **External Access**: DNS redirect only.
- **Example**:

  ```yaml
  type: ExternalName
  externalName: api.external.com
  ```

## Summary

| Service Type | Access From      | Use Case                            |
| ------------ | ---------------- | ----------------------------------- |
| ClusterIP    | Inside cluster   | Internal microservice communication |
| NodePort     | Outside via Node | Quick and simple external access    |
| LoadBalancer | Public IP        | Cloud-based production exposure     |
| ExternalName | DNS Resolution   | Redirect to external services       |
