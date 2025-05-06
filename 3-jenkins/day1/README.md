# Day 1: Jenkins Fundamentals and Architecture

## Introduction to CI/CD

### Continuous Integration (CI)

Continuous Integration is a development practice where developers frequently integrate their code into a shared repository. Each integration is automatically verified by building the application and running automated tests.

**Key Benefits:**

- Early bug detection
- Reduced integration problems
- Faster feedback
- Improved code quality
- Better team collaboration

### Continuous Delivery/Deployment (CD)

Continuous Delivery is the practice of automatically preparing code changes for release to production, while Continuous Deployment automatically deploys every change that passes all tests.

**Key Benefits:**

- Faster time to market
- Reduced deployment risk
- Improved product quality
- Better customer satisfaction
- Increased team productivity

## Jenkins Architecture

### Controller/Agent Architecture

Jenkins follows a distributed architecture with two main components:

- **Controller**: The main Jenkins server that manages the build environment
- **Agent**: Worker nodes that execute the actual build jobs

**Benefits:**

- Scalability
- Resource optimization
- Parallel execution
- Load distribution

### Master-Slave Configuration

The master-slave configuration allows Jenkins to distribute workload across multiple machines:

- **Master**: Manages the Jenkins environment and job configuration
- **Slave**: Executes the actual build jobs

**Key Features:**

- Dynamic agent provisioning
- Resource management
- Build isolation
- Platform independence

### Security Considerations

- User authentication and authorization
- Role-based access control
- Credential management
- Secure communication
- Plugin security

## Jenkins Installation and Setup

### Installation Methods

1. **Standalone Installation**

   - Download and run the Jenkins WAR file
   - Use the native package manager
   - Docker container deployment

2. **System Requirements**
   - Java Development Kit (JDK)
   - Minimum 4GB RAM
   - 50GB disk space
   - Network connectivity

### Initial Configuration

1. **First-time Setup**

   - Unlock Jenkins
   - Install recommended plugins
   - Create admin user
   - Configure system settings

2. **System Configuration**
   - Global tool configuration
   - Environment variables
   - Security settings
   - Email notifications

### Plugin Management

- Installing plugins
- Updating plugins
- Managing plugin dependencies
- Troubleshooting plugin issues

### User Management

- Creating users
- Assigning roles
- Managing permissions
- Security best practices

## Basic Jenkins Jobs

### Freestyle Projects

Freestyle projects are the most flexible and configurable option for building software projects.

**Features:**

- Build steps configuration
- Build triggers
- Build parameters
- Post-build actions
- Workspace management

### Pipeline Projects

Pipeline projects use a Jenkinsfile to define the entire build process as code.

**Benefits:**

- Version control
- Code review
- Reusability
- Maintainability

### Job Configuration

- Source code management
- Build triggers
- Build environment
- Build steps
- Post-build actions

### Build Triggers

- Manual triggers
- SCM polling
- Time-based triggers
- Remote triggers
- Dependency triggers

### Build Parameters

- String parameters
- Choice parameters
- Boolean parameters
- File parameters
- Password parameters

## Lab Exercise: Setting up Jenkins and Creating Basic Jobs

### Exercise 1: Jenkins Installation

1. Install Jenkins on your local machine
2. Complete the initial setup
3. Install recommended plugins
4. Create an admin user

### Exercise 2: Basic Job Creation

1. Create a freestyle project
2. Configure source code management
3. Set up build steps
4. Configure post-build actions
5. Run the build

### Exercise 3: Pipeline Project

1. Create a pipeline project
2. Write a basic Jenkinsfile
3. Configure build triggers
4. Run the pipeline

## Additional Resources

- [Jenkins Official Documentation](https://www.jenkins.io/doc/)
- [Jenkins User Handbook](https://www.jenkins.io/doc/book/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins Security Best Practices](https://www.jenkins.io/doc/book/security/)

## Next Steps

- Review the concepts covered in Day 1
- Complete all lab exercises
- Prepare for Day 2: Jenkins Pipelines and Groovy
