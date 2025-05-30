# Kubernetes RBAC (Role-Based Access Control)

## Table of Contents

1. [Introduction to RBAC](#introduction-to-rbac)
2. [RBAC Components](#rbac-components)
3. [Setting Up RBAC](#setting-up-rbac)
4. [Practical Examples](#practical-examples)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Introduction to RBAC

Role-Based Access Control (RBAC) is a security mechanism in Kubernetes that regulates access to cluster resources based on the roles assigned to users, service accounts, or groups. RBAC allows you to define fine-grained permissions and implement the principle of least privilege.

### Why Use RBAC?

- **Security**: Limit access to only necessary resources
- **Compliance**: Meet organizational security requirements
- **Multi-tenancy**: Safely share clusters between teams
- **Audit**: Track who can perform what actions

## RBAC Components

RBAC in Kubernetes consists of four main components:

### 1. Subjects

Who is requesting access:

- **Users**: Human users (managed externally)
- **Groups**: Collections of users
- **Service Accounts**: Pod identities within the cluster

### 2. Resources

What can be accessed:

- Kubernetes objects (pods, services, deployments, etc.)
- API endpoints
- Non-resource URLs

### 3. Verbs

What actions can be performed:

- `get`, `list`, `watch`
- `create`, `update`, `patch`, `delete`
- `deletecollection`
- Custom verbs for specific resources

### 4. RBAC Objects

#### Role and ClusterRole

Define permissions (what can be done):

```yaml
# Role - namespace-scoped
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
  - apiGroups: ['']
    resources: ['pods']
    verbs: ['get', 'watch', 'list']

# ClusterRole - cluster-scoped
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
  - apiGroups: ['']
    resources: ['secrets']
    verbs: ['get', 'list']
```

The empty string `""` in `apiGroups` has a specific and important meaning in Kubernetes RBAC. Read more here [Api Groups](./api-groups.md)

#### RoleBinding and ClusterRoleBinding

Bind roles to subjects (who can do it):

```yaml
# RoleBinding - binds Role to subjects in a namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
  - kind: User
    name: jane
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io

# ClusterRoleBinding - binds ClusterRole to subjects cluster-wide
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-secrets-global
subjects:
  - kind: User
    name: dave
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

# Kubernetes RBAC Tutorial: Create and Manage Multiple Users with Namespaced Roles

Role-Based Access Control (RBAC) in Kubernetes is an essential mechanism to restrict or allow user access based on defined roles. In this comprehensive tutorial, we will demonstrate how to:

- Create two distinct users (`vinod` and `shyam`)
- Assign different roles to each
- Allow them access to specific Kubernetes resources within different namespaces

## Prerequisites

Ensure you have the following ready:

- A running Kubernetes cluster (e.g., Minikube)
- Access to the Kubernetes control plane (for CA files)
- `kubectl` and `openssl` installed

![RBAC](./rbac.png)

## Step 1: Create Users and Certificates

We'll create TLS certificates for both `vinod` and `shyam`.

### 1.1 Generate Keys and CSRs

```bash
# For vinod
openssl genrsa -out vinod.key 2048
openssl req -new -key vinod.key -out vinod.csr -subj "/CN=vinod/O=team-a"

# For shyam
openssl genrsa -out shyam.key 2048
openssl req -new -key shyam.key -out shyam.csr -subj "/CN=shyam/O=team-b"
```

### 1.2 Sign the Certificates with Kubernetes CA

```bash
# Copy these from your Minikube control plane
minikube ssh -- sudo cat /var/lib/minikube/certs/ca.crt > ca.crt
minikube ssh -- sudo cat /var/lib/minikube/certs/ca.key > ca.key

openssl x509 -req -in vinod.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
-out vinod.crt -days 365

openssl x509 -req -in shyam.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
-out shyam.crt -days 365
```

## Step 2: Create Kubeconfig Files

Create separate kubeconfig files for each user.

```yaml
# vinod.kubeconfig.yaml
apiVersion: v1
kind: Config
clusters:
  - name: minikube
    cluster:
      server: https://127.0.0.1:8443
      certificate-authority: ./ca.crt
users:
  - name: vinod
    user:
      client-certificate: ./vinod.crt
      client-key: ./vinod.key
contexts:
  - name: vinod-context
    context:
      cluster: minikube
      user: vinod
      namespace: dev
current-context: vinod-context
```

```yaml
# shyam.kubeconfig.yaml
apiVersion: v1
kind: Config
clusters:
  - name: minikube
    cluster:
      server: https://127.0.0.1:8443
      certificate-authority: ./ca.crt
users:
  - name: shyam
    user:
      client-certificate: ./shyam.crt
      client-key: ./shyam.key
contexts:
  - name: shyam-context
    context:
      cluster: minikube
      user: shyam
      namespace: prod
current-context: shyam-context
```

## Step 3: Define Namespaces

```bash
kubectl create namespace dev
kubectl create namespace prod
```

## Step 4: Define Roles and Bindings

### 4.1 Role for `vinod` (Pod Reader in `dev` namespace)

```yaml
# dev-pod-reader-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: dev
  name: dev-pod-reader
rules:
  - apiGroups: ['']
    resources: ['pods']
    verbs: ['get', 'list', 'watch']
```

```yaml
# dev-pod-reader-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: vinod-pod-reader-binding
  namespace: dev
subjects:
  - kind: User
    name: vinod
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: dev-pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### 4.2 Role for `shyam` (Deployment Manager in `prod` namespace)

```yaml
# prod-deployment-manager-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: prod
  name: prod-deployment-manager
rules:
  - apiGroups: ['apps']
    resources: ['deployments']
    verbs: ['create', 'update', 'delete', 'get', 'list']
```

```yaml
# prod-deployment-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: shyam-deployment-binding
  namespace: prod
subjects:
  - kind: User
    name: shyam
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: prod-deployment-manager
  apiGroup: rbac.authorization.k8s.io
```

Apply all the YAML files:

```bash
kubectl apply -f dev-pod-reader-role.yaml
kubectl apply -f dev-pod-reader-binding.yaml
kubectl apply -f prod-deployment-manager-role.yaml
kubectl apply -f prod-deployment-binding.yaml
```

## Step 5: Test User Access

### Switch to `vinod` kubeconfig

```bash
export KUBECONFIG=./vinod.kubeconfig.yaml
kubectl get pods -n dev     # ✅ Allowed
kubectl get deployments -n dev  # ❌ Forbidden
```

### Switch to `shyam` kubeconfig

```bash
export KUBECONFIG=./shyam.kubeconfig.yaml
kubectl get deployments -n prod  # ✅ Allowed
kubectl get pods -n prod         # ❌ Forbidden
```

## Conclusion

RBAC is essential for securing Kubernetes clusters and implementing proper access controls. Start with restrictive permissions and gradually expand as needed. Regular auditing and following the principle of least privilege will help maintain a secure environment.

Remember to test your RBAC configurations thoroughly before deploying to production, and always maintain proper documentation of your permission structure for easier management and auditing.

With Kubernetes RBAC, you can create fine-grained access controls tailored to specific users and namespaces. In this tutorial, we:

- Created certificates for `vinod` and `shyam`
- Created kubeconfigs for each user
- Defined roles specific to namespaces and resources
- Validated access restrictions using `kubectl`

This setup is scalable for larger teams and more complex policies using RoleBindings and ClusterRoles.

# Prometheus & Grafana for Cluster Monitoring

Prometheus and Grafana are widely used open-source tools for **monitoring and observability** in modern infrastructure, especially with **Kubernetes clusters**. Together, they provide a complete solution for collecting metrics, querying them, visualizing the data, and setting up alerts.

## **What is Prometheus?**

**Prometheus** is an open-source monitoring and alerting toolkit designed for reliability and scalability, especially in dynamic environments like Kubernetes.

### Key Features:

- **Multi-dimensional data model**: Metrics are stored as time-series data with key-value pairs (labels).
- **Powerful query language**: PromQL (Prometheus Query Language) for slicing and dicing metrics.
- **Pull-based model**: Prometheus scrapes targets (applications, nodes) via HTTP endpoints (`/metrics`).
- **No external dependencies**: Works standalone with its own time-series database.
- **Service discovery**: Natively integrates with Kubernetes to automatically discover services and endpoints.
- **Alerting**: Has a built-in Alertmanager for handling alerts (email, Slack, webhooks).

## **What is Grafana?**

**Grafana** is an open-source analytics and visualization platform that supports multiple data sources, including Prometheus.

### Key Features:

- **Rich visualizations**: Dashboards with graphs, charts, heatmaps, gauges, and tables.
- **Data source plugins**: Supports Prometheus, Elasticsearch, Loki, InfluxDB, MySQL, and more.
- **Custom dashboards**: User-defined dashboards for teams, clusters, services, or namespaces.
- **Alerting**: Configure alert rules based on dashboard panels and send notifications via email, Slack, PagerDuty, etc.
- **Templating**: Dashboards can use template variables for dynamic filtering.

## **Prometheus + Grafana: How They Work Together**

- **Prometheus** collects and stores the metrics from Kubernetes.
- **Grafana** connects to Prometheus as a data source and queries this data to create visual dashboards.

## **How They Monitor Kubernetes Clusters**

### 1. **Metric Collection with Prometheus**

Prometheus collects metrics from:

- **Kubernetes nodes**: CPU, memory, disk, network I/O.
- **Kubelet**: Resource usage of pods.
- **API Server**: Request counts, error rates, etc.
- **ETCD**: Health and performance metrics.
- **Controller Manager / Scheduler**: Operation stats and latencies.
- **Applications**: Custom metrics exposed by microservices (usually via `/metrics` endpoint).
- **CNI and CSI plugins**: For network and storage metrics.

> Prometheus uses **Kubernetes service discovery** to automatically find the metric endpoints.

### 2. **Metric Types Monitored**

- **Cluster-wide health**: Node status, component status.
- **Workload metrics**: Pod CPU/memory usage, restarts, lifecycle events.
- **Service performance**: Response time, request rate, error rate.
- **Infrastructure usage**: Disk pressure, memory pressure, container count.
- **Application-specific**: Custom business metrics exposed by services.

### 3. **Dashboards in Grafana**

Grafana provides dashboards that visualize:

- **Cluster Overview**: Status of nodes, pods, deployments.
- **Namespace View**: Resource usage per namespace.
- **Pod Health**: Memory/cpu usage, restarts, uptime.
- **Resource Consumption**: Across containers, workloads.
- **Custom Metrics**: Tracked via service-specific labels and tags.

Grafana allows filtering views based on:

- Namespace
- Pod name
- Service
- Label values (e.g., `app="nginx"`)

### 4. **Alerts and Notifications**

- **Prometheus Alerts**: Based on metric thresholds using PromQL expressions.

  - Example: Alert if node CPU usage > 90% for 5 minutes.

- **Grafana Alerts**: Visual threshold alerts from dashboard panels.

  - Example: Send Slack alert if average memory usage > 80%.

Alerts can be routed to:

- Email
- Slack
- Microsoft Teams
- PagerDuty
- OpsGenie
- Webhooks

## **Monitoring Use Cases in Kubernetes**

| Use Case                         | Description                                                                 |
| -------------------------------- | --------------------------------------------------------------------------- |
| **Node Monitoring**              | Tracks health, resource usage of all nodes in the cluster.                  |
| **Pod and Container Monitoring** | Keeps tabs on pod restarts, resource constraints, OOM kills.                |
| **Application Monitoring**       | Observes HTTP response codes, latency, throughput, errors.                  |
| **Capacity Planning**            | Helps identify under/overutilized resources.                                |
| **Alerting and Troubleshooting** | Immediate alerts and historical data help in identifying incidents quickly. |
| **SLO/SLI Tracking**             | Helps DevOps teams measure service level objectives/indicators.             |

## Monitoring Kubernetes cluster with Prometheus and Grafana

Before starting, ensure you have the following installed:

- **Docker Desktop** or **Podman** (for container runtime)
- **kubectl** (Kubernetes CLI)
- **Helm** (Package manager for Kubernetes)
- **Minikube** (Local Kubernetes cluster)

### Installation Commands

```bash
# Install Helm (macOS)
brew install helm

# Install Helm (Linux)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Minikube (macOS)
brew install minikube

# Install Minikube (Linux)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

## Environment Setup

### 1. Start Minikube Cluster

```bash
# Start minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --driver=docker --nodes=3 -p vincluster
minikube config set profile vincluster

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

### 2. Create Monitoring Namespace

```bash
# Create dedicated namespace for monitoring
kubectl create namespace monitoring

# Set as default namespace for convenience
kubectl config set-context --current --namespace=monitoring
```

### 3. Add Helm Repositories

```bash
# Add Prometheus community helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Add Grafana helm repository
helm repo add grafana https://grafana.github.io/helm-charts

# Update repositories
helm repo update
```

## Installing Prometheus

### 1. Create Prometheus Values File

Create a file named `prometheus-values.yaml`:

```yaml
# prometheus-values.yaml
server:
  securityContext:
    runAsUser: 65534
    runAsGroup: 65534
    fsGroup: 65534
  persistentVolume:
    enabled: false # Using emptyDir for simplicity
  extraVolumes:
    - name: prometheus-data
      emptyDir: {}
  retention: '15d'

# Enable service monitor for automatic discovery
serviceMonitor:
  enabled: true

# Configure alertmanager
alertmanager:
  enabled: true
  persistentVolume:
    enabled: false

# Configure node exporter for host metrics
nodeExporter:
  enabled: true
  hostNetwork: true
  hostPID: true

# Configure kube-state-metrics for Kubernetes metrics
kubeStateMetrics:
  enabled: true

# Configure pushgateway
pushgateway:
  enabled: true
  persistentVolume:
    enabled: false
```

### 2. Install Prometheus

```bash
# Install Prometheus using Helm
helm install prometheus prometheus-community/prometheus \
  --values prometheus-values.yaml

# Wait for all pods to be ready
kubectl get pods -w
```

### 3. Verify Prometheus Installation

```bash
# Check all components are running
kubectl get all

# Get Prometheus server pod name
export PROMETHEUS_POD=$(kubectl get pods -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/component=server" -o jsonpath="{.items[0].metadata.name}")

# Port forward to access Prometheus UI
kubectl port-forward $PROMETHEUS_POD 9090:9090 &

# Access Prometheus at http://localhost:9090
echo "Prometheus UI available at: http://localhost:9090"
```

### 4. Test Prometheus Queries

Open http://localhost:9090 and try these sample queries:

```promql
# CPU usage by node
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage by node
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Pod CPU usage
rate(container_cpu_usage_seconds_total[5m]) * 100

# Pod memory usage
container_memory_usage_bytes / container_spec_memory_limit_bytes * 100
```

## Installing Grafana

### 1. Create Grafana Values File

Create a file named `grafana-values.yaml`:

```yaml
# grafana-values.yaml
adminPassword: 'admin123' # Change this in production

# Configure data sources
datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        url: http://prometheus-server.monitoring.svc.cluster.local:80
        access: proxy
        isDefault: true

# Configure dashboards
dashboardProviders:
  dashboardproviders.yaml:
    apiVersion: 1
    providers:
      - name: 'default'
        orgId: 1
        folder: ''
        type: file
        disableDeletion: false
        editable: true
        options:
          path: /var/lib/grafana/dashboards/default

# Import popular dashboards
dashboards:
  default:
    kubernetes-cluster-monitoring:
      gnetId: 7249
      revision: 1
      datasource: Prometheus
    kubernetes-pod-monitoring:
      gnetId: 6417
      revision: 1
      datasource: Prometheus
    node-exporter:
      gnetId: 1860
      revision: 31
      datasource: Prometheus

# Configure persistence
persistence:
  enabled: false # Using emptyDir for simplicity

# Service configuration
service:
  type: ClusterIP
  port: 80

# Security context
securityContext:
  runAsUser: 472
  runAsGroup: 472
  fsGroup: 472
```

### 2. Install Grafana

```bash
# Install Grafana using Helm
helm install grafana grafana/grafana \
  --values grafana-values.yaml

# Wait for Grafana to be ready
kubectl rollout status deployment/grafana
```

### 3. Access Grafana

```bash
# Get Grafana pod name
export GRAFANA_POD=$(kubectl get pods -l "app.kubernetes.io/name=grafana" -o jsonpath="{.items[0].metadata.name}")

# Port forward to access Grafana UI
kubectl port-forward $GRAFANA_POD 3000:3000

# Access Grafana at http://localhost:3000
echo "Grafana UI available at: http://localhost:3000"
echo "Username: admin"
echo "Password: admin123"
```

## Configuring Dashboards

### 1. Import Additional Dashboards

Once logged into Grafana:

1. Click the "+" icon → Import
2. Use these popular dashboard IDs:
   - **315** - Kubernetes cluster monitoring
   - **8588** - Kubernetes Deployment Statefulset Daemonset metrics
   - **6417** - Kubernetes Pod monitoring
   - **1860** - Node Exporter Full

### 2. Key Metrics to Monitor

Monitor these essential metrics for cluster health:

**Node Metrics:**

- CPU utilization
- Memory utilization
- Disk space usage
- Network I/O

**Pod Metrics:**

- Pod CPU usage
- Pod memory usage
- Pod restart count
- Pod status

**Cluster Metrics:**

- Total pods running
- Failed pods
- Node status
- Kubernetes API server metrics

## Troubleshooting

### Common Issues and Solutions

#### 1. Permission Denied Errors

```bash
# If you see permission denied errors, check security context
kubectl describe pod <pod-name>

# Fix by updating security context in values file
server:
  securityContext:
    runAsUser: 65534
    runAsGroup: 65534
    fsGroup: 65534
```

#### 2. Pod Stuck in Pending State

```bash
# Check node resources
kubectl describe nodes

# Check pod events
kubectl describe pod <pod-name>

# If resource constraints, restart minikube with more resources
minikube delete
minikube start --cpus=4 --memory=8192
```

#### 3. Metrics Not Showing

```bash
# Check if targets are up in Prometheus
# Go to http://localhost:9090/targets

# Verify service discovery
kubectl get servicemonitors

# Check if endpoints are available
kubectl get endpoints
```

#### 4. Grafana Dashboard Not Loading

```bash
# Check Grafana logs
kubectl logs deployment/grafana

# Verify data source connection
# Go to Grafana → Configuration → Data Sources → Test
```

### Debugging Commands

```bash
# Check all resources in monitoring namespace
kubectl get all

# Check persistent volumes
kubectl get pv,pvc

# Check services and endpoints
kubectl get svc,endpoints

# Check ConfigMaps and Secrets
kubectl get configmaps,secrets

# View pod logs
kubectl logs <pod-name> -f

# Execute into pods for debugging
kubectl exec -it <pod-name> -- /bin/sh
```

## Best Practices

### 1. Resource Management

```yaml
# Set appropriate resource limits
resources:
  limits:
    cpu: 1000m
    memory: 2Gi
  requests:
    cpu: 500m
    memory: 1Gi
```

### 2. Data Retention

```yaml
# Configure appropriate retention periods
server:
  retention: '15d' # For development
  # retention: "90d"  # For production
```

### 3. Security Considerations

```yaml
# Use proper security contexts
securityContext:
  runAsNonRoot: true
  runAsUser: 65534
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

### 4. Monitoring Best Practices

- **Start with basic metrics**: CPU, memory, disk, network
- **Set up alerts gradually**: Begin with critical alerts, add more over time
- **Use appropriate scrape intervals**: 15s for critical metrics, 1m for others
- **Organize dashboards by audience**: Infrastructure, application, business metrics
- **Document your setup**: Keep track of custom configurations and dashboards

### 5. Cleanup Commands

```bash
# Remove all monitoring components
helm uninstall prometheus
helm uninstall grafana

# Delete namespace
kubectl delete namespace monitoring

# Stop minikube
minikube stop

# Delete minikube cluster
minikube delete
```

### 6. Production Considerations

When moving to production, consider:

- **Enable persistent storage** for data retention
- **Set up proper backup** strategies
- **Configure HTTPS/TLS** for secure access
- **Implement proper RBAC** for access control
- **Use external databases** for Grafana configuration
- **Set up proper alerting channels** (email, Slack, PagerDuty)
- **Monitor the monitoring system** itself

## Conclusion

You now have a complete Prometheus and Grafana monitoring setup on Minikube! This setup provides:

- **Comprehensive metrics collection** from Kubernetes components
- **Visual dashboards** for cluster performance monitoring
- **Alerting capabilities** for proactive issue detection
- **Scalable architecture** that can be adapted for production use

Practice with different queries, create custom dashboards, and experiment with alerting rules to become proficient with this powerful monitoring stack.

# Centralized Logging with ELK Stack in Kubernetes

## **Centralized Logging with ELK Stack in Kubernetes**

### **Overview**

Centralized logging is critical in a microservices architecture to track and debug application behavior across distributed components. The **ELK Stack**—**Elasticsearch**, **Logstash**, and **Kibana**—is widely used for this purpose. When running in Kubernetes, log aggregation becomes seamless if the ELK stack is set up correctly.

## **Architecture**

```
[Application Pods] --> [Log Collector (Filebeat/Fluentd)] --> [Logstash] --> [Elasticsearch] --> [Kibana]
```

- **Filebeat**: Lightweight log shipper that reads logs from pods.
- **Logstash**: Parses and transforms logs.
- **Elasticsearch**: Indexes and stores logs.
- **Kibana**: Visualizes logs.

## **Prerequisites**

- Kubernetes cluster (Minikube, Kind, or a cloud provider).
- `kubectl` configured.
- `helm` installed.
- Access to Docker images (for building custom images if needed).

## **Deploying ELK Stack in Kubernetes**

### **Step 1: Add Helm Repos**

```bash
helm repo add elastic https://helm.elastic.co
helm repo update
```

### **Step 2: Deploy Elasticsearch**

```bash
helm install elasticsearch elastic/elasticsearch \
  --version 7.17.3 \
  --set replicas=1 \
  --set minimumMasterNodes=1 \
  --set persistence.enabled=false \
  --set resources.requests.memory=512Mi \
  --set resources.limits.memory=1Gi \
  --set readinessProbe.timeoutSeconds=5 \
  --set readinessProbe.periodSeconds=10 \
  --set readinessProbe.failureThreshold=10
```

> Elasticsearch should now be accessible as a service in your cluster.

### **Step 3: Deploy Kibana**

```bash
helm install kibana elastic/kibana \
  --version 7.17.3 \
  --set elasticsearchURL=http://elasticsearch-master:9200
```

> Forward port to access Kibana dashboard:

```bash
kubectl port-forward svc/kibana-kibana 5601:5601
```

Access: `http://localhost:5601`

### **Step 4: Deploy Filebeat as DaemonSet**

```bash
helm install filebeat elastic/filebeat \
  --version 7.17.3 \
  --set elasticsearch.hosts="{http://elasticsearch-master:9200}" \
  --set filebeat.inputs[0].type=container \
  --set filebeat.inputs[0].paths[0]="/var/log/containers/*.log" \
  --set tolerations[0].operator="Exists" \
  --set nodeSelector."kubernetes\\.io/os"=linux
```

> Filebeat reads logs from all containers and sends them to Elasticsearch.

## **(Optional) Use Logstash for Parsing**

If you want to do more complex parsing or filtering:

### **Deploy Logstash**

```bash
helm install logstash elastic/logstash \
  --version 7.17.3 \
  --set elasticsearch.hosts[0]="http://elasticsearch-master:9200"
```

> Configure Filebeat to send data to Logstash:

```yaml
output.logstash:
  hosts: ['logstash:5044']
```

> And update Logstash config to parse and forward to Elasticsearch.

## **Visualizing Logs in Kibana**

1. Go to **[http://localhost:5601](http://localhost:5601)**.
2. Create an index pattern matching your logs (e.g., `filebeat-*`).
3. Use Discover, Visualize, and Dashboard sections to analyze logs.

## **Best Practices**

- Use persistent storage for Elasticsearch.
- Enable RBAC and TLS for secure communication.
- Limit log retention to reduce disk usage.
- Use namespaces and labels to organize log data.

## **Cleanup**

```bash
helm uninstall filebeat
helm uninstall logstash
helm uninstall kibana
helm uninstall elasticsearch
```

## **Sample Use Case: Debugging a Failing Pod**

1. Application crashes due to an uncaught exception.
2. Filebeat forwards logs to Elasticsearch.
3. Use Kibana to search logs: `kubernetes.pod.name: myapp-pod`
4. Inspect stack trace, container logs, and timestamp to resolve issues.
