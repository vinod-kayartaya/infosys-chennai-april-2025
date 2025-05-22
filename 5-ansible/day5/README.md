# Ansible Roles

## Introduction

Ansible roles are a way to group multiple tasks together into one container to do the work required to complete a portion of the overall objective. They provide a framework for fully independent, or interdependent collections of variables, tasks, files, templates, and modules.

Think of roles as reusable building blocks that can be used to simplify writing complex playbooks.

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

## Advanced Role Techniques

### Role import vs include

- `import_role`: Static import at playbook parsing time
- `include_role`: Dynamic include at runtime

```yaml
# Static import
- import_role:
    name: webserver
  tags: [web] # Tags apply to all tasks in the role

# Dynamic include
- include_role:
    name: webserver
  tags: [web] # Tags only apply to the include itself
```

### Execution control with tags and conditionals

```yaml
- import_role:
    name: security
  tags: [security]
  when: enhance_security | bool
```

### Using role defaults

```yaml
- hosts: all
  roles:
    - role: app
      vars:
        app_port: '{{ app_port | default(8080) }}'
```

### Private roles

Create a `tasks/private_tasks.yml` file with tasks you don't want to execute automatically, then include it from `main.yml` as needed:

```yaml
# In tasks/main.yml
- name: Include private tasks if needed
  include_tasks: private_tasks.yml
  when: run_private_tasks | bool
```

## Role Best Practices

1. **Write focused roles**: Each role should do one thing well
2. **Document your roles**: Include a README.md in each role
3. **Use meaningful names**: Choose descriptive names for roles, variables, and tasks
4. **Default values**: Provide sensible defaults but make them easy to override
5. **Idempotent execution**: Ensure roles can run multiple times without problems
6. **Test your roles**: Write tests using Molecule or other testing frameworks
7. **Version control**: Maintain your roles in a version control system
8. **Use conditionals**: Make roles adaptable to different environments
9. **Performance**: Use tags to allow selective execution of role parts
10. **Follow naming conventions**:
    - Variables: `role_name_variable_name`
    - Tasks: Use clear, action-oriented descriptions

### Documentation example

Create a `README.md` file in your role directory:

<pre>
# Webserver Role

This role installs and configures Nginx web server with a customizable homepage.

## Requirements

- Ansible 2.9 or higher
- Root access on target hosts

## Role Variables

| Variable      | Description           | Default              |
| ------------- | --------------------- | -------------------- |
| website_title | Title for the website | "My Awesome Website" |
| http_port     | Port for HTTP traffic | 80                   |

## Dependencies

- common

## Example Playbook

```yaml
- hosts: webservers
  roles:
    - role: webserver
      vars:
        website_title: 'Custom Website'
```
````

## License

MIT

## Author Information

Your Name <your.email@example.com>

</pre>

## Ansible Galaxy

Ansible Galaxy is a hub for sharing and discovering Ansible roles.

### Finding roles

```bash
# Search for a role
ansible-galaxy search nginx

# Get more information about a role
ansible-galaxy info geerlingguy.nginx
```

### Installing roles

```bash
# Install a role
ansible-galaxy install geerlingguy.nginx

# Install multiple roles from a requirements file
ansible-galaxy install -r requirements.yml
```

Example `requirements.yml`:

```yaml
---
- src: geerlingguy.nginx
  version: 2.8.0
  name: nginx

- src: https://github.com/username/ansible-role-redis
  scm: git
  version: master
  name: redis
```

### Publishing your own roles

1. Create a GitHub repository for your role
2. Ensure your role has proper metadata in `meta/main.yml`
3. Submit it to Galaxy via the web interface or API

### Sharing roles within your organization

For private roles, consider:

- Private GitHub repositories
- Setting up your own Galaxy server
- Using Ansible Automation Platform

# Ansible Vault: Managing Sensitive Data

## Introduction

When automating infrastructure with Ansible, you'll often need to handle sensitive data like passwords, API keys, and certificates. Storing these as plaintext in your playbooks or variable files creates security risks, especially when sharing code via version control systems like Git.

Ansible Vault provides a solution by allowing you to encrypt:

- Entire YAML files containing sensitive data
- Specific strings within larger files
- Structured data (like dictionaries and lists)

This tutorial will guide you through using Ansible Vault effectively to protect sensitive information while maintaining the flexibility and power of your Ansible automation.

## Basic Concepts

### What is Ansible Vault?

Ansible Vault is a feature that encrypts files and strings, preventing sensitive data from being exposed. It uses AES256 encryption to protect your data, requiring a password for decryption during playbook execution.

### Key Terms

- **Vault**: The encryption mechanism in Ansible
- **Vault password**: Secret key used for encryption/decryption
- **Vault ID**: Optional label for different vault passwords
- **Encrypted file**: A file completely encrypted with Ansible Vault
- **Encrypted string**: A single value encrypted within a larger file

## Getting Started with Ansible Vault

### Creating Your First Encrypted File

Let's create an encrypted file containing database credentials:

1. Create a new file with sensitive variables:

```bash
touch db_credentials.yml
```

2. Add some sensitive data to this file:

```yaml
# db_credentials.yml
db_user: admin
db_password: supersecret123
db_host: database.example.com
db_name: production_db
```

3. Encrypt the file using Ansible Vault:

```bash
ansible-vault encrypt db_credentials.yml
```

4. Enter and confirm a vault password when prompted.

The file is now encrypted and will appear as something like:

```
$ANSIBLE_VAULT;1.1;AES256
32613431303636323539323637623763336461653966353164623830383662316639383739666266
3362373564363338363764376637653537643834343563390a353036346338633839636134633861
65316236363635363435356633323461333631363866646638663530656432313935373033376536
3738626261313933360a376465343039356638336461393162383733376630366532623333633864
64376332666334396534333339353566343639396661383736633863393537636338
```

### Viewing Encrypted Files

To view the contents of an encrypted file:

```bash
ansible-vault view db_credentials.yml
```

Enter your vault password when prompted.

### Editing Encrypted Files

To edit an encrypted file:

```bash
ansible-vault edit db_credentials.yml
```

This command decrypts the file, opens it in your default editor, and re-encrypts it when you save and exit.

## Working with Encrypted Files

### Using Encrypted Files in Playbooks

You can use encrypted files just like any other variable file in Ansible:

```yaml
# example_playbook.yml
- name: Configure database
  hosts: database_servers
  vars_files:
    - db_credentials.yml # This file is encrypted

  tasks:
    - name: Create database user
      mysql_user:
        name: '{{ db_user }}'
        password: '{{ db_password }}'
        host: '{{ db_host }}'
        priv: '{{ db_name }}.*:ALL'
        state: present
```

### Running Playbooks with Vault Files

When running a playbook that uses encrypted files, you need to provide the vault password:

```bash
# Method 1: Enter password interactively
ansible-playbook example_playbook.yml --ask-vault-pass

# Method 2: Use a password file (be careful with this!)
echo "your_vault_password" > ~/.vault_pass.txt
chmod 600 ~/.vault_pass.txt
ansible-playbook example_playbook.yml --vault-password-file ~/.vault_pass.txt
```

### Decrypting Files

To decrypt a file when you no longer need encryption:

```bash
ansible-vault decrypt db_credentials.yml
```

You'll be prompted for the vault password.

## Working with Encrypted Strings

Sometimes you only need to encrypt specific variables within a file, rather than the entire file.

### Encrypting Individual Strings

Ansible 2.3+ supports encrypting individual values:

```bash
ansible-vault encrypt_string 'supersecret123' --name 'db_password'
```

This command produces output like:

```yaml
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  35623431303636323539323637623763336461653966353164623830383662316639383739666266
  3362373564363338363764376637653537643834343563390a353036346338633839636134633861
  65316236363635363435356633323461333631363866646638663530656432313935373033376536
  3738626261313933360a376465343039356638336461393162383733376630366532623333633864
  64376332666334396534333339353566343639396661383736633863393537636338
```

### Using Encrypted Strings in Variable Files

You can include the encrypted output in any YAML file:

```yaml
# partial_encryption.yml
db_user: admin
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  35623431303636323539323637623763336461653966353164623830383662316639383739666266
  3362373564363338363764376637653537643834343563390a353036346338633839636134633861
  65316236363635363435356633323461333631363866646638663530656432313935373033376536
  3738626261313933360a376465343039356638336461393162383733376630366532623333633864
  64376332666334396534333339353566343639396661383736633863393537636338
db_host: database.example.com
db_name: production_db
```

This way, only the password is encrypted while the rest of the file remains readable.

### Creating Encrypted Variables Directly to File

You can encrypt a string and append it directly to a file:

```bash
ansible-vault encrypt_string 'supersecret123' --name 'api_key' >> credentials.yml
```

## Best Practices

### Password Management

Good vault password practices:

1. **Use strong passwords**: Complex, long passwords increase security.

2. **Don't store passwords in plain text**: Avoid storing vault passwords in scripts or unencrypted files.

3. **Consider using a password manager**: Tools like LastPass, 1Password, or Bitwarden can generate and store complex passwords securely.

4. **Rotate passwords periodically**: Change vault passwords regularly, especially after team member departures.

### File Organization

Best practices for organizing encrypted files:

1. **Group sensitive variables**: Keep sensitive data in dedicated files separate from non-sensitive configuration.

2. **Use clear naming conventions**: Names like `group_vars/production/vault.yml` clearly indicate encrypted content.

3. **Documentation**: Document which variables are encrypted and their purpose (without revealing the actual values).

Example directory structure:

```
ansible-project/
├── group_vars/
│   ├── all/
│   │   ├── vars.yml          # Non-sensitive variables
│   │   └── vault.yml         # Encrypted sensitive variables
│   ├── production/
│   │   ├── vars.yml          # Non-sensitive production variables
│   │   └── vault.yml         # Encrypted production secrets
│   └── development/
│       ├── vars.yml          # Non-sensitive development variables
│       └── vault.yml         # Encrypted development secrets
├── host_vars/
│   └── critical-server/
│       ├── vars.yml          # Non-sensitive host variables
│       └── vault.yml         # Encrypted host secrets
├── playbooks/
└── ansible.cfg
```

### Version Control Considerations

When using version control:

1. **Always commit encrypted files**: It's safe to commit properly encrypted files.

2. **Never commit unencrypted sensitive data**: Double-check before committing.

3. **Don't commit vault passwords**: Add password files to `.gitignore`.

4. **Be cautious with history**: Remember that if sensitive data was ever committed unencrypted, it remains in the Git history.

## Integration with Playbooks

### Vault Configuration in ansible.cfg

You can configure vault settings in your `ansible.cfg` file:

```ini
[defaults]
vault_password_file = ~/.vault_pass.txt
# OR for vault-id
vault_identity_list = production@~/.vault_pass_prod.txt, development@~/.vault_pass_dev.txt
```

### Using Environment Variables

You can also use environment variables for vault passwords:

```bash
export ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass.txt
ansible-playbook example_playbook.yml
```

### Using vault-id

For more advanced setups with multiple passwords:

```bash
# Create an encrypted file with a specific ID
ansible-vault encrypt --vault-id production@prompt db_credentials.yml

# Run a playbook with multiple vault IDs
ansible-playbook example_playbook.yml --vault-id production@prompt --vault-id development@~/.dev_vault_pass.txt
```

## Multiple Vault Passwords

As projects grow, you might need different vault passwords for different environments or teams.

### Creating Files with Different Vault IDs

```bash
# Create files for different environments
ansible-vault encrypt --vault-id dev@prompt dev_secrets.yml
ansible-vault encrypt --vault-id prod@prompt prod_secrets.yml
```

### Rekey: Changing Vault Passwords

To change the password of an encrypted file:

```bash
# Interactive method
ansible-vault rekey db_credentials.yml

# Specifying vault IDs
ansible-vault rekey --vault-id old@prompt --new-vault-id new@prompt db_credentials.yml
```

### Using Multiple Vault Passwords in Playbooks

```yaml
# example_playbook.yml
- name: Configure environments
  hosts: all
  vars_files:
    - '{{ env }}_secrets.yml' # Could be dev_secrets.yml or prod_secrets.yml

  tasks:
    - name: Deploy application
      # tasks here
```

Run with:

```bash
ansible-playbook example_playbook.yml --vault-id dev@prompt --vault-id prod@prompt -e "env=dev"
```

## Real-World Examples

### Example 1: Database Configuration

```yaml
# group_vars/database_servers/vault.yml (encrypted)
mysql_root_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  62383964323964633566336165383732303438393538626666353263353631653766666634636665
  3661393334646162383732323036366236316636333834350a323832303438313835353566343033
  35366266366664346566376138313563323863623139363965663933613062393461353664613738
  6436356663326566650a393938363139316566306438393730663866613038326235316338303763
  3161

# group_vars/database_servers/vars.yml (not encrypted)
mysql_port: 3306
mysql_bind_address: 0.0.0.0
mysql_databases:
  - name: app_database
    encoding: utf8mb4
    collation: utf8mb4_unicode_ci
```

Playbook using these variables:

```yaml
# database_setup.yml
- name: Configure MySQL servers
  hosts: database_servers
  become: yes

  tasks:
    - name: Set MySQL root password
      mysql_user:
        name: root
        password: '{{ mysql_root_password }}'
        host_all: yes
        state: present
      no_log: true # Prevents password from appearing in logs

    - name: Create application databases
      mysql_db:
        name: '{{ item.name }}'
        encoding: "{{ item.encoding | default('utf8') }}"
        collation: "{{ item.collation | default('utf8_general_ci') }}"
        state: present
      loop: '{{ mysql_databases }}'
```

### Example 2: SSL Certificate Management

```yaml
# group_vars/webservers/vault.yml (encrypted)
ssl_private_key: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  31616338613365366462633831303336303031396233313938316231303030363661373134646534
  3765303862323530623435343064656261383262663264660a343934316434636139356663623632
  61616662333535343565653433353636356362373365373335386138346134626332353663316661
  3230626161613232380a623162626461316632306134626566363965333431353832623633386138
  6639

ssl_certificate: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  36303364363165653664646265343264313866333832646666383737646466383664613065383461
  3933383734383934383764626664623039383930343837630a333836633835323832623633383433
  31373237653837353731663136363135383534656438633237636437356237653263353234656136
  6463313164343834380a363732393565626466363163316436656664383965383834306432383433
  3337
```

Playbook for deploying certificates:

```yaml
# ssl_setup.yml
- name: Configure SSL certificates
  hosts: webservers
  become: yes

  tasks:
    - name: Ensure SSL directory exists
      file:
        path: /etc/nginx/ssl
        state: directory
        mode: '0700'

    - name: Copy SSL private key
      copy:
        content: '{{ ssl_private_key }}'
        dest: /etc/nginx/ssl/server.key
        mode: '0600'
      no_log: true

    - name: Copy SSL certificate
      copy:
        content: '{{ ssl_certificate }}'
        dest: /etc/nginx/ssl/server.crt
        mode: '0644'

    - name: Restart Nginx
      service:
        name: nginx
        state: restarted
```

### Example 3: API Credential Management

```yaml
# group_vars/all/vault.yml (encrypted)
api_credentials:
  github:
    token: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      32383637323562373830393235633536313738623466323666323430353636663836636137626537
      3130353632626165383364353635626332373862333439350a646365316462323337333531633838
      31616331636363306661666335333361363563333933363264623638646338633238333663323632
      3038313164333566390a653164623839633732376138653763373462393164393661323337313034
      6539
  aws:
    access_key: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      63313438393936613439353666393131313362333764613363343634653964613338663737636665
      6135383762343232326466653664396230366534653430380a313035323262633664363662383933
      30303866343962356333653862333235323962306236326633626265633966633031386137653861
      3733376435626538620a326235353464653064376531656337383332353934633764653538316463
      6335
    secret_key: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      39613866613564333538663739646366656565653339613563326266303239623665636534666161
      3462336139383863353632323536633634386465643435310a326234636666633666333462346438
      32313834626664386233333133306433356563396536633134303536356337326338383366323631
      3539343534663338310a336238333465633438613932386131363332643436633366316161633661
      35623661623562643366326134353366653066346539646130616663383765633838
```

Playbook using these API credentials:

```yaml
# deploy_application.yml
- name: Deploy application with API integrations
  hosts: application_servers

  tasks:
    - name: Clone repository using GitHub token
      git:
        repo: 'https://{{ api_credentials.github.token }}@github.com/organization/repo.git'
        dest: /var/www/app
        version: main
      no_log: true

    - name: Configure AWS credentials
      template:
        src: aws_credentials.j2
        dest: /home/app_user/.aws/credentials
        mode: '0600'
        owner: app_user
        group: app_user
      vars:
        aws_access_key: '{{ api_credentials.aws.access_key }}'
        aws_secret_key: '{{ api_credentials.aws.secret_key }}'
      no_log: true
```

With template `aws_credentials.j2`:

```
[default]
aws_access_key_id = {{ aws_access_key }}
aws_secret_access_key = {{ aws_secret_key }}
```

## Troubleshooting

### Common Issues and Solutions

#### 1. "Decryption failed"

**Symptoms:** You see an error like "Decryption failed" when trying to use an encrypted file.

**Solutions:**

- Verify you're using the correct vault password
- Check if the file was encrypted with a different vault ID
- Make sure the file hasn't been corrupted

#### 2. "ERROR! The vault password file... was not found"

**Symptoms:** Ansible can't find your vault password file.

**Solutions:**

- Verify the file path is correct
- Check file permissions
- Ensure the file exists

#### 3. Password prompts when not expected

**Symptoms:** Ansible keeps asking for your vault password even though you've specified a password file.

**Solutions:**

- Check your `ansible.cfg` configuration
- Verify the `--vault-password-file` path
- Ensure the file contains just the password without extra newlines or spaces

### Debugging Vault Issues

Add verbosity to see more details about what's happening:

```bash
ansible-playbook example_playbook.yml --ask-vault-pass -vvv
```

## Advanced Topics

### Vault and CI/CD Pipelines

Integrating Ansible Vault with CI/CD systems:

1. **Environment variables**: Store the vault password as a secure environment variable.

```bash
# In your CI/CD pipeline
export ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass.txt
echo "${VAULT_PASSWORD}" > ~/.vault_pass.txt
chmod 600 ~/.vault_pass.txt
ansible-playbook deploy.yml
```

2. **Vault password scripts**: Use a script that retrieves the password from a secure source.

```python
#!/usr/bin/env python
# vault_pass.py
import os
import sys
# Get password from environment or secure storage
password = os.environ.get('VAULT_PASSWORD', '')
sys.stdout.write(password)
```

Make it executable and use it:

```bash
chmod +x vault_pass.py
ansible-playbook deploy.yml --vault-password-file ./vault_pass.py
```

### Using HashiCorp Vault with Ansible Vault

You can integrate HashiCorp Vault with Ansible Vault using a script:

```python
#!/usr/bin/env python
# hashicorp_vault_script.py
import hvac
import os
import sys

# Configure HashiCorp Vault client
client = hvac.Client(url=os.environ['VAULT_ADDR'])
client.token = os.environ['VAULT_TOKEN']

# Retrieve the Ansible Vault password from HashiCorp Vault
response = client.secrets.kv.v2.read_secret_version(
    path='ansible/vault_password',
    mount_point='secret'
)

password = response['data']['data']['password']
sys.stdout.write(password)
```

### Vault and Custom Encryption Methods

While Ansible Vault uses AES256 by default, you can create custom encryption methods by implementing a script that handles encryption and decryption.

# Jinja Templates in Ansible

## Introduction

Jinja is a powerful templating engine used extensively in Ansible for dynamic content generation. It allows you to create flexible playbooks and configuration files that adapt to different environments and system characteristics.

This tutorial uses facts gathered from a target called `web_server1` to demonstrate all Jinja features in practical scenarios.

Before diving into Jinja templates, let's understand the structure of Ansible facts. When Ansible runs the `setup` module (automatically or explicitly), it gathers comprehensive information about the target system.

### Sample Facts Structure for web_server1

```yaml
ansible_facts:
  ansible_hostname: web_server1
  ansible_fqdn: web_server1.company.com
  ansible_os_family: Debian
  ansible_distribution: Ubuntu
  ansible_distribution_version: '22.04'
  ansible_architecture: x86_64
  ansible_processor_count: 2
  ansible_processor_cores: 3
  ansible_processor_threads_per_core: 1
  ansible_memtotal_mb: 7892
  ansible_interfaces:
    - lo
    - eth0
    - eth1
  ansible_eth0:
    ipv4:
      address: 192.168.1.100
      netmask: 255.255.255.0
    macaddress: 00:50:56:12:34:56
  ansible_mounts:
    - mount: /
      device: /dev/sda1
      fstype: xfs
      size_total: 107374182400
    - mount: /var
      device: /dev/sda2
      fstype: xfs
      size_total: 53687091200
  ansible_service_mgr: systemd
  ansible_user_id: root
  ansible_env:
    PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
    HOME: /root
```

---

## Basic Jinja Syntax

Jinja uses three types of delimiters:

- `{{ }}` - Expressions (for output)
- `{% %}` - Statements (for control structures)
- `{# #}` - Comments

### Example: Basic Template

```jinja2
{# This is a comment - Server configuration template #}
Server Name: {{ ansible_hostname }}
IP Address: {{ ansible_default_ipv4.address }}
Operating System: {{ ansible_distribution }} {{ ansible_distribution_version }}
```

**Output:**

```
Server Name: web_server1
IP Address: 192.168.1.100
Operating System: CentOS 8.4
```

---

## Variable Substitution

### Simple Variable Access

```jinja2
Hostname: {{ ansible_hostname }}
FQDN: {{ ansible_fqdn }}
Architecture: {{ ansible_architecture }}
```

### Dictionary Access

```jinja2
{# Two ways to access dictionary values #}
IP Address (dot notation): {{ ansible_default_ipv4.address }}
IP Address (bracket notation): {{ ansible_default_ipv4['address'] }}

{# Bracket notation is useful for dynamic keys #}
{% set interface_name = 'eth0' %}
Interface IP: {{ ansible_facts[interface_name]['ipv4']['address'] }}
```

### Default Values

```jinja2
{# Using default filter for missing values #}
Web Port: {{ web_port | default(80) }}
SSL Port: {{ ssl_port | default(443) }}
Database Host: {{ db_host | default('localhost') }}

{# Using default with boolean check #}
Service Status: {{ service_enabled | default(false) }}
```

---

## Control Structures

### Conditional Statements

#### Simple If Statement

```jinja2
{% if ansible_os_family == "RedHat" %}
Package Manager: yum/dnf
Firewall: firewalld
{% elif ansible_os_family == "Debian" %}
Package Manager: apt
Firewall: ufw
{% else %}
Package Manager: unknown
Firewall: unknown
{% endif %}
```

#### Complex Conditions

```jinja2
{% if ansible_memtotal_mb >= 8192 and ansible_processor_cores >= 4 %}
Server Class: High Performance
Recommended Services: Database, Application Server
{% elif ansible_memtotal_mb >= 4096 and ansible_processor_cores >= 2 %}
Server Class: Medium Performance
Recommended Services: Web Server, Caching
{% else %}
Server Class: Basic
Recommended Services: Static Content, Monitoring
{% endif %}
```

#### Checking Variable Existence

```jinja2
{% if ansible_virtualization_type is defined %}
Virtualization: {{ ansible_virtualization_type }}
{% else %}
Virtualization: Physical Server
{% endif %}

{% if 'docker' in ansible_facts %}
Docker Status: Available
{% else %}
Docker Status: Not Installed
{% endif %}
```

### Loops

#### Simple Loop

```jinja2
Network Interfaces:
{% for interface in ansible_interfaces %}
- {{ interface }}
{% endfor %}
```

**Output:**

```
Network Interfaces:
- lo
- eth0
- eth1
```

#### Loop with Conditions

```jinja2
Active Network Interfaces:
{% for interface in ansible_interfaces %}
{% if interface != 'lo' and ansible_facts[interface]['active'] %}
- Interface: {{ interface }}
  IP: {{ ansible_facts[interface]['ipv4']['address'] | default('No IP') }}
  MAC: {{ ansible_facts[interface]['macaddress'] | default('No MAC') }}
{% endif %}
{% endfor %}
```

#### Loop with Dictionary

```jinja2
Mount Points:
{% for mount in ansible_mounts %}
- Path: {{ mount.mount }}
  Device: {{ mount.device }}
  Filesystem: {{ mount.fstype }}
  Size: {{ (mount.size_total / 1024 / 1024 / 1024) | round(2) }} GB
  Usage: {{ ((mount.size_total - mount.size_available) / mount.size_total * 100) | round(1) }}%
{% endfor %}
```

#### Loop Variables

```jinja2
System Information Summary:
{% for key, value in ansible_facts.items() %}
{% if loop.index <= 5 %}
{{ loop.index }}. {{ key }}: {{ value }}
{% endif %}
{% endfor %}

{# Loop variables available:
   loop.index - 1-based counter
   loop.index0 - 0-based counter
   loop.first - True for first iteration
   loop.last - True for last iteration
   loop.length - Total iterations
#}
```

#### Nested Loops

```jinja2
Network Configuration:
{% for interface in ansible_interfaces %}
{% if interface != 'lo' %}
Interface: {{ interface }}
{% if ansible_facts[interface]['ipv4'] is defined %}
  IPv4 Addresses:
  {% for addr in ansible_facts[interface]['ipv4_secondaries'] | default([ansible_facts[interface]['ipv4']]) %}
    - {{ addr.address }}/{{ addr.netmask }}
  {% endfor %}
{% endif %}
{% endif %}
{% endfor %}
```

---

## Filters

Filters transform variables and are applied using the pipe (`|`) operator.

### String Filters

```jinja2
Hostname Upper: {{ ansible_hostname | upper }}
Hostname Lower: {{ ansible_hostname | lower }}
Hostname Title: {{ ansible_hostname | title }}

{# String manipulation #}
OS Info: {{ ansible_distribution | replace('CentOS', 'Community Enterprise OS') }}
Short Hostname: {{ ansible_fqdn | regex_replace('^([^.]+).*', '\\1') }}

```

### Numeric Filters

```jinja2
{# Memory calculations #}
Memory (MB): {{ ansible_memtotal_mb }}
Memory (GB): {{ (ansible_memtotal_mb / 1024) | round(2) }}
Memory (GB, rounded): {{ (ansible_memtotal_mb / 1024) | round | int }}

{# Disk space calculations #}
{% for mount in ansible_mounts %}
{{ mount.mount }} - {{ (mount.size_total / 1024**3) | round(1) }}GB
{% endfor %}
```

### List Filters

```jinja2
{# List operations #}
Total Interfaces: {{ ansible_interfaces | length }}
First Interface: {{ ansible_interfaces | first }}
Last Interface: {{ ansible_interfaces | last }}
Sorted Interfaces: {{ ansible_interfaces | sort | join(', ') }}

{# Filtering lists #}
Non-Loopback Interfaces: {{ ansible_interfaces | reject('equalto', 'lo') | list | join(', ') }}

{# Unique values #}
{% set all_filesystems = [] %}
{% for mount in ansible_mounts %}
{% set _ = all_filesystems.append(mount.fstype) %}
{% endfor %}
Unique Filesystems: {{ all_filesystems | unique | join(', ') }}
```

---

## Tests

Tests check variables and return boolean values.

### Common Tests

```jinja2
{# Testing variable states #}
{% if ansible_hostname is defined %}
Hostname is defined: {{ ansible_hostname }}
{% endif %}

{% if custom_variable is undefined %}
Custom variable is not set
{% endif %}

{% if ansible_memtotal_mb is number %}
Memory is numeric: {{ ansible_memtotal_mb }}MB
{% endif %}

{% if ansible_interfaces is iterable %}
Interfaces can be looped: {{ ansible_interfaces | join(', ') }}
{% endif %}
```

### String Tests

```jinja2
{% if ansible_hostname is match('web.*') %}
This is a web server
{% endif %}

{% if ansible_fqdn is search('company.com') %}
This server belongs to company.com domain
{% endif %}

{% if ansible_distribution is in ['CentOS', 'RedHat', 'Fedora'] %}
This is a RedHat-based system
{% endif %}
```

### Numeric Tests

```jinja2
{% if ansible_processor_cores is divisibleby(2) %}
Even number of CPU cores: {{ ansible_processor_cores }}
{% endif %}

{% if ansible_memtotal_mb is gt(4096) %}
High memory system (>4GB)
{% elif ansible_memtotal_mb is lt(2048) %}
Low memory system (<2GB)
{% else %}
Medium memory system
{% endif %}
```
