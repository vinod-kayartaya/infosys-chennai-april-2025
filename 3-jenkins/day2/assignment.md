# Jenkins Pipeline Lab Assignment: Flask Application CI/CD

## Overview

In this lab assignment, you will create and manage Jenkins pipelines for a Flask-based Python application. You will implement various pipeline concepts covered in the course materials, including declarative and scripted pipelines, environment variables, stages, and post-build actions.

## Prerequisites

- Jenkins server up and running
- Python 3.8 or higher installed on Jenkins server
- Git installed on Jenkins server
- Basic understanding of Python and Flask

## Project Setup

1. Create a new directory for your Flask project
2. Initialize a Git repository
3. Create a basic Flask application with the following structure:

```
flask-app/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── models.py
├── tests/
│   ├── __init__.py
│   └── test_routes.py
├── requirements.txt
└── README.md
```

## Task 1: Basic Declarative Pipeline

Create a basic declarative pipeline that performs the following tasks:

1. Checkout the code from your Git repository
2. Set up a Python virtual environment
3. Install dependencies from requirements.txt
4. Run basic unit tests
5. Add appropriate post-build actions

**Requirements:**

- Use declarative pipeline syntax
- Include environment variables for Python version and Flask environment
- Add proper error handling
- Include post-build actions for success and failure scenarios

## Task 2: Advanced Declarative Pipeline

Enhance your pipeline by adding the following features:

1. Add a code quality check stage using flake8
2. Implement parallel test execution for unit and integration tests
3. Add a deployment stage that runs the Flask application
4. Include build parameters for different environments (development, staging)

**Requirements:**

- Use matrix stages for different Python versions
- Implement parallel test execution
- Add input step for production deployment approval
- Include proper error handling and notifications

## Task 3: Scripted Pipeline

Create a scripted pipeline version of your application that includes:

1. Custom functions for common operations
2. Dynamic stage generation based on test files
3. Advanced error handling with custom error messages
4. Shared library implementation for common functions

**Requirements:**

- Convert the declarative pipeline to scripted syntax
- Create reusable functions for setup, testing, and deployment
- Implement proper error handling with custom messages
- Use Groovy closures for test execution

## Task 4: Pipeline Optimization

Optimize your pipeline by implementing:

1. Caching of Python virtual environment
2. Parallel execution of different test suites
3. Conditional stage execution based on file changes
4. Performance monitoring and reporting

**Requirements:**

- Implement workspace cleanup
- Add build time tracking
- Include test coverage reporting
- Optimize pipeline execution time

## Task 5: Pipeline Best Practices

Implement the following best practices in your pipeline:

1. Add proper logging and documentation
2. Implement security best practices
3. Add pipeline validation
4. Create a shared library for common functions

**Requirements:**

- Add detailed logging for each stage
- Implement proper error handling and reporting
- Create a shared library for common functions
- Add pipeline validation checks

## More challenges

1. Implement email notifications for pipeline status
2. Add performance metrics collection
3. Create a dashboard for pipeline statistics
4. Implement automated rollback on deployment failure

## Resources

- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Groovy Documentation](https://groovy-lang.org/documentation.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Testing Documentation](https://docs.python.org/3/library/unittest.html)

## Note

- Do not use Docker in your implementation
- Follow Jenkins pipeline best practices
- Document your implementation thoroughly
