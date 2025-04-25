# Day 2 Lab Assignment: Networking and Scripting

## Overview

This lab assignment presents real-world networking and scripting challenges that you need to solve. Each problem requires you to apply your knowledge of networking concepts and shell scripting to create practical solutions.

## Prerequisites

- Basic understanding of Unix/Linux commands
- Access to a Linux system (Ubuntu/Debian recommended)
- Root or sudo privileges for network configuration
- Text editor (nano, vim, or any preferred editor)

## Problem 1: Network Infrastructure Analysis and Security

**Problem Statement:**
You are a network administrator tasked with analyzing and securing the network infrastructure of a small office. The office has multiple computers connected to a local network, and you need to ensure proper network configuration and security.

**Tasks:**

1. Analyze the current network configuration and document all network interfaces, their IP addresses, and connection status.
2. Test network connectivity to critical services and identify any potential bottlenecks or issues.
3. Identify all running network services and assess their security implications.
4. Implement basic firewall rules to secure the network while maintaining necessary services.

**Hints:**

```bash
# Task 1: Network Configuration Analysis
ifconfig                    # View all network interfaces
ip addr show               # Alternative to ifconfig
ip route show              # View routing table
nmcli device show          # Detailed network device information

# Task 2: Network Connectivity Testing
ping -c 4 google.com       # Test connectivity with 4 packets
traceroute google.com      # Map network path
mtr google.com             # Interactive traceroute
netstat -i                 # Network interface statistics

# Task 3: Service Analysis
netstat -tuln              # List all listening ports
ss -tuln                   # Alternative to netstat
lsof -i                    # List open network connections
systemctl list-units --type=service  # List all services

# Task 4: Firewall Configuration
sudo iptables -L           # List current rules
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT  # Allow SSH
sudo iptables -A INPUT -s 192.168.1.100 -j DROP     # Block IP
sudo iptables-save > /etc/iptables/rules.v4         # Save rules
```

**Deliverables:**

- A detailed network analysis report
- Documentation of all network services and their purposes
- A list of implemented security measures
- Screenshots of network configurations and test results

## Problem 2: Network Monitoring and Automation

**Problem Statement:**
Your organization needs an automated system to monitor network health and performance. You are tasked with creating scripts that will help maintain and monitor the network infrastructure.

**Tasks:**

1. Develop a script that continuously monitors network connectivity to critical servers and services.
2. Create a backup system for network configurations that can be easily restored if needed.
3. Implement a service management system that can monitor and control network services.

**Hints:**

```bash
# Task 1: Network Monitoring Script
#!/bin/bash
# Useful commands for monitoring:
ping -c 1 $HOST           # Check single host
nc -zv $HOST $PORT        # Check port availability
curl -I $URL              # Check web service
date +"%Y-%m-%d %H:%M:%S" # Timestamp for logging

# Task 2: Backup System
#!/bin/bash
# Useful commands for backup:
cp -r /etc/network /backup/network_$(date +%Y%m%d)  # Backup with date
tar -czf backup.tar.gz /etc/network                 # Compressed backup
rsync -av /etc/network/ /backup/network/            # Incremental backup

# Task 3: Service Management
#!/bin/bash
# Useful commands for service management:
systemctl status $SERVICE  # Check service status
systemctl start $SERVICE   # Start service
systemctl stop $SERVICE    # Stop service
systemctl restart $SERVICE # Restart service
```

**Requirements:**

- The monitoring script should:
  - Check multiple hosts simultaneously
  - Log results with timestamps
  - Alert administrators of any issues
  - Be configurable for different monitoring intervals
- The backup system should:
  - Create timestamped backups
  - Include all network configuration files
  - Provide easy restoration
  - Handle errors gracefully
- The service management system should:
  - List all network services
  - Allow service control (start/stop/restart)
  - Monitor service status
  - Log all actions

**Deliverables:**

- Working scripts with proper error handling
- Documentation of script functionality
- Test results and logs
- Usage instructions

## Problem 3: Secure Network Infrastructure

**Problem Statement:**
Your organization needs to implement secure file transfer and remote access capabilities. You are responsible for setting up and securing these services.

**Tasks:**

1. Implement SSH key-based authentication for secure remote access.
2. Set up and secure an SFTP server for file transfers.
3. Create a security monitoring system to detect and respond to potential threats.

**Hints:**

```bash
# Task 1: SSH Key Management
ssh-keygen -t rsa -b 4096                    # Generate key pair
ssh-copy-id user@remote_host                 # Copy public key
chmod 700 ~/.ssh                             # Secure SSH directory
chmod 600 ~/.ssh/id_rsa                      # Secure private key

# Task 2: SFTP Setup
sudo apt-get install openssh-sftp-server     # Install SFTP server
sudo nano /etc/ssh/sshd_config              # Configure SFTP
sudo systemctl restart sshd                  # Restart SSH service
sftp user@host                              # Test SFTP connection

# Task 3: Security Monitoring
grep "Failed password" /var/log/auth.log     # Check failed logins
netstat -an | grep LISTEN                    # Check listening ports
tail -f /var/log/auth.log                    # Monitor auth log
fail2ban-client status                       # Check fail2ban status
```

**Requirements:**

- SSH implementation should:
  - Use strong key pairs
  - Implement proper access controls
  - Include backup authentication methods
  - Document the setup process
- SFTP server should:
  - Support multiple users
  - Implement access restrictions
  - Include logging capabilities
  - Handle file transfer securely
- Security monitoring should:
  - Track login attempts
  - Monitor network activity
  - Generate security reports
  - Implement basic intrusion detection

**Deliverables:**

- Working secure file transfer system
- Documentation of security measures
- Security monitoring reports
- Implementation guide

## Submission Requirements

1. **Documentation**

   - Detailed problem analysis
   - Solution approach and methodology
   - Implementation details
   - Testing results and validation

2. **Code Submission**

   - Well-documented scripts
   - Error handling implementation
   - Configuration files
   - Usage instructions

3. **Testing**
   - Test cases and results
   - Edge case handling
   - Security validation
   - Performance metrics

## Additional Resources

- [Linux Network Administrator's Guide](https://tldp.org/LDP/nag2/index.html)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [SSH and SFTP Documentation](https://www.openssh.com/manual.html)
