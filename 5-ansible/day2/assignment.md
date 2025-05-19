# Ansible Ad-hoc Commands Lab Assignments

## Lab 1: Basic Infrastructure Discovery and Analysis

### Objective

Set up a proper inventory structure for multiple server environments and use Ansible ad-hoc commands to collect and analyze system information across all hosts.

### Lab Environment

- 10 Docker containers representing different types of servers
- All containers accessible via SSH on different ports mapped to localhost
- Base container images include Ubuntu and CentOS variants

### Requirements

1. Create an inventory structure with the following groups:
   - Webservers (4 hosts)
   - Database servers (3 hosts)
   - Cache servers (2 hosts)
   - Monitoring server (1 host)
2. Organize the inventory using both INI and YAML formats (create both versions)

3. Configure the inventory to include:

   - Host variables for each server (at least 3 per host)
   - Group variables for each server type
   - Host connection parameters (ansible_host, ansible_port, ansible_user, etc.)
   - Nested groups with proper inheritance

4. Create an ansible.cfg file with custom configurations including:

   - Custom SSH timeout settings
   - Parallelism settings (forks)
   - Fact gathering controls
   - Callback configurations for better output formatting

5. Use ad-hoc commands to gather and display:

   - System facts for each host across all groups
   - Filter and display only specific facts (installed packages, running services, CPU info)
   - Compare system information between different server types
   - Export the collected information to JSON files with proper formatting

6. Write a Bash script that uses ad-hoc commands to generate a comprehensive text report of all server information

### Deliverables

- Complete inventory files (INI and YAML format)
- Custom ansible.cfg file
- Bash script for report generation
- Sample output from all ad-hoc commands run during the exercise
- Text report sample

## Lab 2: Server Configuration Compliance and Service Management

### Objective

Create a more complex inventory structure and use ad-hoc commands to perform configuration compliance checking and service management across your infrastructure.

### Lab Environment

- 15 Docker containers with various configurations
- Mix of Ubuntu, CentOS, and Alpine Linux systems
- Systems configured with different user accounts and permissions
- Some hosts with deliberate configuration issues to be discovered

### Requirements

1. Create an advanced inventory structure that:

   - Organizes servers by OS type (Ubuntu, CentOS, Alpine)
   - Further subdivides by function (web, database, cache, etc.)
   - Implements parent/child group relationships
   - Defines variables at multiple inheritance levels
   - Uses inventory plugins for enhanced functionality

2. Configure advanced ansible.cfg settings:

   - Set up privilege escalation parameters
   - Configure custom module paths for locally developed modules
   - Implement error handling strategies
   - Set up logging configurations to track all ad-hoc commands
   - Configure fact caching for improved performance

3. Use ad-hoc commands to perform configuration compliance checks:

   - Verify user account configurations (password policies, sudo permissions)
   - Check for unauthorized services running across all hosts
   - Audit SSH configuration settings against security benchmarks
   - Scan for vulnerable packages that need updates
   - Verify file permissions on sensitive directories
   - Validate service configurations against best practices

4. Create service management tasks using ad-hoc commands:

   - Detect and restart failed services
   - Update configuration files across multiple servers
   - Synchronize specific files across server groups
   - Install and remove packages based on compliance requirements
   - Apply security patches without full system upgrades

5. Generate a compliance report using ad-hoc commands that:
   - Identifies non-compliant hosts
   - Categorizes issues by severity
   - Provides remediation commands
   - Exports results to both CSV and JSON formats

### Deliverables

- Advanced inventory structure with documentation
- Modified ansible.cfg with detailed comments
- Documentation of all ad-hoc commands used for compliance checks
- Compliance reports (CSV and JSON)
- Ad-hoc command examples for each remediation type
- Analysis of findings with recommendations

## Lab 3: Advanced Infrastructure Management with High Availability Simulation

### Objective

Design a sophisticated environment with complex dependencies and simulate high availability procedures using only ad-hoc commands while handling complex authentication mechanisms and network constraints.

### Lab Environment

- 25 Docker containers organized in application stacks
- Multi-tier application architectures (web, application, database layers)
- Custom networks with restricted communication paths
- SSH access through jump hosts only
- Simulated load balancers and proxy servers
- Systems with high availability configurations (master-slave, clustered)

### Requirements

1. Create an advanced multi-tier inventory structure:

   - Production environment (12 hosts)
   - Staging environment (8 hosts)
   - Management environment (5 hosts)
   - Define complex group relationships and inheritance patterns
   - Implement cross-environment variables that maintain consistency
   - Use inventory plugins and dynamic inventory scripts

2. Configure advanced authentication and connectivity:

   - Different SSH key authentication methods for different server groups
   - Jump host configuration for accessing internal servers
   - SSH tunneling configurations
   - Custom connection parameters for each host type
   - SSH multiplexing and pipelining optimizations

3. Create a sophisticated ansible.cfg that includes:

   - Integration with custom inventory scripts
   - Advanced parallelism strategies
   - Error handling with custom callbacks
   - SSH multiplexing optimizations
   - Integrated logging to files with rotation

4. Design high availability scenarios and solve them using only ad-hoc commands:

   - Scenario 1: Database primary node failure

     - Detect failure using ad-hoc checks
     - Promote secondary node to primary
     - Update configuration on application servers
     - Verify replication on the new secondary
     - Validate application connectivity after failover

   - Scenario 2: Web server layer scaling

     - Identify high-load web servers using ad-hoc checks
     - Deploy additional web server instances on demand
     - Update load balancer configurations
     - Distribute configuration files to new instances
     - Verify proper operation after scaling

   - Scenario 3: Configuration drift recovery
     - Use ad-hoc commands to identify configuration drift across servers
     - Generate reports of deviations from baseline
     - Create ad-hoc procedures to restore proper configurations
     - Verify configuration consistency after remediation
     - Document compliance status for all hosts

5. Ad-hoc command challenges:

   - Create complex shell pipelines using ad-hoc commands
   - Build multi-stage operations using register variables with conditional execution
   - Implement dynamic targeting based on real-time server status
   - Create idempotent ad-hoc commands for complex state changes
   - Design commands that validate their own success and report failures

6. Documentation requirements:
   - Create a runbook composed entirely of ad-hoc commands for each HA scenario
   - Document inventory architecture with diagrams
   - Create a troubleshooting guide for complex inventory issues
   - Build a performance analysis of various ad-hoc command strategies

### Deliverables

- Complete multi-tier inventory structure (YAML format)
- Advanced ansible.cfg with all required configurations
- HA runbooks for each scenario
- Documentation of all inventory structures with diagrams
- Logs demonstrating successful execution of HA scenarios
- Performance analysis and recommendations
- Security considerations document
