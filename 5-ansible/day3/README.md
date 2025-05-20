# Ansible Day 3 Training

## Table of Contents

1. [YAML Syntax](#yaml-syntax-basic)

   - [Basic YAML Rules](#basic-yaml-rules)
   - [YAML Best Practices](#yaml-best-practices)
   - [YAML Validation Tools](#yaml-validation-tools)
   - [Practice Exercises](#practice-exercises)
   - [Additional Resources](#additional-resources)

2. [Ansible Playbooks and Basic Operations](#ansible-playbooks-and-basic-operations)
   - [Introduction to Playbooks](#1-introduction-to-playbooks)
   - [Writing Your First Playbook](#2-writing-your-first-playbook)
   - [Variables in Ansible](#3-variables-in-ansible)
   - [Conditionals and Loops](#4-conditionals-and-loops)
   - [Handlers](#5-handlers)
   - [Conclusion and Next Steps](#conclusion-and-next-steps)

# YAML Syntax (Basic)

YAML (YAML Ain't Markup Language) is a human-readable data serialization format. It's commonly used for configuration files and data exchange. Here's a comprehensive guide:

##### Basic YAML Rules

1. **Indentation Matters**

   - Use spaces (not tabs) for indentation
   - Typically 2 spaces per level
   - Must be consistent throughout the file

2. **Key-Value Pairs**

   ```yaml
   # Simple key-value pair
   name: John

   # Key with multiple values
   person:
     name: John
     age: 30
     city: New York

   # Use quotes when:
   # - String contains special characters (: { } [ ] , & * # ? | - < > = ! % @ \)
   # - String starts with a number or special character
   # - String is 'true'/'false'/'yes'/'no' and you want them as strings
   # - String contains spaces at start/end
   full_name: 'John Smith'
   description: 'This is a "quoted" string'
   ```

3. **Lists/Arrays**

   ```yaml
   # Simple list
   fruits:
     - apple
     - banana
     - orange

   # List of objects
   people:
     - name: John
       age: 30
     - name: Jane
       age: 25

   # Inline list
   colors: [red, blue, green]
   ```

4. **Multi-line Strings**

   ```yaml
   # Using | (preserves newlines)
   description: |
     This is a multi-line
     string that preserves
     line breaks

   # Using > (folds newlines)
   summary: >
     This is a multi-line
     string that folds
     into a single line
   ```

5. **Anchors and References**

   ```yaml
   # Define an anchor
   person: &person_template
     name: John
     age: 30

   # Reference the anchor
   employee1: *person_template
   employee2: *person_template
   ```

   ```yaml
   # Define a template with variables
   defaults: &defaults
     cpu: 2
     memory: 4G
     disk: 100G

   # Override specific values while using template
   small_instance:
     <<: *defaults # Merge all values from defaults
     memory: 2G # Override just the memory

   large_instance:
     <<: *defaults # Merge all values from defaults
     cpu: 4 # Override CPU
     memory: 8G # Override memory
     disk: 500G # Override disk
   ```

6. **Data Types**

   ```yaml
   # Strings
   name: John
   title: 'Mr. Smith'

   # Numbers
   age: 30
   price: 19.99

   # Booleans
   is_active: true
   is_admin: false

   # Null values
   middle_name: null
   last_name: ~
   ```

7. **Comments**
   ```yaml
   # This is a single-line comment
   name: John # This is an end-of-line comment
   ```

##### YAML Best Practices

1. **Consistent Indentation**

   - Use 2 spaces (Ansible standard)
   - Never mix spaces and tabs
   - Keep indentation consistent

2. **Naming Conventions**

   - Use lowercase for keys
   - Use underscores for spaces
   - Be descriptive but concise

3. **Structure**

   - Keep related items together
   - Use comments for complex sections
   - Break long files into logical sections

4. **Common Pitfalls to Avoid**

   ```yaml
   # WRONG - Inconsistent indentation
   tasks:
     - name: Task 1
       apt:
         name: nginx
       state: present  # Wrong indentation!

   # CORRECT
   tasks:
     - name: Task 1
       apt:
         name: nginx
         state: present
   ```

##### YAML Validation Tools

1. **Online Validators**

   - [YAML Lint](http://www.yamllint.com/)
   - [YAML Validator](https://validateyaml.web.app/)

2. **Command Line Tools**
   ```bash
   # Using Python's yamllint
   pip install yamllint
   yamllint playbook.yml
   ```

##### Practice Exercises

1. **Basic Structure**

   ```yaml
   # Create a YAML file for a user profile
   user:
     name: John Doe
     age: 30
     email: john@example.com
     roles:
       - admin
       - developer
     settings:
       theme: dark
       notifications: true
   ```

2. **Complex Structure**
   ```yaml
   # Create a YAML file for a web application configuration
   application:
     name: MyWebApp
     version: 1.0.0
     database:
       host: localhost
       port: 5432
       credentials:
         username: admin
         password: secret
     servers:
       - name: web1
         ip: 192.168.1.10
         roles: [web, cache]
       - name: web2
         ip: 192.168.1.11
         roles: [web, cache]
   ```

##### Additional Resources

1. **Official YAML Documentation**

   - [YAML Specification](https://yaml.org/spec/1.2/spec.html)
   - [YAML Tutorial](https://yaml.org/start.html)

2. **Ansible YAML References**
   - [Ansible YAML Syntax](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)
   - [Ansible Playbook Examples](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)

# Ansible Playbooks and Basic Operations

## 1. Introduction to Playbooks

### What are Playbooks?

Playbooks are Ansible's configuration, deployment, and orchestration language. They are expressed in YAML format and can describe a policy you want your systems to enforce or a set of steps in a general IT process.

Think of playbooks as instruction manuals for tasks that need to be executed on remote systems.

### Playbook Structure

A basic playbook consists of:

1. **Plays**: A playbook can contain one or more plays
2. **Tasks**: Each play contains a list of tasks to execute
3. **Modules**: Each task calls an Ansible module

```yaml
---
# A simple playbook with one play
- name: My first play
  hosts: web_servers
  become: true

  tasks:
    - name: Ensure Apache is installed
      package:
        name: apache2
        state: present

    - name: Ensure Apache is running
      service:
        name: apache2
        state: started
        enabled: true
```

### Basic Playbook Components

1. **Play header**:

   - `name`: A descriptive name for the play (optional but recommended)
   - `hosts`: Specifies which hosts from your inventory to target
   - `become`: Whether to use privilege escalation (sudo)
   - `vars`: Variables for the play
   - `gather_facts`: Whether to gather system information before tasks (default: true)

2. **Tasks**:

   - `name`: Description of what the task does (optional but recommended)
   - Module name and parameters
   - Task-specific keywords (e.g., `when`, `loop`, `register`)

3. **Other components** (we'll cover these later):
   - Handlers
   - Roles
   - Includes and imports

### Exercise 1.1: Analyzing a Playbook

Take a moment to analyze this playbook:

```yaml
---
- name: Configure web servers
  hosts: web
  become: true
  vars:
    http_port: 80
    max_clients: 200

  tasks:
    - name: Install Apache
      package:
        name: httpd
        state: present

    - name: Start Apache service
      service:
        name: httpd
        state: started
        enabled: true

    - name: Open firewall for HTTP
      firewalld:
        service: http
        permanent: true
        state: enabled
        immediate: true
```

Identify the:

- Number of plays
- Target hosts
- Variables defined
- Number of tasks
- Modules used

## 2. Writing Your First Playbook

Let's create a simple playbook to install and configure a web server.

### Creating a Simple Playbook

```yaml
---
- name: Configure web server
  hosts: webservers
  become: true

  tasks:
    - name: Install Apache
      package:
        name: apache2
        state: present

    - name: Start and enable Apache
      service:
        name: apache2
        state: started
        enabled: true

    - name: Create a test page
      copy:
        content: |
          <html>
            <body>
              <h1>Hello from Ansible!</h1>
              <p>This page was created by Ansible.</p>
            </body>
          </html>
        dest: '/var/www/html/index.html'
        owner: 'www-data'
        group: 'www-data'
        mode: '0644'
```

### Understanding Playbook Execution

To run your playbook:

```bash
ansible-playbook -i inventory webserver.yml
```

Execution phases:

1. **Parsing**: Ansible checks YAML syntax and playbook structure
2. **Inventory loading**: Ansible loads the inventory and resolves groups
3. **Variable loading**: Variables from various sources are loaded and merged
4. **Play execution**: For each play:
   - Fact gathering (if enabled)
   - Task execution in sequence
   - Handler execution (if notified)

### Debugging Playbooks

Common debugging techniques:

1. **Check mode**: Run playbook without making changes

   ```bash
   ansible-playbook webserver.yml --check
   ```

2. **Verbose output**: Get more details about execution

   ```bash
   ansible-playbook webserver.yml -v      # Verbose
   ansible-playbook webserver.yml -vv     # More verbose
   ansible-playbook webserver.yml -vvv    # Debug level
   ansible-playbook webserver.yml -vvvv   # Connection level debugging
   ```

3. **Syntax check**: Validate playbook syntax

   ```bash
   ansible-playbook webserver.yml --syntax-check
   ```

4. **Step execution**: Execute one task at a time with confirmation

   ```bash
   ansible-playbook webserver.yml --step
   ```

5. **Start at task**: Begin execution from a specific task
   ```bash
   ansible-playbook webserver.yml --start-at-task="Create a test page"
   ```

### Exercise 2.1: Write and Debug a Playbook

Create a simple playbook named `system_info.yml` that:

- Targets all your hosts
- Gathers facts
- Creates a file with basic system information (hostname, distribution, IP address)

Use debugging techniques to verify it's working correctly before actual execution.

```yaml
---
- name: Gather system information
  hosts: all

  tasks:
    - name: Create system info file
      copy:
        content: |
          Hostname: {{ ansible_hostname }}
          Distribution: {{ ansible_distribution }} {{ ansible_distribution_version }}
          IP Address: {{ ansible_default_ipv4.address | default("No data") }}
          CPU Cores: {{ ansible_processor_cores }}
          Memory: {{ ansible_memtotal_mb }} MB
        dest: /tmp/system_info.txt
        mode: '0644'
```

## 3. Variables in Ansible

Variables allow you to handle differences between systems dynamically.

### Variable Types

Ansible supports several data types for variables:

1. **Strings**: Text values

   ```yaml
   username: 'john'
   ```

2. **Numbers**: Integers or floating-point values

   ```yaml
   http_port: 80
   pi: 3.14159
   ```

3. **Booleans**: True/false values

   ```yaml
   enable_feature: true
   debug_mode: false
   ```

4. **Lists**: Ordered collections of items

   ```yaml
   users:
     - alice
     - bob
     - charlie
   ```

5. **Dictionaries**: Key-value mappings
   ```yaml
   user:
     name: john
     role: admin
     groups:
       - wheel
       - docker
   ```

### Variable Precedence

Ansible processes variables in a specific order of precedence (from highest to lowest):

1. Extra vars (`-e` or `--extra-vars` on command line)
2. Task vars (only for the specific task)
3. Block vars (only for tasks in block)
4. Role and include vars
5. Play vars_files
6. Play vars_prompt
7. Play vars
8. Host facts
9. Registered vars
10. Set_facts
11. Role vars (defined in role/vars/main.yml)
12. Block vars (in parent blocks)
13. Role default vars (defined in role/defaults/main.yml)
14. Inventory vars (host_vars, group_vars)
15. Inventory file or script host vars
16. Playbook host_vars
17. Playbook group_vars
18. Inventory file or script group vars
19. Playbook group_vars/all
20. Playbook host_vars/\*
21. Command line values (e.g., -u user)

### Variable Sources

Variables can be defined in multiple places:

1. **Inventory variables**:

   - In inventory file:
     ```ini
     [webservers]
     web1 ansible_host=10.0.0.1 http_port=8080
     ```
   - In group_vars files: `group_vars/webservers.yml`
   - In host_vars files: `host_vars/web1.yml`

2. **Playbook variables**:

   ```yaml
   - hosts: webservers
     vars:
       http_port: 80
       max_clients: 200
   ```

3. **Vars files** (included in playbooks):

   ```yaml
   - hosts: webservers
     vars_files:
       - vars/common.yml
       - vars/webserver.yml
   ```

4. **Command line variables**:

   ```bash
   ansible-playbook playbook.yml -e "http_port=8080 max_clients=300"
   ```

5. **Registered variables** (saving task output):
   ```yaml
   - name: Check service status
     command: systemctl status httpd
     register: service_status
   ```

### Using Variables in Playbooks

To use variables in playbooks, wrap them in `{{ }}`:

```yaml
---
- name: Variable demonstration
  hosts: webservers
  vars:
    web_package: apache2
    web_service: apache2
    web_config_file: /etc/apache2/apache2.conf

  tasks:
    - name: Install web server
      package:
        name: '{{ web_package }}'
        state: present

    - name: Configure web server
      template:
        src: templates/apache.conf.j2
        dest: '{{ web_config_file }}'
      notify: Restart web service

    - name: Ensure web service is running
      service:
        name: '{{ web_service }}'
        state: started
        enabled: true

  handlers:
    - name: Restart web service
      service:
        name: '{{ web_service }}'
        state: restarted
```

#### Accessing dictionary variables:

```yaml
vars:
  user:
    name: john
    home: /home/john

tasks:
  - name: Create user directory
    file:
      path: '{{ user.home }}/projects'
      state: directory
```

#### Accessing list variables:

```yaml
vars:
  packages:
    - httpd
    - php
    - mariadb-server

tasks:
  - name: Install packages
    package:
      name: '{{ packages }}'
      state: present
```

### Exercise 3.1: Working with Variables

Create a playbook that uses variables to:

1. Install different packages based on the OS family
2. Configure a service with parameters from variables
3. Use both inline variables and a vars_file

Create a file named `app_deploy.yml`:

```yaml
---
- name: Deploy application
  hosts: app_servers
  vars:
    app_name: myapp
    app_version: 1.2.0
  vars_files:
    - vars/app_config.yml

  tasks:
    - name: Install OS-specific dependencies
      package:
        name: '{{ os_packages[ansible_os_family] }}'
        state: present

    - name: Create app directory
      file:
        path: '{{ app_path }}'
        state: directory
        owner: '{{ app_user }}'
        mode: '0755'

    - name: Deploy app configuration
      template:
        src: templates/app.conf.j2
        dest: '{{ app_config_path }}'
        owner: '{{ app_user }}'
        mode: '0644'
      notify: Restart app service
```

Then create the vars file `vars/app_config.yml`:

```yaml
---
app_path: /opt/{{ app_name }}-{{ app_version }}
app_user: appuser
app_config_path: '{{ app_path }}/config/app.conf'

os_packages:
  Debian:
    - python3
    - python3-pip
    - libpq-dev
  RedHat:
    - python3
    - python3-pip
    - postgresql-devel
```

## 4. Conditionals and Loops

Conditionals and loops help make playbooks more dynamic and efficient.

### Using When Conditions

The `when` clause allows you to conditionally execute tasks based on variable values or facts.

Basic syntax:

```yaml
- name: Task with condition
  module:
    param1: value1
  when: condition_is_true
```

Examples:

1. **OS-specific tasks**:

```yaml
- name: Install Apache (Debian/Ubuntu)
  apt:
    name: apache2
    state: present
  when: ansible_os_family == "Debian"

- name: Install Apache (RedHat/CentOS)
  yum:
    name: httpd
    state: present
  when: ansible_os_family == "RedHat"
```

2. **Variable-based conditions**:

```yaml
- name: Enable debug mode
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf
  when: debug_mode | bool
```

3. **File existence**:

```yaml
- name: Check if config exists
  stat:
    path: /etc/app/config.yml
  register: config_file

- name: Create default config
  template:
    src: default_config.j2
    dest: /etc/app/config.yml
  when: not config_file.stat.exists
```

4. **Multiple conditions** (AND):

```yaml
- name: Perform task
  debug:
    msg: 'This will run if both conditions are true'
  when: ansible_memory_mb.real.total > 2048 and ansible_processor_cores > 1
```

5. **Multiple conditions** (OR):

```yaml
- name: Perform task
  debug:
    msg: 'This will run if either condition is true'
  when: ansible_distribution == "Ubuntu" or ansible_distribution == "Debian"
```

### Working with Loops

Loops allow you to perform the same task multiple times with different values.

#### Basic loop with `loop`:

```yaml
- name: Create multiple users
  user:
    name: '{{ item }}'
    state: present
    groups: developers
  loop:
    - john
    - jane
    - bob
```

#### Looping through dictionaries:

```yaml
- name: Create users with specific properties
  user:
    name: '{{ item.name }}'
    groups: '{{ item.groups }}'
    shell: "{{ item.shell | default('/bin/bash') }}"
  loop:
    - { name: john, groups: 'developers', shell: '/bin/bash' }
    - { name: jane, groups: 'admins,developers' }
    - { name: bob, groups: 'testers' }
```

#### Looping with index using `loop` and `loop_control`:

```yaml
- name: Create directories with specific permissions
  file:
    path: '/opt/app/dir{{ item.0 }}'
    state: directory
    mode: '{{ item.1 }}'
  loop: "{{ range(1, 4) | product(['0755', '0700', '0644']) | list }}"
  loop_control:
    label: 'Directory {{ item.0 }} (mode: {{ item.1 }})'
```

#### Loop with complex data structures:

```yaml
vars:
  web_servers:
    - name: web1
      ip: 192.168.1.10
      packages:
        - nginx
        - php-fpm
    - name: web2
      ip: 192.168.1.11
      packages:
        - apache2
        - libapache2-mod-php

tasks:
  - name: Install packages for each server
    debug:
      msg: 'Would install {{ item.1 }} on {{ item.0.name }}'
    loop: "{{ web_servers | subelements('packages') }}"
```

### Combining Conditions and Loops

You can use conditions and loops together:

```yaml
- name: Install packages if enabled
  package:
    name: '{{ item }}'
    state: present
  loop: '{{ packages }}'
  when: enable_package_install | bool
```

Or with conditions inside loops:

```yaml
- name: Install optional packages
  package:
    name: '{{ item.name }}'
    state: '{{ item.state }}'
  loop:
    - { name: 'nginx', state: 'present' }
    - { name: 'php-fpm', state: 'present' }
    - { name: 'mariadb-server', state: 'present', optional: true }
    - { name: 'redis', state: 'present', optional: true }
  when: not item.optional | default(false) or install_optional_packages | default(false)
```

### Exercise 4.1: Using Conditionals and Loops

Create a playbook that:

1. Installs a list of base packages on all servers
2. Installs additional packages based on server role (web, db, cache)
3. Configures firewall rules with loops and conditionals

```yaml
---
- name: Configure servers based on roles
  hosts: all
  become: true
  vars:
    base_packages:
      - vim
      - curl
      - htop
    web_packages:
      - nginx
      - php-fpm
    db_packages:
      - mariadb-server
      - python3-pymysql
    cache_packages:
      - redis
    firewall_rules:
      - service: ssh
        port: 22
        state: enabled
      - service: http
        port: 80
        state: enabled
        servers: web
      - service: https
        port: 443
        state: enabled
        servers: web
      - service: mysql
        port: 3306
        state: enabled
        servers: db
      - service: redis
        port: 6379
        state: enabled
        servers: cache

  tasks:
    - name: Install base packages
      package:
        name: '{{ item }}'
        state: present
      loop: '{{ base_packages }}'

    - name: Install web server packages
      package:
        name: '{{ item }}'
        state: present
      loop: '{{ web_packages }}'
      when: "'web' in group_names"

    - name: Install database packages
      package:
        name: '{{ item }}'
        state: present
      loop: '{{ db_packages }}'
      when: "'db' in group_names"

    - name: Install cache server packages
      package:
        name: '{{ item }}'
        state: present
      loop: '{{ cache_packages }}'
      when: "'cache' in group_names"

    - name: Configure firewall rules
      firewalld:
        service: '{{ item.service }}'
        port: '{{ item.port }}/tcp'
        permanent: true
        state: '{{ item.state }}'
        immediate: true
      loop: '{{ firewall_rules }}'
      when: item.servers is not defined or item.servers in group_names
```

## 5. Handlers

Handlers are special tasks that only run when notified by other tasks.

### Understanding Handlers

Key points about handlers:

- Handlers run at the end of the play, not when notified
- They only run once, even if notified multiple times
- They run in the order specified in the handlers section, not the notification order
- If any task fails before the handler notification, the handler won't run

### Creating and Using Handlers

Basic syntax:

```yaml
tasks:
  - name: Template configuration file
    template:
      src: template.j2
      dest: /etc/service/config
    notify: Restart service

handlers:
  - name: Restart service
    service:
      name: service_name
      state: restarted
```

Example playbook with handlers:

```yaml
---
- name: Configure web and database services
  hosts: all
  become: true
  vars:
    db_name: myapp
    db_user: appuser
    web_port: 80

  tasks:
    # Web server tasks
    - name: Install Apache
      package:
        name: apache2
        state: present
      when: "'web' in group_names"

    - name: Create Apache virtual host
      template:
        src: vhost.conf.j2
        dest: /etc/apache2/sites-available/myapp.conf
      when: "'web' in group_names"
      notify:
        - Enable Apache site
        - Reload Apache

    # Database server tasks
    - name: Install MariaDB
      package:
        name: mariadb-server
        state: present
      when: "'db' in group_names"

    - name: Create database configuration
      template:
        src: my.cnf.j2
        dest: /etc/mysql/mariadb.conf.d/50-server.cnf
      when: "'db' in group_names"
      notify: Restart MariaDB

    - name: Ensure MySQL is started
      service:
        name: mariadb
        state: started
        enabled: true
      when: "'db' in group_names"

    - name: Create database
      mysql_db:
        name: '{{ db_name }}'
        state: present
      when: "'db' in group_names"
      register: db_created
      notify: Import database schema

  handlers:
    # Web server handlers
    - name: Enable Apache site
      command: a2ensite myapp.conf
      listen: 'Enable Apache site'

    - name: Reload Apache
      service:
        name: apache2
        state: reloaded

    # Database server handlers
    - name: Restart MariaDB
      service:
        name: mariadb
        state: restarted

    - name: Import database schema
      mysql_db:
        name: '{{ db_name }}'
        state: import
        target: /tmp/schema.sql
      when: db_created.changed
```

### Advanced Handler Features

#### Using `listen`:

The `listen` directive allows multiple handlers to be notified using a single name:

```yaml
tasks:
  - name: Configure something
    template:
      src: template.j2
      dest: /etc/config.conf
    notify: 'restart all services'

handlers:
  - name: Restart Apache
    service:
      name: apache2
      state: restarted
    listen: 'restart all services'

  - name: Restart MariaDB
    service:
      name: mariadb
      state: restarted
    listen: 'restart all services'
```

#### Handler chains:

Handlers can notify other handlers:

```yaml
handlers:
  - name: Restart Apache
    service:
      name: apache2
      state: restarted
    notify: Check Apache status

  - name: Check Apache status
    command: systemctl status apache2
    register: apache_status
```

#### Forcing handlers to run:

You can force handlers to run even if tasks fail by using `--force-handlers` flag:

```bash
ansible-playbook playbook.yml --force-handlers
```

### Exercise 5.1: Working with Handlers

Create a playbook that:

1. Installs and configures the Nginx web server
2. Sets up a virtual host for a sample website
3. Uses handlers to reload/restart services as needed

```yaml
---
- name: Configure Nginx web server
  hosts: webservers
  become: true
  vars:
    nginx_port: 80
    server_name: example.com
    web_root: /var/www/example

  tasks:
    - name: Install Nginx
      package:
        name: nginx
        state: present

    - name: Create web root directory
      file:
        path: '{{ web_root }}'
        state: directory
        owner: www-data
        group: www-data
        mode: '0755'

    - name: Create sample index page
      copy:
        content: |
          <!DOCTYPE html>
          <html>
            <head>
              <title>Welcome to {{ server_name }}</title>
            </head>
            <body>
              <h1>Welcome to {{ server_name }}</h1>
              <p>This site was configured using Ansible!</p>
            </body>
          </html>
        dest: '{{ web_root }}/index.html'
        owner: www-data
        group: www-data
        mode: '0644'

    - name: Configure Nginx virtual host
      template:
        src: templates/nginx_vhost.j2
        dest: /etc/nginx/sites-available/example.com.conf
      notify: Validate Nginx configuration

    - name: Enable virtual host
      file:
        src: /etc/nginx/sites-available/example.com.conf
        dest: /etc/nginx/sites-enabled/example.com.conf
        state: link
      notify: Reload Nginx

    - name: Allow HTTP through firewall
      ufw:
        rule: allow
        port: '{{ nginx_port }}'
        proto: tcp
      notify: Reload firewall

  handlers:
    - name: Validate Nginx configuration
      command: nginx -t
      register: nginx_valid
      notify: Enable Nginx
      changed_when: false

    - name: Enable Nginx
      service:
        name: nginx
        enabled: true
      listen: 'Enable Nginx'

    - name: Reload Nginx
      service:
        name: nginx
        state: reloaded
      when: nginx_valid is success

    - name: Reload firewall
      service:
        name: ufw
        state: reloaded
```

## Conclusion and Next Steps

Congratulations! You've now completed Day 2 of your Ansible learning journey. You've learned:

- The basics of YAML syntax and playbook structure
- How to write and debug playbooks
- Working with variables from different sources
- Using conditionals and loops for dynamic playbooks
- Implementing handlers for efficient configuration changes

### Practice Exercises

To reinforce what you've learned, try these exercises:

1. Create a playbook that sets up a complete LAMP stack (Linux, Apache, MySQL, PHP)
2. Extend the playbook to deploy a simple PHP application
3. Use different variables for development and production environments
4. Implement error handling for when services fail to start

### What's Next?

In the next part of your Ansible journey, consider exploring:

- Roles for organizing playbooks
- Ansible Vault for managing secrets
- Ansible Galaxy for community roles
- Advanced templates with Jinja2
- Dynamic inventories
