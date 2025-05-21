# Conditionals and Loops

Conditionals and loops help make playbooks more dynamic and efficient.

## Using When Conditions

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

## Working with Loops

Loops allow you to perform the same task multiple times with different values.

### Basic loop with `loop`:

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

### Looping through dictionaries:

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

### Looping with index using `loop` and `loop_control`:

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

### Loop with complex data structures:

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

## Combining Conditions and Loops

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

## Exercise: Using Conditionals and Loops

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

# Handlers

Handlers are special tasks that only run when notified by other tasks.

## Understanding Handlers

Key points about handlers:

- Handlers run at the end of the play, not when notified
- They only run once, even if notified multiple times
- They run in the order specified in the handlers section, not the notification order
- If any task fails before the handler notification, the handler won't run

## Creating and Using Handlers

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

## Advanced Handler Features

### Using `listen`:

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

### Handler chains:

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

### Forcing handlers to run:

You can force handlers to run even if tasks fail by using `--force-handlers` flag:

```bash
ansible-playbook playbook.yml --force-handlers
```

## Note:

Handlers and regular tasks in Ansible serve different purposes, and there are certain scenarios where handlers offer unique functionality that regular tasks don't provide.

The key difference is that handlers are only triggered when notified by tasks and run at specific points in the playbook execution (typically at the end of each play). They're designed for actions that should only happen once, regardless of how many tasks notify them.

Here are scenarios where handlers are more suitable than regular tasks:

1. Service restarts after configuration changes - If multiple tasks modify a service's configuration, you want the service to restart only once after all changes are complete, not after each change. This is handlers' primary use case.

2. Deferred execution - When you need an action to execute only after several prerequisite tasks have completed, and only if those tasks made changes.

3. Avoiding unnecessary operations - When an operation (like restarting a service) is potentially disruptive and should only occur when absolutely necessary.

4. Conditional execution based on changes - Handlers only run when notified by tasks that actually made changes (when a task's "changed" state is true).

That said, almost anything a handler can do could technically be accomplished with regular tasks using careful conditionals and flags, but it would be more complex and error-prone. Handlers provide a cleaner, more efficient way to handle these specific scenarios.

## Exercise: Working with Handlers

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

# Roles

## Introduction to Ansible Roles

Ansible roles are a way to group multiple tasks together into one container to do the work required to complete a portion of the overall objective. They provide a framework for fully independent, or interdependent collections of variables, tasks, files, templates, and modules.

Think of roles as reusable building blocks that can be used to simplify writing complex playbooks.

### Prerequisites

Before diving into this tutorial, you should:

- Have a basic understanding of Ansible concepts
- Be familiar with writing simple Ansible playbooks
- Have Ansible installed on your system (version 2.9 or later recommended)

## Why Use Roles?

Roles offer several advantages in Ansible automation:

1. **Modular structure**: Break down complex configurations into smaller, more manageable components
2. **Reusability**: Write a role once, use it across multiple playbooks and projects
3. **Organization**: Follow a standardized directory structure that simplifies navigation
4. **Sharing**: Easily share, distribute, and reuse your automation content
5. **Maintenance**: Update functionality in one place rather than multiple playbooks
6. **Collaboration**: Improve team efficiency by allowing different members to work on different roles
7. **Testing**: Test roles independently from playbooks

## Anatomy of an Ansible Role

A typical Ansible role follows a directory structure like this:

```
roles/
└── example_role/
    ├── defaults/     # Default variables (lowest precedence)
    │   └── main.yml
    ├── files/        # Static files to be deployed
    ├── handlers/     # Handler definitions
    │   └── main.yml
    ├── meta/         # Role metadata including dependencies
    │   └── main.yml
    ├── tasks/        # Core logic/tasks
    │   └── main.yml
    ├── templates/    # Jinja2 templates
    ├── tests/        # Role tests
    └── vars/         # Role variables (higher precedence)
        └── main.yml
```

Let's explore each directory:

### defaults/main.yml

Contains default variables for the role, which have the lowest precedence and can be easily overridden.

### files/

Contains static files that may be deployed using the `copy` module.

### handlers/main.yml

Contains handlers that may be triggered by tasks within the role.

### meta/main.yml

Contains metadata about the role, including dependencies, supported platforms, and Galaxy info.

### tasks/main.yml

The main list of tasks that the role executes.

### templates/

Contains Jinja2 templates that can be deployed using the `template` module.

### tests/

Contains tests for the role.

### vars/main.yml

Contains variables that typically shouldn't be overridden, having higher precedence than default variables.

## Creating Your First Role

Let's create a simple role that installs and configures Nginx web server.

### Step 1: Create the role directory structure

You can manually create the directory structure, but the `ansible-galaxy` command makes it easier:

```bash
ansible-galaxy init webserver
```

This creates a `webserver` role with the standard directory structure.

### Step 2: Define the role tasks

Edit `webserver/tasks/main.yml`:

```yaml
---
# tasks file for webserver
- name: Install Nginx
  package:
    name: nginx
    state: present
  become: true

- name: Ensure Nginx is running
  service:
    name: nginx
    state: started
    enabled: yes
  become: true

- name: Deploy website content
  template:
    src: index.html.j2
    dest: /var/www/html/index.html
  become: true
  notify: Restart Nginx
```

### Step 3: Create a handler

Edit `webserver/handlers/main.yml`:

```yaml
---
# handlers file for webserver
- name: Restart Nginx
  service:
    name: nginx
    state: restarted
  become: true
```

### Step 4: Create a template

Create `webserver/templates/index.html.j2`:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>{{ website_title }}</title>
  </head>
  <body>
    <h1>{{ website_title }}</h1>
    <p>Welcome to {{ website_title }}!</p>
    <p>This server is managed by Ansible.</p>
  </body>
</html>
```

### Step 5: Define default variables

Edit `webserver/defaults/main.yml`:

```yaml
---
# defaults file for webserver
website_title: 'My Awesome Website'
```

### Step 6: Create a playbook to use the role

Create `webserver_playbook.yml` in your project root:

```yaml
---
- hosts: webservers
  roles:
    - webserver
```

When you run this playbook, Ansible will:

1. Install Nginx
2. Start the Nginx service
3. Deploy the website content using your template
4. Restart Nginx if the content changes

## Role Variables

Variables in roles can be defined in multiple places:

1. `defaults/main.yml` - Default variables (lowest precedence)
2. `vars/main.yml` - Role variables (higher precedence)
3. In the playbook when including the role
4. In group_vars or host_vars
5. As command-line extra vars (highest precedence)

### Defining defaults

In `defaults/main.yml`:

```yaml
---
# Low precedence defaults
app_port: 8080
app_version: '1.2.3'
app_log_level: 'info'
```

### Defining variables

In `vars/main.yml`:

```yaml
---
# Higher precedence variables
app_user: 'app'
app_group: 'app'
app_temp_path: '/tmp/app'
```

### Overriding variables in a playbook

```yaml
---
- hosts: app_servers
  roles:
    - role: app_role
      vars:
        app_port: 9090
        app_log_level: 'debug'
```

### Variable precedence

If the same variable is defined in multiple places, the value with the highest precedence will be used.

## Role Dependencies

Roles can depend on other roles, creating a hierarchy of automation.

### Defining dependencies

In `meta/main.yml`:

```yaml
---
dependencies:
  - role: common
  - role: security
    vars:
      security_level: high
  - role: database
    when: deploy_database | bool
```

In this example, the `common` and `security` roles will always run before your role, while the `database` role will only run if the condition is met.

### Using allow_duplicates

By default, Ansible will only run a role once even if it's included multiple times. To override this:

```yaml
---
dependencies:
  - role: logging
    vars:
      log_component: 'api'
    allow_duplicates: yes
```

## Using Roles in Playbooks

There are multiple ways to use roles in playbooks:

### Basic inclusion

```yaml
---
- hosts: webservers
  roles:
    - webserver
    - database
    - monitoring
```

### Conditional roles

```yaml
---
- hosts: all
  roles:
    - { role: webserver, when: deploy_web | bool }
    - { role: database, when: deploy_db | bool }
```

### Roles with variables

```yaml
---
- hosts: all
  roles:
    - role: webserver
      vars:
        website_title: 'Custom Website'
        http_port: 8080
```

### Roles with tags

```yaml
---
- hosts: all
  roles:
    - role: webserver
      tags: ['web', 'nginx']
    - role: database
      tags: ['db', 'mysql']
```

This allows selective execution with `ansible-playbook playbook.yml --tags web`.

### Pre and post tasks

```yaml
---
- hosts: all
  pre_tasks:
    - name: Update apt cache
      apt: update_cache=yes
      when: ansible_os_family == "Debian"
  roles:
    - webserver
  post_tasks:
    - name: Run final verification
      command: verify_deployment.sh
```

### Using include_role

For dynamic role inclusion within tasks:

```yaml
---
- hosts: all
  tasks:
    - name: Check database type
      set_fact:
        db_type: "{{ 'mysql' if use_mysql else 'postgresql' }}"

    - name: Include database role
      include_role:
        name: '{{ db_type }}'
```
