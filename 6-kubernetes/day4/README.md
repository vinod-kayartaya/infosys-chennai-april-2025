# Kubernetes Namespaces

Namespaces are a powerful feature in Kubernetes that help you logically divide your cluster resources and organize workloads efficiently. Whether you're managing development, staging, or production environments—or building a multi-tenant architecture—namespaces are essential.

In this guide, we'll walk through everything you need to know about Kubernetes Namespaces, including how to create them, manage them, and view objects within them.

## **What Are Kubernetes Namespaces?**

A **namespace** in Kubernetes is like a virtual cluster inside your actual cluster. It provides scope for names, helping you isolate and organize resources for different teams, applications, or environments.

### **Key Benefits of Namespaces**

- **Environment separation:** Ideal for `dev`, `test`, `prod`.
- **Multi-tenancy:** Enables different teams to share the same cluster.
- **Resource management:** Apply quotas to control resource usage.
- **Security:** Use Role-Based Access Control (RBAC) to restrict access.

## **Default Namespaces in Kubernetes**

Kubernetes includes several built-in namespaces:

| Namespace         | Description                                        |
| ----------------- | -------------------------------------------------- |
| `default`         | Default for resources with no specified namespace. |
| `kube-system`     | Hosts Kubernetes system components.                |
| `kube-public`     | Readable by all users; used for bootstrapping.     |
| `kube-node-lease` | Used for node heartbeats.                          |

## **Creating a Namespace**

You can define a namespace using YAML:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev-environment
```

Apply it with:

```bash
kubectl apply -f namespace.yaml
```

Or create directly using `kubectl`:

```bash
kubectl create namespace dev-environment
```

Verify it:

```bash
kubectl get namespaces
```

## **Creating Resources Within a Namespace**

You can deploy resources to a specific namespace in two ways:

### **1. Include the namespace in the YAML**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
  namespace: dev-environment
spec:
  containers:
    - name: nginx
      image: nginx
```

### **2. Use the `--namespace` flag**

```bash
kubectl run nginx --image=nginx --namespace=dev-environment
```

## **Setting the Default Namespace for a Context**

Avoid repeating the `--namespace` flag by setting a default namespace for your current context:

```bash
kubectl config set-context --current --namespace=dev-environment
```

## **Viewing Objects in a Namespace**

Here’s how to inspect resources in a specific namespace:

### **1. View all resources**

```bash
kubectl get all -n dev-environment
```

### **2. View specific resources**

- **Pods:** `kubectl get pods -n dev-environment`
- **Services:** `kubectl get svc -n dev-environment`
- **Deployments:** `kubectl get deployments -n dev-environment`
- **ReplicaSets:** `kubectl get rs -n dev-environment`
- **ConfigMaps:** `kubectl get configmaps -n dev-environment`
- **Secrets:** `kubectl get secrets -n dev-environment`

### **3. Describe a resource**

```bash
kubectl describe pod mypod -n dev-environment
```

### **4. View events**

```bash
kubectl get events -n dev-environment
```

## **Using Resource Quotas and Limits**

Namespaces work hand-in-hand with quotas to control resource usage.

### **Example ResourceQuota**

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: dev-environment
spec:
  hard:
    pods: '10'
    requests.cpu: '4'
    requests.memory: 8Gi
    limits.cpu: '10'
    limits.memory: 16Gi
```

Apply with:

```bash
kubectl apply -f quota.yaml
```

## **Securing Namespaces with RBAC**

RBAC roles and role bindings can limit access to specific namespaces.

### **Example Role**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: dev-environment
  name: pod-reader
rules:
  - apiGroups: ['']
    resources: ['pods']
    verbs: ['get', 'watch', 'list']
```

### **Example RoleBinding**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: dev-environment
subjects:
  - kind: User
    name: vinod
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

## **Best Practices for Using Namespaces**

- Use namespaces to logically separate different environments or teams.
- Apply resource quotas to control usage.
- Restrict access using RBAC.
- Don’t overuse namespaces—stick to what’s needed.
- Monitor resource usage per namespace using tools like **Prometheus** and **Grafana**.

## **Conclusion**

Namespaces are essential for organizing, securing, and managing Kubernetes clusters—especially as they scale. Whether you're a beginner setting up your first cluster or an admin managing multi-team environments, understanding and using namespaces effectively will keep your deployments clean, efficient, and secure.

# Helm Tutorial: Deploying Microservices Using Helm Charts

## Overview

This tutorial shows how to use **Helm** to deploy a set of microservices in Kubernetes. We'll use the following Docker images:

1. `learnwithvinod/nw-categories`
2. `learnwithvinod/nw-suppliers`
3. `learnwithvinod/nw-products`

The `nw-products` service depends on the other two and requires environment variables to be set accordingly. We'll also expose this service using **NodePort 30000**.

## Project Structure

```bash
microservices-helm/
├── Chart.yaml
├── values.yaml
└── charts/
    ├── categories/
    ├── suppliers/
    └── products/
```

## == Step 1: Create Helm Project ==

```bash
helm create microservices-helm
cd microservices-helm
rm -rf templates/*
```

Create subcharts:

```bash
helm create charts/categories
helm create charts/suppliers
helm create charts/products
```

## == Step 2: Configure `categories` Chart ==

### `charts/categories/values.yaml`

```yaml
image:
  repository: learnwithvinod/nw-categories
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080
```

### `charts/categories/templates/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: '{{ .Chart.Name }}'
  labels:
    app: '{{ .Chart.Name }}'
spec:
  replicas: 1
  selector:
    matchLabels:
      app: '{{ .Chart.Name }}'
  template:
    metadata:
      labels:
        app: '{{ .Chart.Name }}'
    spec:
      containers:
        - name: '{{ .Chart.Name }}'
          image: '{{ .Values.image.repository }}:{{ .Values.image.tag }}'
          imagePullPolicy: '{{ .Values.image.pullPolicy }}'
          ports:
            - containerPort: '{{ .Values.service.port }}'
```

### `charts/categories/templates/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: '{{ .Chart.Name }}'
spec:
  type: '{{ .Values.service.type }}'
  selector:
    app: '{{ .Chart.Name }}'
  ports:
    - port: '{{ .Values.service.port }}'
      targetPort: '{{ .Values.service.port }}'
```

## == Step 3: Configure `suppliers` Chart ==

### `charts/suppliers/values.yaml`

```yaml
image:
  repository: learnwithvinod/nw-suppliers
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080
```

### `charts/suppliers/templates/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: '{{ .Chart.Name }}'
  labels:
    app: '{{ .Chart.Name }}'
spec:
  replicas: 1
  selector:
    matchLabels:
      app: '{{ .Chart.Name }}'
  template:
    metadata:
      labels:
        app: '{{ .Chart.Name }}'
    spec:
      containers:
        - name: '{{ .Chart.Name }}'
          image: '{{ .Values.image.repository }}:{{ .Values.image.tag }}'
          imagePullPolicy: '{{ .Values.image.pullPolicy }}'
          ports:
            - containerPort: '{{ .Values.service.port }}'
```

### `charts/suppliers/templates/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: '{{ .Chart.Name }}'
spec:
  type: '{{ .Values.service.type }}'
  selector:
    app: '{{ .Chart.Name }}'
  ports:
    - port: '{{ .Values.service.port }}'
      targetPort: '{{ .Values.service.port }}'
```

## == Step 4: Configure `products` Chart ==

### `charts/products/values.yaml`

```yaml
image:
  repository: learnwithvinod/nw-products
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: NodePort
  port: 8080
  nodePort: 30000

env:
  CATEGORY_SERVICE_HOST: categories
  CATEGORY_SERVICE_PORT: '8080'
  SUPPLIER_SERVICE_HOST: suppliers
  SUPPLIER_SERVICE_PORT: '8080'
```

### `charts/products/templates/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: '{{ .Chart.Name }}'
  labels:
    app: '{{ .Chart.Name }}'
spec:
  replicas: 1
  selector:
    matchLabels:
      app: '{{ .Chart.Name }}'
  template:
    metadata:
      labels:
        app: '{{ .Chart.Name }}'
    spec:
      containers:
        - name: '{{ .Chart.Name }}'
          image: '{{ .Values.image.repository }}:{{ .Values.image.tag }}'
          imagePullPolicy: '{{ .Values.image.pullPolicy }}'
          ports:
            - containerPort: '{{ .Values.service.port }}'
          env:
            - name: CATEGORY_SERVICE_HOST
              value: '{{ .Values.env.CATEGORY_SERVICE_HOST }}'
            - name: CATEGORY_SERVICE_PORT
              value: '{{ .Values.env.CATEGORY_SERVICE_PORT }}'
            - name: SUPPLIER_SERVICE_HOST
              value: '{{ .Values.env.SUPPLIER_SERVICE_HOST }}'
            - name: SUPPLIER_SERVICE_PORT
              value: '{{ .Values.env.SUPPLIER_SERVICE_PORT }}'
```

### `charts/products/templates/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Chart.Name }}
spec:
  type: {{ .Values.service.type }}
  selector:
    app: {{ .Chart.Name }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.port }}
      {{- if eq .Values.service.type "NodePort" }}
      nodePort: {{ .Values.service.nodePort }}
      {{- end }}
```

## == Step 5: Configure Root Helm Chart ==

### `Chart.yaml`

```yaml
apiVersion: v2
name: microservices-helm
version: 0.1.0
dependencies:
  - name: categories
    version: 0.1.0
    repository: file://charts/categories
  - name: suppliers
    version: 0.1.0
    repository: file://charts/suppliers
  - name: products
    version: 0.1.0
    repository: file://charts/products
```

### Update dependencies

```bash
helm dependency update
```

## == Step 6: Deploy Using Helm ==

### Create Namespace

```bash
kubectl create namespace vinod-ms
```

### Install Helm Chart

```bash
helm install microservices-release . -n vinod-ms
```

## == Step 7: Validate Deployment ==

```bash
kubectl get all -n vinod-ms
```

Check NodePort exposure:

```bash
kubectl get svc -n vinod-ms
```

Expected output:

```
NAME        TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
products    NodePort   10.x.x.x       <none>        3002:30000/TCP   1m
```

Access the product service:

```
curl http://<NODE_IP>:30000
```

Replace `<NODE_IP>` with any Kubernetes node IP.

## == Step 8: Cleanup ==

```bash
helm uninstall microservices-release -n vinod-ms
kubectl delete namespace vinod-ms
```

## Summary

You've learned how to:

- Create and organize Helm charts for multiple services
- Configure inter-service communication using environment variables
- Expose one service using a static NodePort (30000)
- Deploy the full stack using a single Helm command
