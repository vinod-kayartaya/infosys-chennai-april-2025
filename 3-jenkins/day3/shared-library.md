# Creating and Using Jenkins Shared Libraries

This guide explains how to create and use Jenkins shared libraries within your project's Git repository.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Creating the Shared Library](#creating-the-shared-library)
3. [Using the Shared Library](#using-the-shared-library)
4. [Best Practices](#best-practices)

## Project Structure

A typical project structure with an embedded shared library looks like this:

```
project-root/
├── Jenkinsfile
├── src/
│   └── app/
│       ├── __init__.py
│       ├── routes.py
│       └── models.py
├── tests/
├── jenkins/
│   ├── vars/
│   │   ├── buildUtils.groovy
│   │   └── deployUtils.groovy
│   └── src/
│       └── org/
│           └── example/
│               ├── Build.groovy
│               └── Deploy.groovy
└── requirements.txt
```

## Creating the Shared Library

### 1. Create the Directory Structure

```bash
mkdir -p jenkins/vars jenkins/src/org/example
```

### 2. Create a Global Variable (vars/buildUtils.groovy)

```groovy
#!/usr/bin/env groovy

def call(Map config) {
    pipeline {
        agent any
        stages {
            stage('Setup') {
                steps {
                    script {
                        setupPythonEnv(config)
                    }
                }
            }
            stage('Test') {
                steps {
                    script {
                        runTests(config)
                    }
                }
            }
            stage('Build') {
                steps {
                    script {
                        buildDockerImage(config)
                    }
                }
            }
        }
    }
}

def setupPythonEnv(Map config) {
    sh """
        python -m venv ${config.venvName}
        . ${config.venvName}/bin/activate
        pip install -r requirements.txt
    """
}

def runTests(Map config) {
    sh """
        . ${config.venvName}/bin/activate
        pytest ${config.testPath} --cov=src --cov-report=xml
    """
}

def buildDockerImage(Map config) {
    sh """
        docker build -t ${config.imageName}:${config.tag} .
    """
}
```

### 3. Create a Class (src/org/example/Build.groovy)

```groovy
package org.example

class Build implements Serializable {
    def steps

    Build(steps) {
        this.steps = steps
    }

    def setupEnvironment(String pythonVersion, String venvName) {
        steps.sh """
            python${pythonVersion} -m venv ${venvName}
            . ${venvName}/bin/activate
            pip install -r requirements.txt
        """
    }

    def runTests(String venvName, String testPath, int coverageThreshold) {
        steps.sh """
            . ${venvName}/bin/activate
            pytest ${testPath} --cov=src --cov-report=xml
        """

        // Check coverage threshold
        def coverage = steps.readFile('coverage.xml')
        if (coverage < coverageThreshold) {
            steps.error "Test coverage below threshold: ${coverage}%"
        }
    }
}
```

## Using the Shared Library

### 1. Reference the Library in Jenkinsfile

```groovy
// Load the shared library from the project
library identifier: 'project-shared-library@main',
        retriever: modernSCM(
            [
                $class: 'GitSCMSource',
                remote: '${WORKSPACE}/.git',
                credentialsId: ''
            ]
        )

// Use the global variable
buildUtils(
    venvName: 'venv',
    testPath: 'tests',
    imageName: 'myapp',
    tag: 'latest'
)

// Or use the class
def build = new org.example.Build(this)
build.setupEnvironment('3.9', 'venv')
build.runTests('venv', 'tests', 80)
```

### 2. Configure Jenkins to Use the Library

1. Go to Jenkins Dashboard → Manage Jenkins → Configure System
2. Scroll to "Global Pipeline Libraries"
3. Add a new library:
   - Name: `project-shared-library`
   - Default version: `main`
   - Retrieval method: Modern SCM
   - Source Code Management: Git
   - Project Repository: `${WORKSPACE}/.git`
   - Credentials: (leave empty for local repository)

## Best Practices

### 1. Version Control

- Keep the shared library code in the same repository as your project
- Use branches for different versions of the library
- Tag releases for stability

### 2. Code Organization

- Use `vars/` for simple, reusable functions
- Use `src/` for complex classes and utilities
- Follow consistent naming conventions
- Document all functions and classes

### 3. Error Handling

```groovy
def safeExecute(Closure closure) {
    try {
        closure()
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        error "Operation failed: ${e.message}"
    }
}
```

### 4. Testing

- Write unit tests for your shared library code
- Test different scenarios and edge cases
- Include test coverage reporting

### 5. Documentation

- Add comments to explain complex logic
- Include usage examples
- Document parameters and return values
- Keep a changelog

## Example: Complete Pipeline with Shared Library

```groovy
// Jenkinsfile
library identifier: 'project-shared-library@main',
        retriever: modernSCM(
            [
                $class: 'GitSCMSource',
                remote: '${WORKSPACE}/.git',
                credentialsId: ''
            ]
        )

pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.9'
        VENV_NAME = 'venv'
    }

    stages {
        stage('Build and Test') {
            steps {
                script {
                    buildUtils(
                        venvName: env.VENV_NAME,
                        testPath: 'tests',
                        imageName: 'myapp',
                        tag: 'latest'
                    )
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    def deploy = new org.example.Deploy(this)
                    deploy.execute(
                        environment: 'staging',
                        version: 'latest'
                    )
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            emailext (
                subject: "Pipeline Failed: ${currentBuild.fullDisplayName}",
                body: "Check console output at ${env.BUILD_URL}",
                to: 'team@example.com'
            )
        }
    }
}
```

## Troubleshooting

### Common Issues

1. **Library Not Found**

   - Check the library identifier
   - Verify the Git repository path
   - Ensure the library is properly configured in Jenkins

2. **Permission Issues**

   - Check file permissions
   - Verify Jenkins user has access to the repository
   - Check credentials if using remote repository

3. **Version Conflicts**
   - Use specific versions or tags
   - Keep library versions in sync
   - Document version requirements

## Additional Resources

1. [Jenkins Shared Libraries Documentation](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
2. [Groovy Documentation](https://groovy-lang.org/documentation.html)
3. [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
