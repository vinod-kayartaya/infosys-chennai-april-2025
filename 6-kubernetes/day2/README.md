In **Kubernetes**, a **DaemonSet** ensures that **a copy of a pod runs on all (or some) nodes in the cluster**. It is useful for running background tasks like:

- Log collection (e.g., Fluentd)
- Node monitoring (e.g., Prometheus Node Exporter)
- System-level agents (e.g., anti-virus, storage sync)

## Key Features of DaemonSet

- Automatically adds pods when a new node joins the cluster.
- Removes pods when a node is removed.
- If the DaemonSet is deleted, all its pods are removed.

## Sample DaemonSet YAML

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: my-daemonset
  labels:
    app: my-daemon
spec:
  selector:
    matchLabels:
      name: my-daemon-pod
  template:
    metadata:
      labels:
        name: my-daemon-pod
    spec:
      containers:
        - name: daemon-container
          image: busybox
          command:
            [
              'sh',
              '-c',
              'while true; do echo Hello from the DaemonSet; sleep 30; done',
            ]
```

## Common Commands with DaemonSets

### 1. Create a DaemonSet

```bash
kubectl apply -f my-daemonset.yaml
```

- This will create a DaemonSet and deploy a pod on every node.

### 2. List all DaemonSets

```bash
kubectl get daemonsets
kubectl get ds  # shorthand
```

**Optional: specify namespace**

```bash
kubectl get ds -n kube-system
```

### 3. Describe a DaemonSet

```bash
kubectl describe daemonset my-daemonset
```

- Gives detailed info such as number of pods scheduled, image used, node selectors, etc.

### 4. Check Pods created by a DaemonSet

```bash
kubectl get pods -o wide --selector=name=my-daemon-pod
```

- Lists the DaemonSet pods and shows which nodes they are running on.

### 5. Update a DaemonSet

Edit directly:

```bash
kubectl edit daemonset my-daemonset
```

Or apply changes to a new YAML file:

```bash
kubectl apply -f updated-daemonset.yaml
```

### 6. Rolling Update a DaemonSet

By default, DaemonSets do not perform rolling updates (unlike Deployments). You must use:

```yaml
spec:
  updateStrategy:
    type: RollingUpdate
```

Then run:

```bash
kubectl rollout status daemonset/my-daemonset
```

### 7. Delete a DaemonSet

```bash
kubectl delete daemonset my-daemonset
```

### 8. View YAML of an Existing DaemonSet

```bash
kubectl get daemonset my-daemonset -o yaml
```

### 9. Filter Nodes for DaemonSet

You can restrict the DaemonSet to certain nodes using:

#### a. Node Selectors

```yaml
spec:
  template:
    spec:
      nodeSelector:
        disktype: ssd
```

#### b. Node Affinity

```yaml
spec:
  template:
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: kubernetes.io/hostname
                    operator: In
                    values:
                      - node-1
```

Node Affinity provides more expressive pod placement rules than nodeSelector:

- `requiredDuringSchedulingIgnoredDuringExecution`: Hard requirement that must be met to schedule the pod
- `matchExpressions`: Allows complex matching rules using operators like `In`, `NotIn`, `Exists`, `DoesNotExist`
- The example above ensures the DaemonSet pod only runs on the node with hostname "node-1"
- You can specify multiple rules and they will be combined with logical AND

## Notes

- Pods managed by DaemonSets do **not** use ReplicaSets.
- They are automatically scheduled on nodes by the **DaemonSet controller**.
- DaemonSets respect **taints and tolerations** if specified.

## Use Cases for DaemonSets

| Use Case   | Example                  |
| ---------- | ------------------------ |
| Monitoring | Prometheus Node Exporter |
| Logging    | Fluentd, Logstash        |
| Storage    | Glusterd, Ceph           |
| Network    | Weave, Calico            |

In **Kubernetes**, a **ReplicaSet** is a controller that ensures a specified number of pod **replicas** are running at any given time. If a pod fails or is terminated, the ReplicaSet automatically creates a new pod to maintain the desired count.

## **What is a ReplicaSet?**

- Ensures high availability by maintaining a **stable set of replica pods**.
- It **replaces pods** if they are deleted or fail.
- Usually, **ReplicaSets are not created directly**, but through **Deployments**, which manage them.

## **Basic Structure of a ReplicaSet YAML**

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: my-replicaset
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: mycontainer
          image: nginx
          ports:
            - containerPort: 80
```

## **Key Commands and Their Descriptions**

### 1. **Create a ReplicaSet**

```bash
kubectl apply -f replicaset.yaml
```

- Creates the ReplicaSet from the YAML file.
- If pods don’t already exist, it launches the specified number of replicas.

### 2. **List ReplicaSets**

```bash
kubectl get rs
```

- Displays all ReplicaSets in the current namespace.

### 3. **Describe a ReplicaSet**

```bash
kubectl describe rs my-replicaset
```

- Shows detailed information, including labels, selectors, events, and pod template.

### 4. **View Pods Created by a ReplicaSet**

```bash
kubectl get pods -l app=myapp
```

- Lists pods created by the ReplicaSet, filtered using label selector.

### 5. **Scale a ReplicaSet**

```bash
kubectl scale rs my-replicaset --replicas=5
```

- Increases or decreases the number of pods (to the specified number) managed by the ReplicaSet.

### 6. **Edit a ReplicaSet**

```bash
kubectl edit rs my-replicaset
```

- Opens the ReplicaSet manifest in a text editor to make live changes (e.g., change the number of replicas).

### 7. **Delete a ReplicaSet**

```bash
kubectl delete rs my-replicaset
```

- Deletes the ReplicaSet and its pods **if not managed by a Deployment**.

### 8. **Check Events for a ReplicaSet**

```bash
kubectl get events --sort-by='.metadata.creationTimestamp'
```

- Useful for troubleshooting if pods aren’t getting created.

## **Important Notes:**

- **Selector and Labels** are critical. A ReplicaSet uses the selector to know which pods to manage.
- If the selector matches existing pods **not created** by the ReplicaSet, it will try to adopt them.
- **ReplicaSets vs Deployments**:

  - Use **Deployments** for most use-cases (as they provide rolling updates and rollback).
  - ReplicaSet is used under the hood by Deployments.

# ConfigMaps and Secrets

In Kubernetes, **ConfigMaps** and **Secrets** are used to **externalize configuration** from your application code. This makes your application more flexible and secure.

## **1. ConfigMaps**

Used to store **non-sensitive configuration data**, such as application settings, URLs, or filenames.

### **Example: ConfigMap**

Suppose your app needs two environment variables: `APP_MODE` and `APP_PORT`.

**Step 1: Create a ConfigMap**

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_MODE: 'production'
  APP_PORT: '8080'
```

**Create it:**

```bash
kubectl apply -f configmap.yaml
```

**Step 2: Use it in a Pod**

```yaml
# pod-using-configmap.yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
    - name: app-container
      image: myapp:latest
      env:
        - name: APP_MODE
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_MODE
        - name: APP_PORT
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_PORT
```

### **1. ConfigMap with key-value pairs (CLI method)**

```bash
kubectl create configmap app-config-cli \
  --from-literal=ENV=staging \
  --from-literal=LOG_LEVEL=debug
```

**Usage in Deployment:**

```yaml
env:
  - name: ENV
    valueFrom:
      configMapKeyRef:
        name: app-config-cli
        key: ENV
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: app-config-cli
        key: LOG_LEVEL
```

### **2. ConfigMap from a file**

**Create a file `app.properties`:**

```
ENV=dev
LOG_LEVEL=info
MAX_CONNECTIONS=100
```

```bash
kubectl create configmap app-config-file --from-file=app.properties
```

**Mount it as a volume:**

```yaml
volumeMounts:
  - name: config-volume
    mountPath: /etc/config
    readOnly: true
volumes:
  - name: config-volume
    configMap:
      name: app-config-file
```

The app can now read from `/etc/config/app.properties`.

### **3. ConfigMap as environment variables (entire config)**

```yaml
envFrom:
  - configMapRef:
      name: app-config-cli
```

This injects **all** key-value pairs from the configmap into the container as environment variables.

## **2. Secrets**

Used to store **sensitive data**, such as passwords, API keys, tokens, etc. Secrets are **Base64-encoded** for safe transmission and storage.

### **Example: Secret**

Suppose your app needs a `DB_PASSWORD`.

**Step 1: Create a Secret**

```bash
kubectl create secret generic db-secret --from-literal=DB_PASSWORD='myS3cretPass'
```

**Step 2: Use it in a Pod**

```yaml
# pod-using-secret.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
spec:
  containers:
    - name: db-app
      image: mydbapp:latest
      env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: DB_PASSWORD
```

### **1. Secret with CLI (simple password)**

```bash
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=P@ssw0rd123
```

**Use in environment variables:**

```yaml
env:
  - name: DB_USERNAME
    valueFrom:
      secretKeyRef:
        name: db-credentials
        key: username
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: db-credentials
        key: password
```

### **2. Secret from a file**

Create a file `api-key.txt` containing your secret key.

```bash
kubectl create secret generic api-key-secret --from-file=api-key.txt
```

**Mount it as a volume:**

```yaml
volumeMounts:
  - name: secret-volume
    mountPath: /etc/secrets
    readOnly: true
volumes:
  - name: secret-volume
    secret:
      secretName: api-key-secret
```

Your app can now read the key from `/etc/secrets/api-key.txt`.

### **3. Secret for Docker Registry Credentials**

Used for private Docker images.

```bash
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=vinod_user \
  --docker-password=mydockersecret \
  --docker-email=vinod@example.com
```

**Usage in a Pod:**

```yaml
imagePullSecrets:
  - name: regcred
```

### **4. EnvFrom using Secret (inject all keys)**

```yaml
envFrom:
  - secretRef:
      name: db-credentials
```

Injects all keys from the secret as environment variables.

**Tip: Decode Secret in Base64**

If you create secrets using YAML directly, you need to encode the values:

```bash
echo -n 'P@ssw0rd123' | base64
```

YAML example:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  password: UEAzc3cwcmQxMjM=
```

## **List and Inspect Secrets**

### a. List all secrets in current namespace

```bash
kubectl get secrets
```

### b. List secrets in a specific namespace

```bash
kubectl get secrets -n <namespace-name>
```

### c. Show details of a secret

```bash
kubectl describe secret db-secret
```

### d. Get secret in YAML format

```bash
kubectl get secret db-secret -o yaml
```

## **Decode Secret Data (Base64)**

### a. Decode individual key

```bash
kubectl get secret db-secret -o jsonpath="{.data.DB_PASSWORD}" | base64 --decode
```

### b. Decode all keys (loop)

```bash
for key in $(kubectl get secret db-secret -o json | jq -r '.data | keys[]'); do
  echo -n "$key: "
  kubectl get secret db-secret -o jsonpath="{.data.$key}" | base64 --decode
  echo
done
```

(Requires `jq` installed)

## **Delete a Secret**

```bash
kubectl delete secret db-secret
```

## **Edit a Secret**

This opens the secret in your default editor:

```bash
kubectl edit secret db-secret
```

> Remember: values are in **Base64** — you'll need to encode/decode manually.

## **Export/Backup a Secret (for redeploy)**

```bash
kubectl get secret db-secret -o yaml > db-secret.yaml
```

To recreate:

```bash
kubectl apply -f db-secret.yaml
```

## **Summary**

| Feature     | ConfigMap                        | Secret                           |
| ----------- | -------------------------------- | -------------------------------- |
| Purpose     | Non-sensitive config             | Sensitive info (passwords, keys) |
| Data Format | Plain text                       | Base64-encoded                   |
| Access      | Env variables, files, or volumes | Env variables, files, or volumes |
| Use Case    | App settings                     | DB passwords, tokens             |

# Volumes

In **Kubernetes (K8s)**, a **Volume** is a directory accessible to containers in a Pod. Unlike a container’s local storage (which is temporary and tied to the container's life), volumes exist **independently of the container** and can preserve data across container restarts.

### **Why Use Volumes?**

1. **Persistent data** – Store data even if the container dies.
2. **Sharing data** – Allow multiple containers in a pod to access the same files.
3. **Configuration** – Inject config files or secrets into a container.

### **Types of Volumes in Kubernetes**

Some common volume types:

- `emptyDir`
- `hostPath`
- `configMap`
- `secret`
- `persistentVolumeClaim` (PVC)

### **1. emptyDir Volume Example**

Used to share temporary storage between containers in a pod.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: app-container
      image: busybox
      command: ['sh', '-c', 'echo Hello > /data/message; sleep 3600']
      volumeMounts:
        - name: myvolume
          mountPath: /data
    - name: sidecar
      image: busybox
      command: ['sh', '-c', 'cat /data/message; sleep 3600']
      volumeMounts:
        - name: myvolume
          mountPath: /data
  volumes:
    - name: myvolume
      emptyDir: {}
```

**Explanation:**

- Both containers share `/data` via `emptyDir`.
- The first container writes a message, the second reads it.

### **2. hostPath Volume Example**

Mounts a file or directory from the node’s filesystem.

```yaml
volumes:
  - name: host-volume
    hostPath:
      path: /var/log
```

**Caution**: Useful in testing but not recommended in production due to tight node coupling.

### **3. ConfigMap Volume Example**

Inject configuration files into a container.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    key1=value1
    key2=value2
```

```yaml
volumeMounts:
  - name: config-volume
    mountPath: /etc/config
volumes:
  - name: config-volume
    configMap:
      name: app-config
```

**Explanation**: The container sees `/etc/config/app.properties` file inside.

### **4. PersistentVolumeClaim (PVC) Example**

Used for **persistent storage** like cloud disks or network drives.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

```yaml
volumeMounts:
  - name: persistent-storage
    mountPath: /data
volumes:
  - name: persistent-storage
    persistentVolumeClaim:
      claimName: myclaim
```

**Explanation**: Data stored in `/data` will survive pod restarts.

# Deployment in Kubernetes

In Kubernetes, a **Deployment** is a higher-level **controller** that manages **ReplicaSets** and provides **declarative updates** to Pods and ReplicaSets. It is one of the most commonly used resources in Kubernetes.

A **Deployment** allows you to:

- **Create and manage ReplicaSets**, which in turn manage the Pods.
- **Update the application** without downtime using **rolling updates**.
- **Rollback** to previous versions in case of failure.
- **Scale the application** up or down easily.
- Manage **stateless applications** efficiently.

## **Basic Deployment YAML Example**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: nginx-container
          image: nginx:latest
          ports:
            - containerPort: 80
```

## **Key Features of a Deployment**

| Feature              | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| **replicas**         | Desired number of pod copies                                |
| **selector**         | Matches Pods using labels                                   |
| **template**         | Defines the Pod's specification (same as in Pod/ReplicaSet) |
| **strategy**         | Specifies update strategy (default is RollingUpdate)        |
| **revision history** | Allows rollback to previous versions                        |

## **All Important Commands for Deployments**

### 1. **Create a Deployment**

```bash
kubectl apply -f deployment.yaml
```

- Creates a new Deployment from the YAML definition.

### 2. **List Deployments**

```bash
kubectl get deployments
```

- Lists all Deployments in the current namespace.

### 3. **Describe a Deployment**

```bash
kubectl describe deployment my-deployment
```

- Shows detailed info: events, selectors, replica sets, pod template, etc.

### 4. **Check ReplicaSets Managed by a Deployment**

```bash
kubectl get rs
```

- Lists ReplicaSets created and managed by Deployments.

### 5. **View Pods Created by a Deployment**

```bash
kubectl get pods -l app=myapp
```

- View pods with specific label set in Deployment.

### 6. **Update the Deployment (e.g., change image)**

```bash
kubectl set image deployment/my-deployment nginx-container=nginx:1.25
```

- Updates the container image, triggering a rolling update.

### 7. **Check Rollout Status**

```bash
kubectl rollout status deployment/my-deployment
```

- Shows progress of a deployment update.

### 8. **Rollback to Previous Revision**

```bash
kubectl rollout undo deployment/my-deployment
```

- Rollback to previous working state if the new rollout fails.

### 9. **View Revision History**

```bash
kubectl rollout history deployment/my-deployment
```

- Lists all revisions of the deployment.

### 10. **Scale the Deployment**

```bash
kubectl scale deployment my-deployment --replicas=5
```

- Changes the number of pods the deployment maintains.

### 11. **Pause and Resume Rollout**

```bash
kubectl rollout pause deployment my-deployment
kubectl rollout resume deployment my-deployment
```

- Pause a deployment before making changes and resume after.

### 12. **Delete a Deployment**

```bash
kubectl delete deployment my-deployment
```

- Deletes the Deployment and associated ReplicaSets and Pods.

### 13. **Edit a Deployment**

```bash
kubectl edit deployment my-deployment
```

- Opens a live editor to modify the deployment YAML.

## **Tips and Best Practices**

- Always use **labels** and **selectors** properly; they are critical for managing pods.
- Use **`kubectl rollout`** commands to manage updates and rollbacks effectively.
- Prefer **Deployments over ReplicaSets** directly for better control and stability.
- Test with **probes (readiness/liveness)** for production-grade deployments.
