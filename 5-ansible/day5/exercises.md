
## Practical Exercises


Let's put your knowledge to practice with a series of exercises:

### Exercise 1: Basic Role Creation

**Task**: Create a role called `system_baseline` that:
- Updates all packages
- Sets the system timezone to UTC
- Configures a basic firewall with SSH access
- Creates a non-root user with sudo privileges

### Exercise 2: Role Variables

**Task**: Enhance your `system_baseline` role by adding variables for:
- Timezone (default: UTC)
- SSH port (default: 22)
- Additional firewall ports to open
- Username and password for the non-root user

### Exercise 3: Role Dependencies

**Task**: Create a new role called `web_application` that:
- Depends on your `system_baseline` role
- Installs and configures Nginx
- Deploys a simple web application from a template
- Sets up a logrotate configuration

### Exercise 4: Complex Role Structure

**Task**: Create a multi-tier application deployment with these roles:
- `loadbalancer`: Installs and configures HAProxy
- `webserver`: Installs and configures Nginx/Apache
- `app_server`: Installs and configures your application
- `database`: Installs and configures MySQL/PostgreSQL

Create a playbook that uses all these roles with proper conditionals and variables.

### Exercise 5: Ansible Galaxy

**Task**: Find and use appropriate roles from Ansible Galaxy to:
- Install and configure Docker
- Set up a monitoring solution with Prometheus and Grafana
- Create a playbook that uses these roles together
