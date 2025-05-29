## **Capstone Project: Smart Inventory and Order Management System**

### **Objective**

You are required to build, containerize, and deploy a Flask-based microservices architecture using Docker, Helm charts for Kubernetes deployment, Jenkins for CI/CD, and Ansible for automation.

## **Microservices Overview**

1. **Inventory Service**
   Tracks items in stock and supports operations like add/update/remove items, and fetch stock levels.

2. **Order Service**
   Accepts new customer orders, validates item availability by calling Inventory Service, and confirms/rejects the order.

3. **Pricing Service**
   Maintains dynamic pricing for items, provides pricing info to Order Service, and allows admin updates.

4. **Analytics Service**
   Collects data from other services (e.g., order counts, inventory levels) and generates reports or basic analytics.

5. **Notification Service**
   Sends out alerts (mocked email/log entries) when:

   - Inventory is low
   - An order is processed
   - Prices change

## **Tech Stack**

| Component        | Tool / Platform                |
| ---------------- | ------------------------------ |
| Microservices    | Flask (Python)                 |
| Containerization | Docker                         |
| CI/CD            | Jenkins (Declarative Pipeline) |
| Automation       | Ansible                        |
| Deployment       | Kubernetes                     |
| Helm Packaging   | Helm                           |

## **Detailed Task Breakdown**

### Phase 1: Microservices Development using Flask (Python)

Each microservice should be developed using **Flask REST APIs**.

#### Tasks

- **Set up Flask project structure**.
- **Use SQLite or in-memory data store** for simplicity.
- **Define REST endpoints** (example shown below).
- **Implement inter-service HTTP communication** using `requests` library.

#### Example APIs per Service

- **Inventory Service**:

  - `GET /items` – List all items
  - `GET /items/<item_id>` – Get item details
  - `POST /items` – Add a new item
  - `PUT /items/<item_id>` – Update item stock
  - `GET /items/<item_id>/check` – Check stock availability

- **Order Service**:

  - `POST /orders` – Place a new order
  - `GET /orders/<order_id>` – Get order status

- **Pricing Service**:

  - `GET /price/<item_id>` – Get item price
  - `PUT /price/<item_id>` – Update item price

- **Analytics Service**:

  - `GET /report/orders` – Daily order count
  - `GET /report/low-stock` – Items with stock < 10

- **Notification Service**:

  - `POST /notify/low-stock` – Triggered when stock is low
  - `POST /notify/order` – Triggered when order is processed

### Phase 2: Dockerization

#### Tasks

- Create **Dockerfile** for each service.
- Use `python:3.10-slim` or similar base image.
- Use Gunicorn to expose the Flask app via `0.0.0.0` on port 5000 or unique port per service.
- Build Docker images:

  ```bash
  docker build -t inventory-service .
  ```

- Tag and push to Docker Hub (for CI/CD).

### Phase 3: Docker Compose (Optional Step for Local Testing)

#### Tasks

- Create a `docker-compose.yml` file to spin up all services locally.
- Use Docker Compose networking for service discovery.
- Define service dependencies (e.g., Order depends on Inventory and Pricing).

### Phase 4: Jenkins for CI/CD

#### Tasks

- Set up Jenkins pipeline using **Declarative Pipeline syntax**.
- For each service:

  - Pull code from Git (GitHub or local repo)
  - Run unit tests (optional pytest)
  - Build Docker image
  - Push image to Docker Hub or private registry
  - Deploy to Kubernetes
    s

### Phase 5: **Helm Chart for Each Microservice**

Each student must create a **Helm chart** for every microservice.

#### Tasks

1. Create a Helm chart and sub-charts for each microservice.
2. Folder structure:

   ```
   sioms-chart/
   ├── Chart.yaml
   ├── values.yaml
   ├── charts/
   │   ├── inventory-service/
   │   │   ├── Chart.yaml
   │   │   ├── values.yaml
   │   │   └── templates/
   │   │       ├── deployment.yaml
   │   │       └── service.yaml
   │   ├── order-service/
   │   │   ├── Chart.yaml
   │   │   ├── values.yaml
   │   │   └── templates/
   │   │       ├── deployment.yaml
   │   │       └── service.yaml
   │   ├── pricing-service/
   │   │   ├── Chart.yaml
   │   │   ├── values.yaml
   │   │   └── templates/
   │   │       ├── deployment.yaml
   │   │       └── service.yaml
   │   ├── analytics-service/
   │   │   ├── Chart.yaml
   │   │   ├── values.yaml
   │   │   └── templates/
   │   │       ├── deployment.yaml
   │   │       └── service.yaml
   │   └── notification-service/
   │       ├── Chart.yaml
   │       ├── values.yaml
   │       └── templates/
   │           ├── deployment.yaml
   │           └── service.yaml
   ```

3. Customize templates with placeholders:

   - `image.repository`, `image.tag`
   - `service.port`
   - `resources`
   - `env` variables using `values.yaml`

4. Example `values.yaml`:

   ```yaml
   replicaCount: 2
   image:
     repository: yourdockerhub/inventory-service
     tag: '1.0.0'
   service:
     type: NodePort
     port: 5000
   ```

5. Optional: Add ConfigMaps or Secrets if services need configuration.

### Phase 6: Helm-Based Deployment

Use Helm to install the services:

```bash
helm install sioms sioms-chart/ --namespace sioms
```

### Phase 7: CI/CD Deployment with Jenkins + Helm

Update the Jenkinsfile to include:

```groovy
stage('Helm Deploy') {
  steps {
    sh 'helm upgrade --install sioms sioms-chart/ --namespace sioms --create-namespace'
  }
}
```

### Phase 8: Ansible for Helm-Oriented Automation

Update Ansible playbooks to:

- Install Helm (if not present).
- Clone the project repo.
- Run Helm install or upgrade commands.
- (Optional) Use `helm diff` plugin for safer upgrades.

## **Example Project Folder Structure**

```
smart-inventory-system/
├── services/
│   ├── inventory/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── utils.py
│   │   ├── tests/
│   │   │   └── test_routes.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── orders/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── utils.py
│   │   ├── tests/
│   │   │   └── test_routes.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── pricing/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── utils.py
│   │   ├── tests/
│   │   │   └── test_routes.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── analytics/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── utils.py
│   │   ├── tests/
│   │   │   └── test_routes.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── notifications/
│       ├── app/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── routes.py
│       │   └── utils.py
│       ├── tests/
│       │   └── test_routes.py
│       ├── Dockerfile
│       └── requirements.txt
├── helm/
│   └── sioms-chart/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── charts/
│           ├── inventory-service/
│           ├── order-service/
│           ├── pricing-service/
│           ├── analytics-service/
│           └── notification-service/
├── ansible/
│   ├── inventory.yml
│   ├── playbook.yml
│   └── roles/
│       ├── docker/
│       ├── kubernetes/
│       └── helm/
├── jenkins/
│   └── Jenkinsfile
├── docker-compose.yml
├── README.md
└── .gitignore
```

## **Pro tips**

### Development Setup

1. **Service Template Creation**

   - Consider writing a shell script to generate the basic Flask service structure
   - Script could create folders, **init**.py files, and basic route templates
   - Include common requirements.txt generation
   - Create basic test structure

2. **Docker Setup**

   - Create a base Dockerfile template that can be customized per service
   - Consider using multi-stage builds to keep images small
   - Use .dockerignore to exclude tests and development files

3. **Service Communication**
   - Implement service discovery using environment variables
   - Use retries and circuit breakers for inter-service communication
   - Consider using Flask-RestX or FastAPI for automatic API documentation

### Helm Chart Management

1. **Chart Generation**

   - Consider creating a script to generate basic Helm chart structure
   - Use a template values.yaml that can be customized per service
   - Maintain a common set of labels and annotations

2. **Development Tips**
   - Use `helm lint` to validate charts
   - Test with `helm template` before deploying
   - Create a values-dev.yaml for development settings

### CI/CD Best Practices

1. **Jenkins Pipeline**

   - Break pipeline into reusable shared libraries
   - Use parameters for flexible deployments
   - Implement proper error handling and notifications

2. **Testing Strategy**
   - Run unit tests in parallel
   - Implement integration tests using docker-compose
   - Consider using pytest-docker-compose for integration testing

### Automation Tips

1. **Local Development**

   - Create scripts for:
     - Setting up local development environment
     - Running all services locally
     - Database initialization
     - Test data generation

2. **Deployment**
   - Script for checking deployment prerequisites
   - Automated rollback procedures
   - Health check implementation

### Common Pitfalls to Avoid

1. **Architecture**

   - Don't tightly couple services
   - Implement proper error handling between services
   - Use appropriate timeout values

2. **Docker**

   - Don't run containers as root
   - Properly handle container signals
   - Use proper cache management in Dockerfile

3. **Kubernetes**

   - Set resource limits and requests
   - Implement proper health checks
   - Use appropriate update strategies

4. **Security**
   - Don't commit secrets to Git
   - Use proper network policies
   - Implement appropriate RBAC

### Useful Tools

1. **Development**

   - Postman/Insomnia for API testing
   - HTTPie for command-line API testing
   - Flask-DebugToolbar for debugging

2. **Monitoring**

   - Prometheus for metrics
   - Grafana for visualization
   - ELK stack for logging

3. **Testing**
   - pytest for Python testing
   - locust for load testing
   - coverage.py for code coverage

**Remember to maintain a development journal documenting challenges and solutions encountered during the project implementation.**
