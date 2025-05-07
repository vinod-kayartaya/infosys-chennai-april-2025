# Jenkins Day 3 Assignment: Parallel Execution and Shared Libraries

## Assignment 1: Parallel Build Stages Implementation

### Objective

Create a Jenkins pipeline that efficiently runs multiple build stages in parallel for a Python Flask application.

### Requirements

1. Create a new pipeline that implements parallel execution for:

   - Unit tests
   - Integration tests
   - API tests
   - Code quality checks (pylint, flake8)
   - Security scanning
   - Documentation generation

2. Implement proper resource management:
   - Set appropriate timeouts for each parallel stage
   - Handle stage failures gracefully
   - Implement retry mechanisms for flaky tests
   - Collect and aggregate test results

### Expected Pipeline Structure

```groovy
pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                // Setup steps
            }
        }
        stage('Parallel Execution') {
            parallel {
                // Parallel stages here
            }
        }
        stage('Results') {
            steps {
                // Aggregate and report results
            }
        }
    }
}
```

### Implementation Details

1. **Setup Stage**:

   - Create Python virtual environment
   - Install dependencies
   - Set up test databases
   - Configure test environment

2. **Parallel Stages**:

   - Unit Tests:

     - Run pytest for unit tests
     - Generate coverage report
     - Set timeout of 10 minutes
     - Retry up to 2 times on failure

   - Integration Tests:

     - Run integration test suite
     - Test database interactions
     - Set timeout of 15 minutes
     - No retries on failure

   - API Tests:

     - Test all API endpoints
     - Validate response formats
     - Set timeout of 20 minutes
     - Retry up to 2 times on failure

   - Code Quality:

     - Run pylint
     - Run flake8
     - Generate code quality report
     - Set timeout of 5 minutes

   - Security Scan:

     - Run bandit for security checks
     - Check for known vulnerabilities
     - Set timeout of 10 minutes

   - Documentation:
     - Generate API documentation
     - Create test coverage report
     - Set timeout of 5 minutes

3. **Results Stage**:
   - Aggregate test results
   - Generate combined coverage report
   - Create build summary
   - Archive artifacts

### Submission Requirements

1. Jenkinsfile with parallel execution implementation
2. Screenshots of:
   - Pipeline execution with parallel stages
   - Test results and coverage reports
   - Code quality reports
   - Security scan results
3. Documentation explaining:
   - Parallel stage configuration
   - Resource management approach
   - Failure handling strategy
   - Results aggregation method

---

## Assignment 2: Basic Shared Library Implementation

### Objective

Create a simple shared library that provides basic utility functions for Python application builds.

### Requirements

1. Create a new Git repository named `jenkins-python-utils`
2. Implement the following shared library functions:
   - `setupPythonEnv`: Creates and activates a Python virtual environment
   - `runTests`: Executes pytest with coverage reporting
   - `buildDockerImage`: Builds a Docker image for the application

### Expected Structure

```
jenkins-python-utils/
├── vars/
│   └── pythonUtils.groovy
└── README.md
```

### Implementation Details

1. The `setupPythonEnv` function should:

   - Accept parameters for Python version and virtual environment name
   - Create a virtual environment
   - Install requirements.txt
   - Return the activation command

2. The `runTests` function should:

   - Accept test directory path and coverage threshold
   - Run pytest with coverage
   - Fail the build if coverage is below threshold

3. The `buildDockerImage` function should:
   - Accept image name and tag
   - Build Docker image
   - Return the image ID

### Example Usage

```groovy
@Library('jenkins-python-utils') _

pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                script {
                    def venv = pythonUtils.setupPythonEnv(
                        pythonVersion: '3.9',
                        venvName: 'venv'
                    )
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    pythonUtils.runTests(
                        testPath: 'tests',
                        coverageThreshold: 80
                    )
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    pythonUtils.buildDockerImage(
                        imageName: 'myapp',
                        tag: 'latest'
                    )
                }
            }
        }
    }
}
```

### Submission Requirements

1. Git repository URL
2. Screenshot of successful pipeline run
3. Documentation of the shared library functions

---

## Assignment 3: Advanced Shared Library with Pipeline Templates

### Objective

Create an advanced shared library that implements reusable pipeline templates for different deployment strategies.

### Requirements

1. Create a new Git repository named `jenkins-pipeline-templates`
2. Implement the following components:
   - Pipeline templates for different deployment strategies
   - Environment configuration management
   - Notification system
   - Health check utilities

### Expected Structure

```
jenkins-pipeline-templates/
├── vars/
│   ├── deploymentTemplates.groovy
│   ├── environmentConfig.groovy
│   └── notificationUtils.groovy
├── src/
│   └── org/
│       └── example/
│           ├── DeploymentStrategy.groovy
│           ├── Environment.groovy
│           └── HealthCheck.groovy
└── README.md
```

### Implementation Details

1. Create deployment strategy templates:

   - Blue-Green deployment
   - Canary deployment
   - Rolling update
     Each template should handle:
   - Version management
   - Traffic switching
   - Rollback procedures
   - Health checks

2. Environment configuration management:

   - Load environment-specific variables
   - Manage secrets
   - Handle different deployment targets
   - Support multiple cloud providers

3. Notification system:

   - Slack notifications
   - Email alerts
   - Custom webhook support
   - Build status reporting

4. Health check utilities:
   - Application health monitoring
   - Database connectivity checks
   - API endpoint validation
   - Performance metrics collection

### Example Usage

```groovy
@Library('jenkins-pipeline-templates') _

// Load environment configuration
def envConfig = environmentConfig.load('production')

// Create deployment pipeline
deploymentTemplates.blueGreen(
    application: 'myapp',
    version: '1.0.0',
    environment: envConfig,
    healthCheck: {
        // Custom health check configuration
        timeout: 300,
        interval: 10,
        retries: 3
    },
    notifications: {
        slack: '#deployments',
        email: 'team@example.com'
    }
)
```

### Advanced Features to Implement

1. **Deployment Strategy Class**

```groovy
class DeploymentStrategy {
    def execute() {
        // Implementation
    }

    def rollback() {
        // Rollback implementation
    }

    def healthCheck() {
        // Health check implementation
    }
}
```

2. **Environment Configuration**

```groovy
class Environment {
    def loadConfig() {
        // Load environment configuration
    }

    def validateConfig() {
        // Validate configuration
    }

    def getSecrets() {
        // Retrieve secrets
    }
}
```

3. **Health Check Utility**

```groovy
class HealthCheck {
    def checkEndpoint() {
        // Check API endpoint
    }

    def checkDatabase() {
        // Check database connection
    }

    def checkPerformance() {
        // Check performance metrics
    }
}
```

### Submission Requirements

1. Git repository URL
2. Documentation including:
   - Architecture overview
   - Usage examples
   - Configuration guide
3. Screenshots of:
   - Successful pipeline runs
   - Different deployment strategies
   - Notification examples
4. Unit tests for the shared library

### Challenge tasks

1. Implement additional deployment strategies
2. Add support for multiple cloud providers
3. Create a web interface for configuration
4. Implement automated testing for the shared library

## Submission Deadline

Submit your assignments by the end of the week. Include all required documentation and screenshots in your repository.
