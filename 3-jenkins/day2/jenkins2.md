# Jenkins Pipelines and Groovy - Day 2

## Table of Contents

- [Introduction to Jenkins Pipelines](#introduction-to-jenkins-pipelines)
- [Groovy Fundamentals for Jenkins](#groovy-fundamentals-for-jenkins)
- [Declarative Pipeline](#declarative-pipeline)
- [Scripted Pipeline](#scripted-pipeline)
- [Practical Examples](#practical-examples)

## Introduction to Jenkins Pipelines

### Pipeline Concepts

Jenkins Pipeline is a suite of plugins that supports implementing and integrating continuous delivery pipelines into Jenkins. A pipeline is a collection of steps or jobs that helps you build, test and deploy applications.

Key benefits:

- Code: Pipelines are implemented in code and typically checked into source control
- Durable: Pipelines can survive both planned and unplanned restarts of the Jenkins controller
- Pausable: Pipelines can optionally stop and wait for human input or approval
- Versatile: Pipelines support complex real-world CD requirements
- Extensible: Pipeline plugin supports custom extensions and multiple options for integration

### Pipeline Syntax

Jenkins Pipeline provides two syntax options:

1. Declarative Pipeline
2. Scripted Pipeline

Basic structure of a Jenkinsfile:

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

### Pipeline Structure

A typical Jenkins Pipeline consists of:

- `agent`: Specifies where the pipeline will execute
- `stages`: Contains all the stages in the pipeline
- `steps`: Contains all the steps to be executed in a stage
- `post`: Contains actions to be run after stages completion

In Jenkins, pipelines can be defined using either Declarative or Scripted syntax. Here's the difference:

1. **Declarative Pipelines**:

   - **Structured and Simplified**: Declarative pipelines provide a more structured and simplified way to define your pipeline. They use a predefined set of conventions and are easier to read and maintain.
   - **Block-Based**: They are defined using a specific block structure, such as `pipeline`, `agent`, `stages`, and `steps`.
   - **Limited Flexibility**: While they are easier for beginners and for standard pipeline tasks, they offer less flexibility for complex logic compared to scripted pipelines.

2. **Scripted Pipelines**:

   - **Flexible and Powerful**: Scripted pipelines provide more flexibility and control over the pipeline’s behavior. They allow you to write complex logic using Groovy scripting.
   - **Script-Based**: They are defined using Groovy code, which means you have to manage the syntax and structure yourself.
   - **More Control**: Scripted pipelines are ideal for complex workflows that require custom logic and conditions.

In summary, Declarative pipelines are simpler and more structured, while Scripted pipelines offer greater flexibility for complex scenarios.

## Groovy Fundamentals for Jenkins

### Basic Groovy Syntax

Groovy is a versatile and dynamic programming language for the Java platform. It integrates smoothly with Java, allowing you to use Java libraries and frameworks. Groovy is known for its concise syntax, which reduces boilerplate code and enhances productivity. It's often used for scripting, testing, and building applications. The language supports both static and dynamic typing, making it flexible for different development styles. Overall, Groovy offers a powerful way to enhance Java development with more expressive and flexible code.

Groovy is primarily an interpreted language, which means that code is executed directly by the Groovy interpreter without the need for a separate compilation step. However, Groovy can also be compiled to Java bytecode, allowing it to run on the Java Virtual Machine (JVM). This gives developers the flexibility to choose between immediate execution and optimized performance.

Here are some basic syntax examples:

```groovy
// Variables
def name = 'Jenkins'
String version = '2.0'
int buildNumber = 42

// String interpolation
println "Building ${name} version ${version}"

// Lists
def tools = ['git', 'maven', 'gradle']
tools.each { tool ->
    println "Using ${tool}"
}

// Maps
def config = [
    server: 'production',
    port: 8080
]
```

### Variables and Data Types

Common data types in Groovy:

```groovy
// Numbers
def count = 10
def price = 99.99

// Strings
def singleQuoted = 'Hello'
def doubleQuoted = "Hello ${name}"

// Lists
def list = [1, 2, 3, 4]

// Maps
def map = [name: 'Jenkins', type: 'CI/CD']

// Boolean
def isValid = true
```

### Control Structures

```groovy
// If-else
if (buildStatus == 'SUCCESS') {
    println 'Build passed'
} else {
    println 'Build failed'
}

// For loop
for (int i = 0; i < 5; i++) {
    println "Iteration ${i}"
}

// While loop
def counter = 0
while (counter < 3) {
    println counter
    counter++
}

// Switch statement
switch(buildType) {
    case 'debug':
        println 'Debug build'
        break
    case 'release':
        println 'Release build'
        break
    default:
        println 'Unknown build type'
}
```

### Functions and Closures

```groovy
// Function definition
def greet(name) {
    return "Hello, ${name}!"
}

// Closure example
def multiply = { a, b ->
    return a * b
}

// Using closures in collections
def numbers = [1, 2, 3, 4]
// def doubled = numbers.collect { it * 2 }
def doubled = numbers.collect { n -> n * 2 }
// JS equivalent
let doubled = numbers.map( n -> n*2 )
```

## Declarative Pipeline

### Pipeline Structure

A complete declarative pipeline structure for a Python Flask application:

```groovy
pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.8'
        FLASK_ENV = 'development'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/
                '''
            }
        }

        stage('Code Quality') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 app/
                    pylint app/
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    . venv/bin/activate
                    gunicorn app:app
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

### Stages and Steps

Stages represent different phases in your pipeline:

- Each stage must have a unique name
- Steps define the actual work to be performed
- Steps can include shell commands, Jenkins plugins, or other Pipeline steps

### Environment Variables

Environment variables can be set at different levels:

```groovy
pipeline {
    environment {
        // Global variables
        APP_NAME = 'flask-app'
        APP_VERSION = '1.0.0'
    }

    stages {
        stage('Build') {
            environment {
                // Stage-specific variables
                BUILD_FLAGS = '--no-cache'
            }
            steps {
                echo "Building ${APP_NAME} version ${APP_VERSION}"
            }
        }
    }
}
```

### Post-build Actions

Post-build actions are executed after all stages complete:

```groovy
post {
    always {
        // Always executed
        cleanWs()
    }
    success {
        // Executed only on success
        emailext subject: 'Build Successful',
                 body: 'Your build has completed successfully',
                 to: 'team@example.com'
    }
    failure {
        // Executed only on failure
        emailext subject: 'Build Failed',
                 body: 'Your build has failed',
                 to: 'team@example.com'
    }
}
```

## Scripted Pipeline

### Advanced Groovy Scripting

Scripted Pipeline provides more flexibility using Groovy:

```groovy
node {
    def buildVersion = ''

    try {
        stage('Prepare') {
            buildVersion = sh(script: 'python setup.py --version', returnStdout: true).trim()
        }

        stage('Build') {
            parallel (
                'Unit Tests': {
                    sh 'python -m pytest tests/unit'
                },
                'Integration Tests': {
                    sh 'python -m pytest tests/integration'
                }
            )
        }
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        throw e
    }
}
```

### Custom Functions

Creating reusable functions in Scripted Pipeline:

```groovy
def runPythonTests(String testType) {
    sh """
        . venv/bin/activate
        python -m pytest tests/${testType}
    """
}

node {
    stage('Test') {
        runPythonTests('unit')
        runPythonTests('integration')
    }
}
```

### Error Handling

Proper error handling in Scripted Pipeline:

```groovy
node {
    try {
        stage('Deploy') {
            sh 'python deploy.py'
        }
    } catch (Exception e) {
        // Handle specific errors
        if (e.getMessage().contains('Connection refused')) {
            echo 'Deployment server is not responding'
        } else {
            echo 'Unknown deployment error occurred'
        }
        currentBuild.result = 'FAILURE'
        throw e
    } finally {
        // Cleanup
        sh 'python cleanup.py'
    }
}
```

### Shared Libraries

Creating and using shared libraries:

```groovy
// In your shared library (src/org/example/Pipeline.groovy)
package org.example

class Pipeline {
    static def deployFlaskApp(script) {
        script.sh '''
            . venv/bin/activate
            gunicorn app:app
        '''
    }
}

// In your Jenkinsfile
@Library('my-shared-library') _

node {
    stage('Deploy') {
        org.example.Pipeline.deployFlaskApp(this)
    }
}
```

## Practical Examples

### Example 1: Basic Flask Application Pipeline

```groovy
pipeline {
    agent any

    environment {
        FLASK_ENV = 'development'
        FLASK_APP = 'app.py'
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    . venv/bin/activate
                    gunicorn app:app -b 0.0.0.0:8000
                '''
            }
        }
    }
}
```

### Example 2: Flask REST API with Multiple Environments

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Deployment Environment')
    }

    environment {
        APP_NAME = 'flask-rest-api'
    }

    stages {
        stage('Validate') {
            steps {
                script {
                    if (params.ENVIRONMENT == 'prod') {
                        input message: 'Deploy to production?', ok: 'Deploy'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh """
                    . venv/bin/activate
                    export FLASK_ENV=${params.ENVIRONMENT}
                    python deploy.py --env ${params.ENVIRONMENT}
                """
            }
        }
    }
}
```

These examples demonstrate how to create pipelines for Python Flask applications, incorporating best practices for testing, deployment, and environment management. Remember to adapt these examples based on your specific requirements and infrastructure setup.
