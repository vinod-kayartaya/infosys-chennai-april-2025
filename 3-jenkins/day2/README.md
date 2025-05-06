# Day 2: Jenkins Pipelines and Groovy

## Introduction to Jenkins Pipelines

### Pipeline Concepts

Jenkins Pipeline is a suite of plugins that supports implementing and integrating continuous delivery pipelines into Jenkins. It provides an extensible set of tools for modeling simple-to-complex delivery pipelines "as code."

**Key Concepts:**

- Pipeline as Code
- Declarative vs Scripted Pipelines
- Pipeline Stages and Steps
- Pipeline Visualization
- Pipeline Reusability

### Pipeline Syntax

Jenkins Pipeline provides two syntax options:

1. **Declarative Pipeline**: A more structured and opinionated syntax
2. **Scripted Pipeline**: A more flexible and powerful syntax based on Groovy

**Basic Pipeline Structure:**

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                // Build steps
            }
        }
        stage('Test') {
            steps {
                // Test steps
            }
        }
        stage('Deploy') {
            steps {
                // Deploy steps
            }
        }
    }
}
```

## Groovy Fundamentals for Jenkins

### Basic Groovy Syntax

Groovy is a powerful, optionally typed and dynamic language for the Java platform. It's the foundation of Jenkins Pipeline scripting.

**Key Features:**

- Dynamic typing
- Closures
- String interpolation
- List and Map operations
- Regular expressions

### Variables and Data Types

```groovy
// Variable declaration
def name = "Jenkins"
String version = "2.387.1"
int port = 8080
boolean isRunning = true

// Collections
def list = [1, 2, 3, 4, 5]
def map = [name: "Jenkins", version: "2.387.1"]
```

### Control Structures

```groovy
// If-else
if (condition) {
    // code
} else {
    // code
}

// Switch
switch (value) {
    case 1:
        // code
        break
    default:
        // code
}

// Loops
for (item in items) {
    // code
}
```

### Functions and Closures

```groovy
// Function definition
def greet(name) {
    return "Hello, ${name}!"
}

// Closure
def closure = { param ->
    println "Parameter: ${param}"
}
```

## Declarative Pipeline

### Pipeline Structure

```groovy
pipeline {
    agent any
    environment {
        // Environment variables
    }
    parameters {
        // Build parameters
    }
    stages {
        // Pipeline stages
    }
    post {
        // Post-build actions
    }
}
```

### Stages and Steps

- **Stages**: Logical divisions of the pipeline
- **Steps**: Individual tasks within stages
- **Parallel Stages**: Concurrent execution
- **Matrix Stages**: Multi-configuration builds

### Environment Variables

```groovy
environment {
    PATH = "/usr/local/bin:${env.PATH}"
    BUILD_NUMBER = "${env.BUILD_NUMBER}"
    CUSTOM_VAR = "value"
}
```

### Post-build Actions

```groovy
post {
    always {
        // Always execute
    }
    success {
        // On success
    }
    failure {
        // On failure
    }
    unstable {
        // On unstable
    }
}
```

## Scripted Pipeline

### Advanced Groovy Scripting

- Custom functions
- Shared libraries
- Error handling
- Dynamic pipeline generation

### Custom Functions

```groovy
def buildProject() {
    // Build logic
}

def runTests() {
    // Test logic
}

node {
    buildProject()
    runTests()
}
```

### Error Handling

```groovy
try {
    // Risky operation
} catch (Exception e) {
    // Error handling
} finally {
    // Cleanup
}
```

### Shared Libraries

- Creating shared libraries
- Importing shared libraries
- Using shared functions
- Version control integration

## Lab Exercise: Creating and Managing Pipelines

### Exercise 1: Basic Pipeline

1. Create a new pipeline project
2. Write a basic declarative pipeline
3. Add build, test, and deploy stages
4. Run the pipeline

### Exercise 2: Advanced Pipeline

1. Create a scripted pipeline
2. Implement custom functions
3. Add error handling
4. Use shared libraries

### Exercise 3: Pipeline Best Practices

1. Implement parallel stages
2. Add environment variables
3. Configure post-build actions
4. Optimize pipeline performance

## Additional Resources

- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Groovy Documentation](https://groovy-lang.org/documentation.html)
- [Jenkins Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
- [Pipeline Best Practices](https://www.jenkins.io/doc/book/pipeline/best-practices/)

## Next Steps

- Review the concepts covered in Day 2
- Complete all lab exercises
- Prepare for Day 3: Advanced Pipeline Features and Deployment
