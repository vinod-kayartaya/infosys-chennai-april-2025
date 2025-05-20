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
