# Practice Exercises

To reinforce what you've learned, try these exercises:

1. Create a playbook that sets up a complete LAMP stack (Linux, Apache, MySQL, PHP)
2. Extend the playbook to deploy a simple PHP application
3. Use different variables for development and production environments
4. Implement error handling for when services fail to start

This guide provides the necessary Ansible modules and Linux commands to complete this exercise.

## Target Environment

- **Operating System**: Ubuntu
- **Connection Method**: SSH

## Essential Ansible Modules

### Package Management

- `apt`: Install, update, or remove packages via apt
- `package`: Generic package manager (useful for cross-platform playbooks)
- `apt_repository`: Add or remove APT repositories

### Service Management

- `service`: Control system services
- `systemd`: Manage systemd services
- `reboot`: Reboot target host (if needed)

### File Management

- `file`: Set file attributes, create directories
- `copy`: Copy files from local to remote
- `lineinfile`: Ensure specific lines are in files
- `blockinfile`: Insert/update/remove multi-line blocks

### Database Management

- `mysql_db`: Create/drop MySQL databases
- `mysql_user`: Add/remove MySQL users and manage privileges
- `mysql_query`: Execute MySQL queries

### Web Server Management

- `apache2_module`: Enable/disable Apache modules
- `apache2_site`: Enable/disable Apache sites
- `uri`: Interact with web services and test pages

### Command Execution

- `command`: Execute commands on target
- `shell`: Execute shell commands (when you need pipes, redirects)
- `script`: Run local scripts on remote nodes

### Error Handling

- `fail`: Force a task to fail and provide message
- `debug`: Print debug messages
- `assert`: Assert conditions are met
- `rescue`: Add error handling to task blocks
- `ignore_errors`: Allow playbook to continue despite errors

## Essential Linux Commands

### Package Management

- `apt update`: Update package lists
- `apt install <package>`: Install packages
- `apt upgrade`: Upgrade installed packages
- `dpkg -l`: List installed packages
- `apt-cache search <keyword>`: Search for packages

### Apache

- `apache2ctl -t`: Test Apache configuration
- `apache2ctl -M`: List loaded Apache modules
- `a2enmod <module>`: Enable Apache module
- `a2dismod <module>`: Disable Apache module
- `a2ensite <site>`: Enable Apache site
- `a2dissite <site>`: Disable Apache site

### MySQL/MariaDB

- `mysql -u <user> -p`: Connect to MySQL
- `mysqladmin`: Administrative utility
- `mysql_secure_installation`: Secure MySQL installation
- `mysqlshow`: Show databases, tables, columns
- `mysqldump`: Create database backups

### PHP

- `php -v`: Check PHP version
- `php -m`: List loaded PHP modules
- `php -i`: PHP information
- `php -l <file>`: Syntax check on file

### Service Management

- `systemctl start <service>`: Start service
- `systemctl stop <service>`: Stop service
- `systemctl restart <service>`: Restart service
- `systemctl status <service>`: Check service status
- `systemctl enable <service>`: Enable service at boot
- `systemctl disable <service>`: Disable service at boot
- `journalctl -u <service>`: View service logs

### File Management

- `ls -la`: List all files with details
- `find / -name <filename>`: Find files
- `chmod <permissions> <file>`: Change file permissions
- `chown <user>:<group> <file>`: Change file ownership
- `mkdir -p <dir>`: Create directory (with parents)
- `rm -rf <dir>`: Remove directory recursively

### Log Files

- `/var/log/apache2/error.log`: Apache error log
- `/var/log/apache2/access.log`: Apache access log
- `/var/log/mysql/error.log`: MySQL error log
- `/var/log/syslog`: System log

## Example Directory Structure

```
lamp_stack/
├── inventory/
│   ├── hosts
│   └── group_vars/
│       └── all.yml
├── files/
│   └── webapp/
│       └── index.php
├── vars/
│   ├── main.yml
│   ├── dev.yml
│   └── prod.yml
├── ansible.cfg
└── lamp_stack.yml
```

## Sample Variables for Different Environments

### Development Variables (vars/dev.yml)

```yaml
---
# Web server configuration
apache_port: 8080
document_root: '/var/www/html'
enable_debug: true

# MySQL configuration
mysql_root_password: 'devpassword'
mysql_db_name: 'devapp'
mysql_user: 'devuser'
mysql_password: 'devpass'

# PHP configuration
php_memory_limit: '256M'
php_display_errors: 'On'

# Application settings
app_environment: 'development'
```

### Production Variables (vars/prod.yml)

```yaml
---
# Web server configuration
apache_port: 80
document_root: '/var/www/html'
enable_debug: false

# MySQL configuration
mysql_root_password: 'strong_production_password'
mysql_db_name: 'prodapp'
mysql_user: 'produser'
mysql_password: 'strong_user_password'

# PHP configuration
php_memory_limit: '512M'
php_display_errors: 'Off'

# Application settings
app_environment: 'production'
```

## Error Handling Techniques

1. **Block/Rescue/Always Structure**:

   ```yaml
   tasks:
     - block:
         - name: Start Apache service
           service:
             name: apache2
             state: started
       rescue:
         - name: Log Apache failure
           debug:
             msg: 'Apache failed to start!'

         - name: Check Apache error logs
           command: tail -n 20 /var/log/apache2/error.log
           register: apache_error

         - name: Display Apache errors
           debug:
             var: apache_error.stdout_lines
       always:
         - name: Ensure Apache is configured properly
           command: apache2ctl -t
   ```

2. **Conditional Checks**:

   ```yaml
   - name: Check if MySQL is running
     command: systemctl is-active mysql
     register: mysql_status
     failed_when: false
     changed_when: false

   - name: Start MySQL if not running
     service:
       name: mysql
       state: started
     when: mysql_status.rc != 0

   - name: Report MySQL status to log
     debug:
       msg: "MySQL is {{ 'running' if mysql_status.rc == 0 else 'not running' }}"
   ```

3. **Register and Fail Module**:

   ```yaml
   - name: Check PHP configuration
     command: php -l /etc/php/7.4/apache2/php.ini
     register: php_check
     ignore_errors: yes

   - name: Fail if PHP configuration has errors
     fail:
       msg: 'PHP configuration has syntax errors!'
     when: php_check.rc != 0
   ```

## Best practices

1. Always validate your playbooks with `ansible-playbook --syntax-check playbook.yml`
2. Use `ansible-lint` to check for best practices and potential issues
3. Start with a minimal configuration and build incrementally
4. Test your playbooks against a development environment before production
5. Use `--check` (dry run) and `--diff` flags to preview changes
6. Document your variables and tasks with comments
7. Remember idempotence - your playbook should be safe to run multiple times
8. Use handlers for service restarts to only restart when needed
