# Ansible Playbooks Lab Assignments

## Lab 1: Basic Playbook Development and Execution

### Objective

Create and execute basic Ansible playbooks to configure multiple servers with standard system configurations.

### Lab Environment

- 10 Docker containers representing different types of servers
- All containers accessible via SSH on different ports mapped to localhost
- Base container images include Ubuntu and CentOS variants

### Requirements

1. Create a playbook named `system_setup.yml` that performs the following tasks on all hosts:

   - Update package cache
   - Install essential system packages (vim, curl, wget, htop, tcpdump)
   - Create a standard user account with sudo privileges
   - Configure the timezone to UTC
   - Set up basic system limits for open files and processes

2. Create a playbook named `webserver_setup.yml` that:

   - Installs and configures Apache or Nginx on designated web servers
   - Creates a default virtual host configuration
   - Deploys a simple static website
   - Ensures the web service is started and enabled
   - Configures basic server settings (worker processes, timeout, etc.)

3. Create a playbook named `dbserver_setup.yml` that:

   - Installs and configures MariaDB or PostgreSQL on database servers
   - Sets up initial database security
   - Creates a sample database and user
   - Configures basic performance settings
   - Ensures the database service is running and enabled

4. Create a main playbook `site.yml` that:

   - Includes all three previous playbooks
   - Uses appropriate host targeting for each included playbook
   - Adds clear play names and descriptions
   - Implements proper task naming conventions

5. Implement proper playbook organization:

   - Use appropriate directory structure for playbooks
   - Follow best practices for playbook organization
   - Add comments and documentation within playbooks
   - Use proper YAML formatting and indentation

6. Test and validate:
   - Execute playbooks with appropriate flags
   - Test playbooks for idempotence (run multiple times without errors)
   - Document any issues encountered and their resolution

### Deliverables

- Complete set of well-documented playbooks
- Directory structure following best practices
- Documentation explaining the purpose of each playbook
- Output logs showing successful execution
- Brief report on lessons learned and challenges encountered

## Lab 2: Deploying a Flask Application with Ansible and MariaDB

In this lab, you will create Ansible playbooks to automate the deployment of a Flask web application with a MariaDB backend. This exercise will help you understand how to use Infrastructure as Code (IaC) principles to manage multi-tier application deployments in a repeatable and consistent manner.

### Learning Objectives

- Create Ansible playbooks to automate multi-tier application deployment
- Configure MariaDB database server installations
- Install and configure Python environments
- Clone and configure a Git repository
- Set up and manage Python virtual environments and environment variables
- Configure and run a Flask application with Gunicorn
- Establish secure connections between application and database tiers

### Requirements

- A Linux host with Ansible installed (version 2.9 or higher)
- Basic understanding of YAML syntax
- Familiarity with Python and Flask concepts
- At least two target hosts (one for the application, one for the database)
- Basic understanding of database concepts

### Assignment Tasks

#### Task 1: Create an Ansible Inventory File

Create an inventory file that defines two groups:

- `app_servers`: Hosts that will run the Flask application
- `db_servers`: Hosts that will run the MariaDB database

#### Task 2: Create Ansible Playbooks

Create two playbooks:

1. `deploy_mariadb.yml` that will:

   - Install and configure MariaDB on the hosts in the `db_servers` group
   - Create a database and database user for the Flask application
   - Configure appropriate permissions and security settings
   - Ensure the database service starts automatically

2. `deploy_flask_app.yml` that will:
   - Install the latest version of Python on the hosts in the `app_servers` group
   - Clone the specified GitHub repository containing the Flask application
   - Create and configure a Python virtual environment
   - Install all required dependencies from the project's requirements.txt
   - Configure necessary environment variables to connect to the MariaDB database
   - Configure and run the application using Gunicorn as the WSGI server

#### Task 3: Environment Variable Configuration

Create a configuration file or method to manage the following environment variables required by the application:

- Database connection parameters (host, port, username, password, database name)
- Any other application-specific configuration parameters

These environment variables should be securely set and appropriately passed to the Flask application.

#### Task 4: Playbook Specifications

Your playbooks should:

- Use appropriate Ansible modules for each task
- Include proper error handling
- Be idempotent (can be run multiple times without causing errors)
- Include comments explaining the purpose of each section
- Use variables where appropriate to make the playbooks more flexible
- Implement proper security practices (avoid hardcoding sensitive information)
- Use Ansible roles where appropriate to organize your code

#### Task 5: Testing Your Playbooks

Test your playbooks by:

1. Running them against clean environments
2. Verifying the database is correctly configured and accessible only to the application
3. Verifying the application is accessible via HTTP and correctly connects to the database
4. Making small changes and re-running the playbooks to ensure idempotency
5. Testing failure scenarios and recovery

Below is a recommended folder structure for organizing your Ansible project:

```
flask-ansible-deployment/
│
├── inventory/
│   ├── hosts                  # Main inventory file
│   └── group_vars/
│       ├── all.yml            # Variables for all hosts
│       ├── app_servers.yml    # Variables specific to app servers
│       └── db_servers.yml     # Variables specific to database servers
├── deploy_mariadb.yml        # Main playbook for MariaDB deployment
├── deploy_flask_app.yml      # Main playbook for Flask app deployment
├── site.yml                  # Master playbook to run all deployments
└── README.md                 # Project documentation
```

This structure follows Ansible best practices by:

- Separating inventory from playbooks
- Using group_vars for variable organization
- Including proper documentation

You are free to modify this structure based on your specific needs, but your submission should follow a similar organizational approach.

### Deliverables

1. The Ansible inventory file
2. The completed `deploy_mariadb.yml` playbook
3. The completed `deploy_flask_app.yml` playbook
4. Any additional files needed for configuration (templates, vars files, etc.)
5. A brief report (maximum 2 pages) explaining:
   - Your approach to creating the playbooks
   - How you managed environment variables and secure information
   - Any challenges you encountered and how you resolved them
   - How you tested the playbooks
   - Any recommendations for improving the deployment process

### Repository Information

For this assignment, you will use the following GitHub repository URL:

```
https://github.com/vinod-kayartaya/flask-products-api
```

This repository contains a Flask Products API application that uses MariaDB as its backend database.

### Notes on the Flask-Products-API Repository

The Flask Products API repository (https://github.com/vinod-kayartaya/flask-products-api) has the following key characteristics:

1. It's a RESTful API built with Flask for managing product data
2. It uses MariaDB as its backend database
3. The application uses environment variables for configuration, including:
   - `DB_HOST`: The hostname of the MariaDB server
   - `DB_PORT`: The port for the MariaDB server (default: 3306)
   - `DB_USER`: The database username
   - `DB_PASSWORD`: The database password
   - `DB_NAME`: The name of the database

Your Ansible playbooks should properly configure these environment variables to ensure the application can connect to the database server.

You may need to create database tables based on the schema requirements in the repository. Examine the application code to understand the database structure needed or look for any SQL setup files included in the repository.

### Helpful Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Python Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/pip_module.html)
- [Ansible Git Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html)
- [Ansible MySQL/MariaDB Module](https://docs.ansible.com/ansible/latest/collections/community/mysql/mysql_db_module.html)
- [Ansible MySQL/MariaDB User Module](https://docs.ansible.com/ansible/latest/collections/community/mysql/mysql_user_module.html)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Flask Environment Configuration](https://flask.palletsprojects.com/en/2.0.x/config/)
- [Managing Environment Variables in Ansible](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html)
