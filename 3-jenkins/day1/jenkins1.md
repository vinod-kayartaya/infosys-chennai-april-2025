# Jenkins Fundamentals and Architecture: A Comprehensive Tutorial

## Introduction to CI/CD

### Continuous Integration (CI) Concepts

Continuous Integration is a software development practice where developers frequently integrate their code changes into a shared repository, followed by automated builds and tests. The primary goal is to detect integration issues early in the development cycle.

#### Key Elements of Continuous Integration

1. **Frequent Code Commits**: Developers commit code to a centralized repository multiple times per day.

   *Example:* 
   ```
   # Developer workflow
   git pull origin develop  # Get latest changes
   # Make code changes
   git add .
   git commit -m "Add user authentication feature"
   git push origin develop
   ```

2. **Automated Building**: Every commit triggers an automated build process.

   *Example of Jenkins build trigger configuration:*
   ```groovy
   triggers {
       githubPush()  // Trigger build when code is pushed to GitHub
       pollSCM('H/15 * * * *')  // Poll repository every 15 minutes
   }
   ```

3. **Automated Testing**: Comprehensive testing is performed on each build.

   *Types of tests typically included:*
   - Unit tests
   - Integration tests
   - Functional tests
   - API tests
   - UI tests

4. **Fast Feedback**: Developers receive feedback on their changes quickly.

   *Example feedback workflow:*
   - Developer pushes code
   - Jenkins detects changes and initiates build (typically within 1-2 minutes)
   - Build and tests run (5-15 minutes depending on project complexity)
   - Results sent via email/Slack notifications

#### CI Benefits

- **Early Bug Detection**: Issues are found and fixed early in the development cycle.
- **Reduced Integration Problems**: Frequent integration minimizes merge conflicts.
- **Improved Code Quality**: Regular testing ensures quality code.
- **Increased Visibility**: Team members can see the status of builds and tests.

### Continuous Delivery/Deployment (CD) Concepts

Continuous Delivery extends CI by ensuring that code can be rapidly and safely deployed to production at any time. Continuous Deployment takes this a step further by automatically deploying every change that passes all tests to production.

#### Continuous Delivery vs. Continuous Deployment

**Continuous Delivery:**
- Code is always in a deployable state
- Deployment to production is a manual decision
- Changes go through staging environments before production

*Example Continuous Delivery Pipeline:*
```
Build → Unit Tests → Integration Tests → User Acceptance Testing → Manual Approval → Production Deployment
```

**Continuous Deployment:**
- Every change that passes automated tests is automatically deployed to production
- No manual intervention required
- Requires high confidence in test coverage

*Example Continuous Deployment Pipeline:*
```
Build → Unit Tests → Integration Tests → Automated Performance Tests → Production Deployment
```

#### CD Benefits

- **Faster Time to Market**: Features and fixes reach users quickly.
- **Lower Deployment Risk**: Smaller, incremental changes are less risky.
- **User Feedback**: Get user feedback on new features sooner.
- **Reduced Manual Overhead**: Automation reduces human error.

### CI/CD Best Practices

1. **Maintain a Single Source Repository**
   - All code should be stored in a version control system like Git
   - Use branching strategies like GitFlow or trunk-based development

   *Example GitFlow workflow:*
   ```
   master (production-ready code)
   ├── develop (integration branch)
       ├── feature/user-auth (feature branch)
       ├── feature/payment-processing (feature branch)
   ```

2. **Automate the Build Process**
   - Build should be self-testing
   - Build should be executable with a single command

   *Example Maven build command:*
   ```bash
   mvn clean package
   ```

3. **Make the Build Fast**
   - Keep build times under 10 minutes if possible
   - Parallelize tests
   - Use incremental builds

4. **Test in a Production-like Environment**
   - Use containers or VMs to replicate production
   - Include infrastructure as code

   *Example Docker-based testing environment:*
   ```yaml
   # docker-compose.yml
   version: '3'
   services:
     app:
       build: .
       ports:
         - "8080:8080"
     db:
       image: postgres:13
       environment:
         POSTGRES_USER: testuser
         POSTGRES_PASSWORD: testpassword
         POSTGRES_DB: testdb
   ```

5. **Make Deployments Easy**
   - Automate deployment processes
   - Implement feature flags for risk mitigation

   *Example feature flag implementation:*
   ```java
   if (FeatureFlags.isEnabled("new-payment-system")) {
       // New payment processing code
   } else {
       // Old payment processing code
   }
   ```

6. **Everyone is Responsible**
   - Entire team commits to keeping the build passing
   - Fix broken builds immediately

7. **Implement Comprehensive Monitoring**
   - Monitor application performance
   - Track user behavior and business metrics

   *Example monitoring setup with Prometheus and Grafana:*
   ```yaml
   # prometheus.yml
   scrape_configs:
     - job_name: 'jenkins'
       static_configs:
         - targets: ['jenkins:8080']
   ```

## Jenkins Architecture

### Controller/Agent Architecture

Jenkins uses a controller-agent (formerly known as master-slave) architecture to distribute build and test workloads.

#### Controller (Master)

The Jenkins controller is responsible for:
- Scheduling build jobs
- Dispatching builds to agents
- Monitoring agents and recording build results
- Presenting the user interface
- Storing and serving build artifacts

*Typical controller specifications:*
- 4+ CPU cores
- 8+ GB RAM
- 50+ GB disk space (SSD preferred)
- Stable network connection

#### Agents (Slaves)

Agents are the worker nodes that execute the builds assigned by the controller.

*Types of agents:*

1. **Permanent Agents**: Long-running agents that are always available
   
   *Example configuration in Jenkins UI:*
   - Name: linux-agent-01
   - Number of executors: 4
   - Remote root directory: /var/jenkins
   - Labels: linux, docker, maven
   - Launch method: SSH
   - Host: 192.168.1.100

2. **Cloud Agents**: Dynamically provisioned when needed (e.g., using Docker, Kubernetes, AWS EC2)

   *Example Jenkins Kubernetes cloud configuration:*
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     labels:
       jenkins-agent: "true"
   spec:
     containers:
     - name: jnlp
       image: jenkins/inbound-agent:4.11.2-4
       resources:
         requests:
           memory: "512Mi"
           cpu: "500m"
         limits:
           memory: "1Gi"
           cpu: "1"
   ```

#### Communication Protocol

The controller and agents communicate using the Jenkins Remote Protocol:
- Bidirectional TCP/IP connection
- Encrypted with TLS
- Authentication using pre-shared keys or certificates

### Master-Slave Configuration

Setting up a master-slave configuration involves:

1. **Install Jenkins Controller**
   ```bash
   # On Ubuntu/Debian
   wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
   sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
   sudo apt-get update
   sudo apt-get install jenkins
   ```

2. **Configure JNLP Port** (if needed)
   
   Edit `/etc/default/jenkins` and add:
   ```bash
   JENKINS_ARGS="$JENKINS_ARGS --httpPort=8080 --httpsPort=-1 --slaveAgentPort=50000"
   ```

3. **Set Up Agent Node**

   *Via Jenkins UI:*
   - Navigate to "Manage Jenkins" → "Manage Nodes and Clouds" → "New Node"
   - Enter node name and select "Permanent Agent"
   - Configure connection details (SSH, JNLP, etc.)

   *Example SSH agent configuration:*
   - Host: 192.168.1.101
   - Credentials: (Add SSH private key)
   - Remote root directory: /var/jenkins_home
   - Launch method: Launch agent via SSH
   - Custom WorkDir path: /var/jenkins_home

4. **Connect Agent to Controller**

   *For SSH agents:*
   - The controller will automatically attempt to connect

   *For JNLP agents:*
   - On the agent machine, download the agent JAR:
     ```bash
     wget http://jenkins-master:8080/jnlpJars/agent.jar
     ```
   - Launch the agent:
     ```bash
     java -jar agent.jar -jnlpUrl http://jenkins-master:8080/computer/agent-name/slave-agent.jnlp -secret <secret-key>
     ```

### Distributed Builds

Distributed builds allow Jenkins to run different jobs or parts of a job across multiple agents, increasing throughput and efficiency.

#### Build Distribution Strategies

1. **Label-based Distribution**
   
   Jobs are assigned to agents based on labels that identify capabilities or environments.

   *Example job configuration:*
   ```groovy
   pipeline {
       agent {
           label 'linux && docker'  // Run on any agent with both 'linux' and 'docker' labels
       }
       stages {
           // Job stages
       }
   }
   ```

2. **Load Balancing**
   
   Jenkins automatically distributes builds to idle agents.

   *Configure in "Manage Jenkins" → "Configure System" → "# of executors"*

3. **Matrix Builds**
   
   Run the same job with different configurations across multiple agents.

   *Example matrix build configuration:*
   ```groovy
   matrix {
       axes {
           axis {
               name 'PLATFORM'
               values 'linux', 'windows', 'mac'
           }
           axis {
               name 'BROWSER'
               values 'chrome', 'firefox', 'safari'
           }
       }
       stages {
           stage('Test') {
               steps {
                   sh "run-tests.sh ${PLATFORM} ${BROWSER}"
               }
           }
       }
   }
   ```

#### Benefits of Distributed Builds

- **Scalability**: Easily add more agents to handle increased workload
- **Platform Coverage**: Test on multiple operating systems/environments
- **Resource Optimization**: Specialized agents for specific tasks
- **Parallel Execution**: Run multiple builds simultaneously

### Security Considerations

Jenkins security is critical because it often has access to sensitive codebases and deployment environments.

#### Authentication

1. **Jenkins Internal User Database**
   
   Configure in "Manage Jenkins" → "Configure Global Security"
   
   *Best practices:*
   - Use strong passwords
   - Implement password rotation
   - Limit admin accounts

2. **LDAP Integration**
   
   *Example LDAP configuration:*
   ```
   Server: ldap://ldap.example.com:389
   Root DN: dc=example,dc=com
   User search base: ou=users
   User search filter: uid={0}
   Group search base: ou=groups
   Group search filter: cn={0}
   ```

3. **Single Sign-On (SSO)**
   
   Using plugins for OAuth, SAML, or other SSO providers.
   
   *Example Google OAuth configuration:*
   1. Create OAuth credentials in Google Cloud Console
   2. Install "Google Login Plugin" in Jenkins
   3. Configure client ID and secret in Jenkins

#### Authorization

1. **Matrix-based Security**
   
   Grant specific permissions to specific users or groups.
   
   *Common permission patterns:*
   - Admins: Overall/Administer
   - Developers: Job/Build, Job/Read, Job/Workspace
   - Testers: Job/Read, Job/Workspace

2. **Role-based Authorization Strategy**
   
   Create roles with specific permissions and assign users to roles.
   
   *Example roles:*
   - Admin: full access
   - Developer: create/configure/build jobs
   - Viewer: read-only access

3. **Project-based Matrix Authorization**
   
   Assign permissions at the project level.
   
   *Example:*
   - Team A has full access to Project A jobs
   - Team B has full access to Project B jobs
   - Both teams have read-only access to each other's projects

#### Agent Security

1. **Controller-Agent Security**
   
   *Best practices:*
   - Use encrypted connections (TLS)
   - Use agent-specific credentials
   - Implement firewall rules to restrict access

2. **Agent Isolation**
   
   *Methods:*
   - Run agents in containers (Docker/Kubernetes)
   - Use different user accounts for different agents
   - Clean workspaces between builds

   *Example Docker agent with workspace cleaning:*
   ```groovy
   pipeline {
       agent {
           docker {
               image 'maven:3.8.5-openjdk-11'
               args '-v $HOME/.m2:/root/.m2'
           }
       }
       options {
           cleanWs()  // Clean workspace before and after build
       }
       stages {
           // Job stages
       }
   }
   ```

#### Credential Management

Jenkins provides a credentials system to securely store and use authentication information.

1. **Types of Credentials**
   - Username/password
   - SSH keys
   - Secret text (API tokens)
   - Certificates
   - Docker host certificates

2. **Credential Scopes**
   - Global: Available to all jobs
   - System: Available for system administration
   - Project: Limited to specific jobs

3. **Using Credentials in Pipeline**

   *Example accessing credentials in a pipeline:*
   ```groovy
   pipeline {
       agent any
       stages {
           stage('Deploy') {
               steps {
                   withCredentials([string(credentialsId: 'api-token', variable: 'API_TOKEN')]) {
                       sh 'curl -H "Authorization: Bearer $API_TOKEN" https://api.example.com/deploy'
                   }
               }
           }
       }
   }
   ```

## Jenkins Installation and Setup

### Installation Methods

Jenkins can be installed using various methods depending on your operating system and requirements.

#### 1. WAR File Installation

The most portable method that works across platforms:

```bash
# Download latest stable Jenkins WAR
wget https://get.jenkins.io/war-stable/latest/jenkins.war

# Run Jenkins
java -jar jenkins.war --httpPort=8080
```

*Pros:*
- Simple to set up
- Works on any system with Java
- Easy to upgrade

*Cons:*
- Manual setup of service/daemon
- No automatic updates

#### 2. Package Manager Installation

**Ubuntu/Debian:**

```bash
# Add the Jenkins repository key
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -

# Add the Jenkins repository to sources
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

# Update package index and install Jenkins
sudo apt-get update
sudo apt-get install jenkins
```

**Red Hat/CentOS:**

```bash
# Add Jenkins repository
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key

# Install Jenkins
sudo yum install jenkins
```

*Pros:*
- Installs as a system service
- Includes init scripts
- Can be updated with package manager

*Cons:*
- Less portable
- Tied to system package management

#### 3. Docker Installation

```bash
# Pull Jenkins LTS image
docker pull jenkins/jenkins:lts

# Run Jenkins container
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  --name jenkins jenkins/jenkins:lts
```

*Advanced Docker setup with custom network and persistent volumes:*
```bash
# Create a network for Jenkins
docker network create jenkins-network

# Create volumes for Jenkins data
docker volume create jenkins-data
docker volume create jenkins-docker-certs

# Run Jenkins with Docker support
docker run -d --name jenkins \
  --network jenkins-network \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins-data:/var/jenkins_home \
  -v jenkins-docker-certs:/certs/client:ro \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --restart unless-stopped \
  jenkins/jenkins:lts
```

*Pros:*
- Isolated environment
- Consistent across platforms
- Easy to upgrade or rollback
- Can be part of Docker Compose setup

*Cons:*
- Requires Docker knowledge
- Extra configuration for persistent storage

#### 4. Kubernetes Installation

Using Helm chart:

```bash
# Add Jenkins Helm repository
helm repo add jenkins https://charts.jenkins.io
helm repo update

# Create a persistent volume claim
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: jenkins-pvc
  namespace: jenkins
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
EOF

# Install Jenkins
helm install jenkins jenkins/jenkins \
  --namespace jenkins \
  --create-namespace \
  --set persistence.existingClaim=jenkins-pvc
```

*Pros:*
- Highly available
- Scalable
- Cloud-native deployment
- Automatic recovery

*Cons:*
- Complex setup
- Requires Kubernetes knowledge

### Initial Configuration

After installation, Jenkins requires some initial configuration to make it ready for use.

#### 1. Unlocking Jenkins

When you first access Jenkins (typically at http://localhost:8080), you'll be prompted to unlock it:

1. Find the initial admin password:
   ```bash
   # For standard installation
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   
   # For Docker installation
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```

2. Enter the password in the web interface

#### 2. Plugin Installation

After unlocking, you'll be asked to install plugins:

1. Choose either:
   - **Install suggested plugins**: Quick start with common plugins
   - **Select plugins to install**: Customized setup

*Recommended base plugin set:*
- Git integration
- Pipeline
- Folders
- Credentials
- Build timeout
- Timestamper
- Workspace cleanup
- Pipeline stage view
- SSH Build Agents

#### 3. Creating Admin User

After plugin installation, create your admin user:
- Username
- Password
- Full name
- Email address

#### 4. Instance Configuration

Configure the Jenkins URL (e.g., http://jenkins.example.com/)

#### 5. Basic System Configuration

Navigate to "Manage Jenkins" → "Configure System" to set up:

1. **System Message**
   
   Set a welcome message for users:
   ```
   Welcome to Our Jenkins CI/CD Server
   This server is maintained by the DevOps team. Contact us at devops@example.com for assistance.
   ```

2. **# of Executors**
   
   Set the number of concurrent builds on the controller (typically 0-2)

3. **Environment Variables**
   
   Add global environment variables:
   ```
   MAVEN_OPTS=-Xmx1024m
   COMPANY_NEXUS=https://nexus.example.com
   ```

4. **Global Tool Configuration**
   
   Configure tools like JDK, Maven, Gradle:
   
   *Example JDK configuration:*
   - Name: JDK 11
   - Install automatically: checked
   - Install from: AdoptOpenJDK
   - Version: OpenJDK 11
   
   *Example Maven configuration:*
   - Name: Maven 3.8.5
   - Install automatically: checked
   - Version: 3.8.5

### Plugin Management

Jenkins plugins extend its functionality and integrate with external tools.

#### 1. Installing Plugins

**Via UI:**
1. Navigate to "Manage Jenkins" → "Manage Plugins"
2. Go to "Available" tab
3. Search for plugins
4. Select plugins and click "Install without restart" or "Download now and install after restart"

**Via Jenkins CLI:**
```bash
java -jar jenkins-cli.jar -s http://localhost:8080/ install-plugin git pipeline-model-definition blueocean
```

**Using Configuration as Code:**
```yaml
jenkins:
  plugins:
    - git:latest
    - pipeline-model-definition:latest
    - blueocean:latest
```

#### 2. Updating Plugins

**Via UI:**
1. Go to "Manage Jenkins" → "Manage Plugins"
2. Check the "Available updates" tab
3. Select plugins to update
4. Click "Download now and install after restart"

**Best practices:**
- Review release notes before updating
- Update in test environment first
- Schedule updates during maintenance windows
- Keep plugins up-to-date for security patches

#### 3. Plugin Configuration

Most plugins add their own configuration sections to the Jenkins system configuration:

1. Go to "Manage Jenkins" → "Configure System"
2. Find the plugin's section
3. Configure plugin-specific settings

*Example: Configuring the Slack Notification plugin:*
- Team Domain: mycompany
- Integration Token: (secret token)
- Channel: #jenkins-notifications
- Test Connection

#### 4. Essential Plugins for CI/CD

1. **Source Code Management**
   - Git
   - Subversion
   - Bitbucket
   - GitHub Integration

2. **Build Tools**
   - Maven Integration
   - Gradle
   - Node.js
   - Docker

3. **Testing and Code Quality**
   - JUnit
   - Cobertura
   - SonarQube Scanner
   - JaCoCo

4. **Deployment**
   - Deploy to container
   - AWS Steps
   - Kubernetes

5. **Visualization and Reporting**
   - BlueOcean
   - Build Pipeline
   - Dashboard View

6. **Utility Plugins**
   - Credentials
   - Pipeline Utility Steps
   - Timestamper
   - AnsiColor

### User Management and Security

Managing users and security is crucial for Jenkins as it often has access to critical systems.

#### 1. User Creation and Management

**Creating Users:**
1. Navigate to "Manage Jenkins" → "Manage Users"
2. Click "Create User"
3. Fill in username, password, name, and email

**Managing Users:**
- View all users: "Manage Jenkins" → "Manage Users"
- Edit user details: Click on the cog icon next to the user
- Delete user: Click on the red X icon

**User API Token:**
1. Go to user's configuration page
2. Click "Add new Token"
3. Generate and save the token for API access

#### 2. Authentication Options

1. **Jenkins Database**
   
   Default authentication storing users locally in Jenkins.

2. **LDAP Integration**
   
   Connect to corporate directory:
   
   *Example configuration:*
   ```
   Server: ldap://ldap.example.com:389
   Root DN: dc=example,dc=com
   User search filter: uid={0}
   ```

3. **Active Directory**
   
   *Example configuration:*
   ```
   Domain name: example.com
   Domain controller: dc.example.com:3268
   Bind DN: cn=jenkins,ou=service,dc=example,dc=com
   Bind Password: (secure password)
   ```

4. **OAuth (Google, GitHub, etc.)**
   
   *Example GitHub OAuth configuration:*
   1. Register OAuth application in GitHub
   2. Install GitHub OAuth plugin
   3. Configure Client ID and Secret
   4. Set Authorization: "Logged-in users can do anything"

#### 3. Authorization Strategies

1. **Matrix-based Security**
   
   *Example configuration:*
   - admin: Overall/Administer
   - developers: Job/Read, Job/Build, Job/Configure
   - testers: Job/Read, Job/Build
   - viewers: Job/Read

2. **Project-based Matrix Authorization**
   
   *Example:*
   - ProjectA: TeamA has full access, TeamB has read access
   - ProjectB: TeamB has full access, TeamA has read access

3. **Role-based Authorization Strategy**
   
   *Example role configuration:*
   - Global roles:
     - admin: Overall/Administer
     - developer: Overall/Read, Job/Create
   - Project roles:
     - project-admin: Job/Configure, Job/Build
     - project-developer: Job/Build, Job/Read
     - project-viewer: Job/Read

4. **Authorize Project**
   
   Run jobs as specific users or with specific permissions.
   
   *Example:*
   ```groovy
   pipeline {
       agent any
       options {
           authorizationMatrix {
               permissions([
                   [user: 'alice', permission: 'Job/Build'],
                   [user: 'bob', permission: 'Job/Workspace']
               ])
           }
       }
       stages {
           // job stages
       }
   }
   ```

#### 4. Security Best Practices

1. **Principle of Least Privilege**
   - Grant minimum required permissions
   - Regularly audit permissions

2. **Credentials Management**
   - Use Jenkins Credentials Plugin
   - Never hardcode credentials in jobs
   - Rotate credentials regularly

3. **Agent Security**
   - Run agents with limited user permissions
   - Isolate agents with containers or VMs
   - Clean workspaces between builds

4. **Network Security**
   - Use HTTPS for web interface
   - Configure firewall rules
   - Use reverse proxy (Nginx/Apache) for additional security

5. **Audit Logging**
   - Install Audit Trail plugin
   - Monitor login attempts
   - Review job execution history

   *Example Audit Trail configuration:*
   - Log location: /var/log/jenkins/audit.log
   - Log format: %d{yyyy-MM-dd HH:mm:ss} %c{1} [%p] %m%n
   - Events to log: Login attempt, Configuration change, Job execution

## Basic Jenkins Jobs

### Freestyle Projects

Freestyle projects are the simplest and most flexible type of Jenkins jobs.

#### 1. Creating a Freestyle Project

1. Click "New Item" on the Jenkins dashboard
2. Enter a name (e.g., "my-first-job")
3. Select "Freestyle project" and click "OK"

#### 2. Configuring Source Code Management

**Git Configuration:**
1. Under "Source Code Management", select "Git"
2. Enter Repository URL: https://github.com/example/repo.git
3. Credentials: Add or select credentials
4. Branch Specifier: */main

**Advanced Git Options:**
- Checkout to specific directory
- Checkout submodules
- Shallow clone
- Clean before checkout

*Example advanced Git configuration:*
```
Repository URL: https://github.com/example/repo.git
Credentials: github-credentials
Branch Specifier: */release-*
Additional Behaviors:
  - Checkout to subdirectory: project-dir
  - Clean before checkout
  - Recursively update submodules
```

#### 3. Build Triggers

**Common Triggers:**

1. **Build periodically**
   
   Schedule builds using cron syntax:
   ```
   # Every weekday at 8am
   0 8 * * 1-5
   
   # Every 4 hours
   0 */4 * * *
   ```

2. **Poll SCM**
   
   Check for changes and build if changes are found:
   ```
   # Check every 15 minutes
   H/15 * * * *
   ```

3. **GitHub webhook**
   
   Build when changes are pushed to GitHub:
   1. Install GitHub plugin
   2. Add webhook in GitHub repository settings:
      - Payload URL: http://jenkins-url/github-webhook/
      - Content type: application/json
      - Events: Just the push event
   3. Select "GitHub hook trigger for GITScm polling" in job configuration

4. **Trigger from other jobs**
   
   Build after other jobs complete:
   - Select "Build after other projects are built"
   - Enter project names
   - Select trigger condition (success, stable, etc.)

#### 4. Build Environment

**Common Options:**

1. **Delete workspace before build starts**
   
   Clean workspace for consistent builds

2. **Set environment variables**
   
   Add custom environment variables:
   ```
   NAME=value
   VERSION=1.0.0
   ```

3. **Inject passwords and credentials**
   
   Securely provide credentials to builds:
   1. Install "Credentials Binding" plugin
   2. Select "Use secret text(s) or file(s)"
   3. Add bindings:
      - Username and password (separated)
      - Username and password (conjoined)
      - Secret text
      - Secret file

4. **Timestamper**
   
   Add timestamps to console output

#### 5. Build Steps

Build steps define what actions the job should perform.

**Common Build Steps:**

1. **Execute shell** (Linux/macOS)
   
   Run shell commands:
   ```bash
   echo "Building project..."
   mvn clean install
   echo "Build completed successfully"
   ```

2. **Execute Windows batch command**
   
   Run batch commands:
   ```batch
   echo "Building project..."
   mvn clean install
   echo "Build completed successfully"
   ```

3. **Invoke Ant**
   
   Run Ant targets:
   - Ant Version: Ant 1.10.8
   - Targets: clean compile test

4. **Invoke top-level Maven targets**
   
   Run Maven goals:
   - Maven Version: Maven 3.8.5
   - Goals: clean install
   - POM: pom.xml
   - Properties: skipTests=true

5. **Run with Docker**
   
   Execute commands in Docker container:
   ```bash
   docker run --rm -v $WORKSPACE:/app -w /app maven:3.8.5-openjdk-11 mvn clean install
   ```

#### 6. Post-build Actions

Actions to perform after the build completes.

**Common Post-build Actions:**

1. **Archive artifacts**
   
   Save build outputs:
   - Files to archive: target/*.jar, target/*.war
   - Exclude: target/*-sources.jar
   - Archive only if build succeeds: checked

2. **Publish JUnit test results**
   
   Process test reports:
   - Test report XMLs: target/surefire-reports/*.xml
   - Health report amplification factor: 1.0
   - Allow empty results: unchecked

3. **Email notification**
   
   Send email on build results:
   - Recipients: team@example.com
   - Send separate emails to individuals who broke the build: checked
   - Send email for every unstable build: checked

4. **Trigger downstream projects**
   
   Start other jobs:
   - Projects to build: deployment-job, notification-job
   - Trigger only if build succeeds: checked

5. **Publish code coverage**
   
   Process coverage reports:
   - Report directory: target/site/cobertura
   - Health targets:
     - Method: 80%
     - Line: 80%
     - Conditional: 70%

### Pipeline Projects

Pipeline projects define the entire build process as code, typically in a Jenkinsfile.

#### 1. Creating a Pipeline Project

1. Click "New Item" on the Jenkins dashboard
2. Enter a name (e.g., "my-pipeline")
3. Select "Pipeline" and click "OK"

#### 2. Pipeline Definition

**Options for defining pipelines:**

1. **Pipeline script**
   
   Write pipeline code directly in Jenkins:
   
   ```groovy
   pipeline {
       agent any
       
       stages {
           stage('Checkout') {
               steps {
                   git 'https://github.com/example/repo.git'
               }
           }
           stage('Build') {
               steps {
                   sh 'mvn clean install'
               }
           }
           stage('Test') {
               steps {
                   sh 'mvn test'
               }
           }
       }
   }
   ```

2. **Pipeline script from SCM**
   
   Store pipeline in version control:
   
   - SCM: Git
   - Repository URL: https://github.com/example/repo.git
   - Credentials: Select credentials
   - Branch: */main
   - Script Path: Jenkinsfile