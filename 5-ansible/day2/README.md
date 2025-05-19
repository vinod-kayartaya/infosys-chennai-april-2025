# Ansible Day 2 Training

## Table of Contents

1. [Ansible Inventory](#ansible-inventory)

   - [Core Concepts](#core-concepts-of-ansible-inventory)
   - [Inventory File Formats](#inventory-file-formats)
   - [Dynamic Inventory](#dynamic-inventory)
   - [Special Variables](#special-variables)
   - [Inventory Directory Structure](#inventory-directory-structure)
   - [Best Practices](#best-practices)

2. [Ansible Configuration File (ansible.cfg)](#ansible-configuration-file-ansiblecfg-explained)

   - [Configuration File Locations](#configuration-file-locations)
   - [Basic Structure](#basic-structure)
   - [Common Sections](#common-sections)
   - [Advanced Features](#advanced-features)
   - [Best Practices](#best-practices-1)
   - [Validation and Debugging](#validation-and-debugging)

3. [YAML Syntax](#yaml-syntax-basic)

   - [Basic YAML Rules](#basic-yaml-rules)
   - [YAML Best Practices](#yaml-best-practices)
   - [YAML Validation Tools](#yaml-validation-tools)
   - [Practice Exercises](#practice-exercises)
   - [Additional Resources](#additional-resources)

4. [Ansible Playbooks and Basic Operations](#ansible-playbooks-and-basic-operations)
   - [Introduction to Playbooks](#1-introduction-to-playbooks)
   - [Writing Your First Playbook](#2-writing-your-first-playbook)
   - [Variables in Ansible](#3-variables-in-ansible)
   - [Conditionals and Loops](#4-conditionals-and-loops)
   - [Handlers](#5-handlers)
   - [Conclusion and Next Steps](#conclusion-and-next-steps)

# Ansible Inventory

Ansible inventory is a critical component of Ansible automation that defines the hosts and groups you're managing with Ansible. It serves as a catalog of your infrastructure that Ansible uses to determine where and how to execute tasks.

## Core Concepts of Ansible Inventory

### Basic Structure

An inventory file defines hosts and groups in a simple text format. The default location is `/etc/ansible/hosts`, but you can specify a different inventory file using the `-i` flag when running Ansible commands.

The simplest inventory is a list of hostnames or IP addresses:

```ini
192.168.1.100
webserver.example.com
db01.example.com
```

### Groups

Hosts can be organized into groups, which allow you to apply configuration and run tasks on sets of servers:

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db01.example.com
db02.example.com
```

### Nested Groups

Groups can contain other groups using the `:children` suffix:

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db01.example.com
db02.example.com

[datacenter:children]
webservers
databases
```

### Host Variables

Variables can be assigned to individual hosts:

```ini
[webservers]
web1.example.com http_port=80 ansible_user=admin
web2.example.com http_port=8080 ansible_user=deployer
```

### Group Variables

Variables can be assigned to groups:

```ini
[webservers]
web1.example.com
web2.example.com

[webservers:vars]
http_port=80
ansible_user=admin
```

## Inventory File Formats

Ansible supports multiple inventory formats:

1. **INI format** - The traditional format shown in examples above
2. **YAML format** - More structured and supports complex data
3. **Dynamic inventory** - Scripts or plugins that generate inventory on the fly

### Example YAML Inventory

```yaml
all:
  hosts:
    mail.example.com:
  children:
    webservers:
      hosts:
        web1.example.com:
          http_port: 80
        web2.example.com:
          http_port: 8080
    databases:
      hosts:
        db01.example.com:
        db02.example.com:
```

## Dynamic Inventory

Dynamic inventory is crucial for cloud environments where servers are created and destroyed frequently. It uses scripts or plugins to query external sources (like AWS, Azure, GCP) to build the inventory in real-time.

### Common Dynamic Inventory Sources:

- Cloud providers (AWS, Azure, GCP)
- Infrastructure management tools (Terraform)
- Configuration management databases (CMDB)
- Service discovery systems (Consul, etcd)

## Special Variables

Ansible recognizes several special variables for controlling connection parameters:

- `ansible_host`: The hostname/IP to connect to
- `ansible_port`: The SSH port (default: 22)
- `ansible_user`: The username for SSH connections
- `ansible_password`: The password for SSH connections
- `ansible_connection`: Connection type (ssh, winrm, docker, etc.)
- `ansible_python_interpreter`: Path to Python on the target host

## Inventory Directory Structure

For more complex setups, you can use a directory structure:

```
inventory/
├── hosts               # Main inventory file
├── group_vars/
│   ├── all.yml         # Variables for all hosts
│   ├── webservers.yml  # Variables for webservers group
│   └── databases.yml   # Variables for databases group
└── host_vars/
    ├── web1.yml        # Variables for web1.example.com
    └── db01.yml        # Variables for db01.example.com
```

## Best Practices

1. **Use version control** for your inventory files
2. **Separate variables** from host definitions using group_vars and host_vars
3. **Group meaningfully** by function, location, and environment
4. **Use meaningful aliases** for hosts with long or complex names
5. **Document your inventory structure** for team members
6. **Test inventory** with `ansible-inventory --list` to verify structure

# Ansible Configuration File (ansible.cfg) Explained

The `ansible.cfg` file is Ansible's configuration file that controls its behavior. It provides a way to set default options so you don't have to specify them on the command line or in environment variables every time you run Ansible commands.

## Configuration File Locations

Ansible looks for configurations in the following order (first found wins):

1. `ANSIBLE_CONFIG` environment variable (if set to a file path)
2. `ansible.cfg` in the current directory
3. `~/.ansible.cfg` (in the user's home directory)
4. `/etc/ansible/ansible.cfg` (system-wide default)

## Basic Structure

The `ansible.cfg` file uses an INI-style format with sections in square brackets:

```ini
[defaults]
inventory = ./inventory
remote_user = deploy
host_key_checking = False

[privilege_escalation]
become = True
become_method = sudo
```

## Common Sections

### [defaults]

This is the most commonly used section that controls Ansible's core behavior:

```ini
[defaults]
# Inventory file location
inventory = ./inventory

# Default remote user
remote_user = ansible

# Disable SSH host key checking (not recommended for production)
host_key_checking = False

# Number of parallel processes for executing commands
forks = 10

# Set the default timeout for connections
timeout = 30

# Set path for custom Ansible module development
library = ./library

# Define location for roles
roles_path = ./roles:/usr/share/ansible/roles

# Path to the vault password file
vault_password_file = ~/.vault_pass

# Default log path
log_path = ./ansible.log

# Set the default callback
stdout_callback = yaml

# Show elapsed time and timing information
callback_whitelist = timer, profile_tasks

# Control fact gathering
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 86400
```

### [privilege_escalation]

Controls how Ansible escalates privileges on target hosts:

```ini
[privilege_escalation]
# Enable privilege escalation by default
become = True

# Method used for privilege escalation
become_method = sudo

# User to become
become_user = root

# Ask for sudo password
become_ask_pass = False
```

### [ssh_connection]

Configures how SSH connections are handled:

```ini
[ssh_connection]
# Enable SSH pipelining for improved performance
pipelining = True

# Set SSH arguments
ssh_args = -o ControlMaster=auto -o ControlPersist=60s

# Control how many SSH connections to keep alive
control_path_dir = ~/.ansible/cp
control_path = %(directory)s/%%h-%%r

# Transfer files using SCP instead of SFTP
scp_if_ssh = True

# Compression settings
sftp_batch_mode = True
```

### [persistent_connection]

Settings for persistent connections:

```ini
[persistent_connection]
connect_timeout = 30
connect_retries = 5
connect_interval = 1
```

### [paramiko_connection]

Configuration for Paramiko SSH connections:

```ini
[paramiko_connection]
record_host_keys = False
look_for_keys = False
```

### [colors]

Customizes Ansible's console output colors:

```ini
[colors]
highlight = white
verbose = blue
warn = bright purple
error = red
debug = dark gray
deprecate = purple
skip = cyan
unreachable = red
ok = green
changed = yellow
```

## Advanced Features

### Environment Variable Configuration

Most `ansible.cfg` options can be overridden with environment variables using the format `ANSIBLE_*`:

```bash
export ANSIBLE_INVENTORY=./custom-inventory
export ANSIBLE_FORKS=20
```

### Vault Configuration

Control how Ansible Vault behaves:

```ini
[defaults]
vault_password_file = ~/.vault_pass

[vault]
vault_identity = production
vault_identity_list = dev@~/.dev_vault_pass, prod@~/.prod_vault_pass
```

### Plugin Settings

Configure various plugins:

```ini
[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml

[callback_log_plays]
log_folder = /var/log/ansible/hosts
```

## Best Practices

1. **Version control your ansible.cfg** alongside your playbooks and roles
2. **Use a project-specific ansible.cfg** in your playbook directory
3. **Document custom settings** with comments
4. **Keep security in mind** - be careful with host_key_checking and other security-related settings
5. **Override selectively** - only configure values that differ from defaults
6. **Use include directives** for more complex setups:

```ini
[defaults]
inventory = ./inventory
remote_user = deploy

# Include additional configuration
inventory_includes_directory = ./inventory.d/
config_file = ./ansible.advanced.cfg
```

## Validation and Debugging

You can validate your configuration with:

```bash
ansible-config dump --only-changed
```

To see all configurations (including defaults):

```bash
ansible-config list
```

To see where a specific setting comes from:

```bash
ansible-config dump --only-changed -t all
```
