# API Groups

## Empty String in apiGroups

The empty string `""` refers to the **core API group** (also called the "legacy" API group). This is where Kubernetes stores its fundamental, built-in resources.

### Core API Group Resources

When you use `apiGroups: [""]`, you're referencing resources from the core API group, which includes:

- `pods`
- `services`
- `configmaps`
- `secrets`
- `namespaces`
- `nodes`
- `persistentvolumes`
- `persistentvolumeclaims`
- `serviceaccounts`
- `endpoints`
- `events`

### Example Comparison

```yaml
# Core API group (empty string)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: core-resources-role
rules:
  - apiGroups: [''] # Empty string = core API group
    resources: ['pods', 'services', 'configmaps']
    verbs: ['get', 'list']

---
# Named API group
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: apps-resources-role
rules:
  - apiGroups: ['apps'] # Named API group
    resources: ['deployments', 'replicasets']
    verbs: ['get', 'list']
```

### How to Identify API Groups

You can check which API group a resource belongs to:

```bash
# List all API resources with their groups
kubectl api-resources

# Example output:
# NAME          SHORTNAMES   APIVERSION   NAMESPACED   KIND
# pods          po           v1           true         Pod
# services      svc          v1           true         Service
# deployments   deploy       apps/v1      true         Deployment
# ingresses     ing          networking.k8s.io/v1     true         Ingress
```

In the output:

- `v1` means core API group (empty string in RBAC)
- `apps/v1` means "apps" API group
- `networking.k8s.io/v1` means "networking.k8s.io" API group

### Complete Example

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: multi-group-role
rules:
  # Core API group resources
  - apiGroups: ['']
    resources: ['pods', 'services', 'secrets']
    verbs: ['get', 'list', 'watch']

  # Apps API group resources
  - apiGroups: ['apps']
    resources: ['deployments', 'daemonsets']
    verbs: ['get', 'list', 'create', 'update']

  # Networking API group resources
  - apiGroups: ['networking.k8s.io']
    resources: ['ingresses']
    verbs: ['get', 'list']
```

### Why the Empty String?

This design choice maintains backward compatibility. The core Kubernetes resources existed before the API group concept was introduced, so they remained in the "default" or "core" group, represented by an empty string rather than being moved to a named group like "core" or "v1".

So remember: `apiGroups: [""]` = core Kubernetes resources like pods, services, configmaps, secrets, etc.
