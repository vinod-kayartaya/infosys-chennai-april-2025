# Day 2: Networking and Scripting in Unix/Linux

## Table of Contents

1. [Basic Networking Concepts](#basic-networking-concepts)
2. [Shell Scripting Fundamentals](#shell-scripting-fundamentals)
3. [Lab Exercises](#lab-exercises)

## Basic Networking Concepts

### Introduction to Networking

_More information_ available [here](https://github.com/vinod-kayartaya/EV-AUG-2022/tree/master/Network-Fundamentals)

#### What is a Computer Network?

A computer network is a system of interconnected devices that can communicate and share resources. These devices can be computers, servers, routers, switches, or any other network-enabled equipment.

#### Key Networking Concepts

1. **IP Addresses**

   - IPv4: 32-bit addresses (e.g., 192.168.1.1)
   - IPv6: 128-bit addresses (e.g., 2001:0db8:85a3:0000:0000:8a2e:0370:7334)
   - Private IP ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16

2. **Network Types**

   - LAN (Local Area Network): Small geographical area (home, office)
   - WAN (Wide Area Network): Large geographical area (internet)
   - MAN (Metropolitan Area Network): City-wide network
   - PAN (Personal Area Network): Personal devices (Bluetooth)

3. **Network Protocols**

   - TCP/IP: The fundamental protocol suite of the internet
   - HTTP/HTTPS: Web protocols
   - FTP: File transfer
   - SSH: Secure shell
   - DNS: Domain Name System

4. **Network Layers (OSI Model)**

   - Application Layer (7): User interface
   - Presentation Layer (6): Data formatting
   - Session Layer (5): Connection management
   - Transport Layer (4): End-to-end communication
   - Network Layer (3): Routing
   - Data Link Layer (2): Physical addressing
   - Physical Layer (1): Hardware transmission

5. **Common Network Devices**

   - Router: Connects different networks
   - Switch: Connects devices within a network
   - Hub: Basic network device (obsolete)
   - Firewall: Network security device
   - Modem: Connects to internet service provider

6. **Network Security Basics**
   - Authentication: Verifying user identity
   - Authorization: Controlling access to resources
   - Encryption: Securing data transmission
   - Firewall: Filtering network traffic
   - VPN: Secure remote access

#### Network Configuration Files

```bash
# Common network configuration files
/etc/hosts           # Local hostname resolution
/etc/resolv.conf     # DNS configuration
/etc/network/interfaces  # Network interface configuration
/etc/hostname        # System hostname
```

#### Network Troubleshooting Tools

```bash
# Basic network diagnostics
ping          # Test connectivity
traceroute    # Trace network path
netstat       # Network statistics
ifconfig/ip   # Interface configuration
dig/nslookup  # DNS queries
```

#### Understanding Network Interfaces

```bash
# View all network interfaces
ifconfig
# or using the newer ip command
ip addr show

# View routing table
route -n
# or
ip route show
```

#### Configuring Network Interfaces

```bash
# Temporary configuration
sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0
# or
sudo ip addr add 192.168.1.100/24 dev eth0

# Permanent configuration (Ubuntu/Debian)
sudo nano /etc/network/interfaces
```

### Essential Network Commands

#### 1. ping - Testing Network Connectivity

The `ping` command is a fundamental network diagnostic tool that tests connectivity between your computer and another host on the network. It works by:

1. Sending ICMP (Internet Control Message Protocol) "echo request" packets to the target host
2. Waiting for ICMP "echo reply" packets from the target
3. Measuring the round-trip time between sending and receiving packets
4. Reporting packet loss and latency statistics

Ping helps administrators:

- Verify if a remote host is reachable
- Measure network latency and packet loss
- Debug network connectivity issues
- Monitor network reliability over time

```bash
# Basic ping
ping google.com

# Limit number of packets
ping -c 4 google.com

# Set interval between packets
ping -i 2 google.com
```

#### 2. netstat - Network Statistics and Connections

The `netstat` command is a powerful network diagnostic tool that provides detailed information about:

- Network connections (both incoming and outgoing)
- Routing tables
- Network interface statistics
- Protocol statistics

It works by:

1. Reading various files in the /proc filesystem
2. Gathering network statistics from the kernel
3. Displaying formatted network information to users

Netstat helps administrators:

- Monitor active network connections and their states
- View which ports are listening for connections
- Identify potential network issues or security concerns
- Analyze network traffic patterns
- Verify network service configurations

```bash
# Show all listening ports
netstat -tuln

# Show all established connections
netstat -t

# Show routing information
netstat -r
```

#### 3. traceroute - Path and Route Analysis

The `traceroute` command is a network diagnostic tool that shows the path packets take to reach a destination host. It works by:

1. Sending packets with incrementing TTL (Time To Live) values
2. Receiving ICMP "Time Exceeded" messages from intermediate routers
3. Building a map of the network path hop by hop

Traceroute helps administrators:

- Identify network bottlenecks and latency issues
- Troubleshoot routing problems
- Verify network paths and topology
- Detect network changes or outages
- Understand the number of hops to reach destinations

```bash
# Basic traceroute
traceroute google.com

# Use TCP instead of UDP
traceroute -T google.com

# Specify number of queries
traceroute -q 2 google.com
```

### Network Services

#### SSH (Secure Shell)

SSH (Secure Shell) is a cryptographic network protocol that enables secure remote access and command execution on remote systems. It provides:

- Encrypted communication channel between client and server
- Strong authentication mechanisms (passwords, keys)
- Port forwarding and tunneling capabilities
- Secure file transfers through SCP and SFTP
- Protection against network attacks like eavesdropping

SSH works by:

1. Establishing encrypted connection between client and server
2. Authenticating user credentials or keys
3. Creating secure channel for data transmission
4. Enabling remote command execution and file transfers

Common use cases:

- Remote server administration
- Secure file transfers
- Port forwarding and tunneling
- Remote application access
- Automated scripts and deployments

```bash
# Basic SSH connection
ssh user@remote_host

# Specify port
ssh -p 2222 user@remote_host

# Generate SSH key pair
ssh-keygen -t rsa -b 4096

# Copy public key to remote server
ssh-copy-id user@remote_host
```

#### SCP (Secure Copy)

SCP (Secure Copy) is a command-line utility that allows secure file transfers between hosts over SSH. It provides:

- Encrypted file transfers using SSH protocol
- Simple command syntax for copying files/directories
- Local-to-remote, remote-to-local, and remote-to-remote transfers
- Preservation of file permissions and timestamps
- Progress reporting during transfers

Key features:

1. Built on SSH protocol for security
2. Supports recursive directory copying
3. Bandwidth limiting capabilities
4. Automatic compression during transfer
5. Identity file and port specification options

Common use cases:

- Copying configuration files to servers
- Backing up remote files locally
- Deploying application files
- Transferring data between systems
- Automated file synchronization scripts

```bash
# Copy file to remote server
scp file.txt user@remote_host:/path/to/destination

# Copy directory recursively
scp -r directory/ user@remote_host:/path/to/destination

# Copy from remote server
scp user@remote_host:/path/to/file.txt ./
```

#### SFTP (Secure File Transfer Protocol)

SFTP (Secure File Transfer Protocol) is a secure file transfer protocol that runs over SSH. It provides a more robust and feature-rich alternative to SCP with the following capabilities:

Key features:

1. Interactive file transfer interface
2. Full file system operations (create/delete directories, change permissions)
3. Resume interrupted transfers
4. Directory listings and navigation
5. File locking and atomic operations
6. Better error handling and recovery

Advantages over SCP:

- Full remote filesystem access and manipulation
- Interactive shell for multiple operations
- Built-in file management commands
- More reliable for large transfers
- Better error reporting and recovery options

Common use cases:

- Interactive remote file management
- Automated file synchronization
- Secure file uploads/downloads
- Remote backup operations
- Web server file management

```bash
# Connect to SFTP server
sftp user@remote_host

# Common SFTP commands
put file.txt          # Upload file
get file.txt          # Download file
ls                    # List remote files
lls                   # List local files
```

#### curl and wget

curl and wget are two popular command-line tools for downloading files and interacting with web resources:

**curl (Client URL)**

- Versatile tool for transferring data using various protocols (HTTP, HTTPS, FTP, etc.)
- Supports uploading and downloading files
- Can send various types of HTTP requests (GET, POST, PUT, etc.)
- Excellent for API testing and web scraping
- Supports authentication, cookies, and custom headers
- Can display detailed transfer information and progress

**wget (Web Get)**

- Primarily focused on file downloading
- Supports recursive downloads of websites
- Better at handling large file downloads and poor connections
- Can download files in the background
- Automatically retries failed downloads
- Supports FTP and HTTP(S) protocols
- Excellent for mirroring websites or batch downloads

Key differences:

- curl is more versatile for general web interactions and API testing
- wget is specialized for downloading files and website mirroring
- curl requires more flags for some operations but offers more protocol support
- wget has better built-in support for recursive downloads

```bash
# Download file with curl
curl -O https://example.com/file.txt

# Download file with wget
wget https://example.com/file.txt

# Download with progress bar
curl -# -O https://example.com/file.txt
```

### Firewall Basics

#### iptables

iptables is a command-line firewall utility that allows a system administrator to configure the IP packet filter rules of the Linux kernel firewall. Key concepts include:

- **Tables**: Different categories of firewall rules (filter, nat, mangle, etc.)

  - filter: Default table for packet filtering
  - nat: For network address translation
  - mangle: For specialized packet alteration

- **Chains**: Groups of rules in a specific order

  - INPUT: For packets coming into the system
  - OUTPUT: For packets leaving the system
  - FORWARD: For packets being routed through the system

- **Rules**: Individual packet filtering instructions that specify:

  - Matching criteria (source IP, destination port, protocol, etc.)
  - Target action (ACCEPT, DROP, REJECT, etc.)

- **Policies**: Default actions for chains when no rules match

Common use cases:

- Blocking malicious IP addresses
- Allowing/blocking specific services (ports)
- Network address translation (NAT)
- Port forwarding
- Logging suspicious traffic

```bash
# List all rules
sudo iptables -L

# Allow incoming SSH
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Block specific IP
sudo iptables -A INPUT -s 192.168.1.100 -j DROP

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

## Shell Scripting Fundamentals

Shell scripting is a powerful way to automate tasks in Unix/Linux systems by writing sequences of commands in a file that can be executed. A shell script is essentially a computer program written in a shell language (like Bash, sh, zsh, etc.) that the shell can read and execute.

Key aspects of shell scripting:

- **Automation**: Automate repetitive tasks and system administration
- **System Administration**: Manage users, processes, and system resources
- **Task Scheduling**: Run scripts at specific times using cron jobs
- **File Operations**: Bulk file processing, backups, and organization
- **System Monitoring**: Track system resources and generate reports
- **Network Operations**: Automate network configurations and testing
- **Data Processing**: Parse logs, process text files, and handle data

Common use cases:

- System backups and maintenance
- Log file analysis and reporting
- User account management
- Software installation and updates
- System health monitoring
- Automated testing and deployment
- Batch file processing
- System initialization and startup tasks

Shell scripts are especially valuable for:

- DevOps automation
- System administration
- Build and deployment processes
- Data processing pipelines
- Security auditing and monitoring

### Basic Script Structure

```bash
#! /usr/bin/bash
# This is a comment
echo "Hello, World!"
```

### Variables

Variables in shell scripting are used to store and manipulate data. They are fundamental building blocks that allow scripts to work with dynamic values and maintain state.

Key points about variables:

1. **Declaration and Assignment**:

   - No declaration keyword needed (unlike other languages)
   - Assigned using `=` with NO spaces around it
   - Example: `name="Vinod"` (correct), `name = "Vinod"` (incorrect)

2. **Naming Rules**:

   - Must start with a letter or underscore
   - Can contain letters, numbers, underscores
   - Case-sensitive
   - Cannot use reserved keywords

3. **Types of Variables**:

   - Environment variables (like PATH, HOME)
   - User-defined variables
   - Special variables ($0, $1, $#, etc.)
   - Read-only variables (declared with readonly)

4. **Usage**:

   - Access value using `$` prefix: `$variable` or `${variable}`
   - Curly braces {} recommended for clarity
   - Double quotes preserve spacing but allow variable expansion
   - Single quotes preserve literal text

5. **Scope**:
   - By default, variables are local to current shell
   - Use `export` to make them available to child processes
   - Functions can have local variables using `local` keyword

Common practices and limitations:

- Initialize variables before use
- Use meaningful names
- Cannot use spaces or special characters in names
- Cannot start with numbers
- Cannot use mathematical operators in names

```bash
# Variable declaration
name="Vinod"
age=52

# Using variables
echo "Name: $name"
echo "Age: $age"

# Command substitution
current_date=$(date)
echo "Current date: $current_date"
```

### Control Structures

Control structures in shell scripting allow you to control the flow of execution in your scripts. The main control structures are:

1. **Conditional Statements**:

   - if-then-else statements for decision making
   - case statements for multiple condition matching
   - test commands [ ] for evaluating conditions

2. **Loops**:

   - for loops for iterating over lists/sequences
   - while loops for condition-based iteration
   - until loops for inverse condition-based iteration
   - break and continue for loop control

3. **Selection**:
   - case statements for pattern matching
   - select for creating simple menus

These structures help create logic and make scripts more dynamic by allowing different execution paths based on conditions and repetitive tasks through loops.

#### If-Else Statements

The if-else statement is a fundamental control structure in shell scripting that allows conditional execution of code. Here's how it works:

1. **Basic Syntax**:

   ```bash
   if [ condition ]; then
       # code to execute if condition is true
   fi
   ```

2. **With Else Clause**:

   ```bash
   if [ condition ]; then
       # code for true condition
   else
       # code for false condition
   fi
   ```

3. **With Elif (Else If)**:

   ```bash
   if [ condition1 ]; then
       # code for condition1
   elif [ condition2 ]; then
       # code for condition2
   else
       # code if no conditions match
   fi
   ```

4. **Common Operators**:

   - `-eq`: Equal to
   - `-ne`: Not equal to
   - `-gt`: Greater than
   - `-lt`: Less than
   - `-ge`: Greater than or equal to
   - `-le`: Less than or equal to
   - `=`: String equality
   - `!=`: String inequality
   - `-z`: String is empty
   - `-n`: String is not empty

5. **File Test Operators**:
   - `-f file`: True if file exists and is regular file
   - `-d file`: True if file exists and is directory
   - `-r file`: True if file is readable
   - `-w file`: True if file is writable
   - `-x file`: True if file is executable

Note: Always ensure proper spacing within brackets [ ] as they are actually commands themselves.

```bash
#!/bin/bash
if [ $1 -gt 10 ]; then
    echo "Number is greater than 10"
elif [ $1 -eq 10 ]; then
    echo "Number is equal to 10"
else
    echo "Number is less than 10"
fi
```

#### Loops

```bash
# For loop
for i in {1..5}; do
    echo "Iteration $i"
done

# While loop
count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    ((count++))
done
```

### Functions

Functions in shell scripts are blocks of reusable code that can be called multiple times. They help organize code and reduce redundancy.

1. **Function Declaration**:

   ```bash
   function_name() {
       # Function body
   }
   ```

   Or simply:

   ```bash
   function function_name {
       # Function body
   }
   ```

2. **Function Parameters**:

   - Access parameters using $1, $2, etc.
   - $@ represents all parameters
   - $# gives number of parameters

   ```bash
   function greet() {
       echo "Hello $1, you are $2 years old"
   }
   greet "John" "25"
   ```

3. **Local Variables**:

   - Use 'local' keyword for function-scoped variables
   - Prevents variable name conflicts

   ```bash
   function calculate() {
       local result=$((1 + 2))
       echo $result
   }
   ```

4. **Return Values**:

   - Use 'return' for exit status (0-255)
   - Use echo/printf for actual values

   ```bash
   function add() {
       echo $(($1 + $2))
       return 0
   }
   result=$(add 5 3)
   ```

5. **Function Examples**:

```bash
#!/bin/bash
function greet() {
    local name=$1
    echo "Hello, $name!"
}

# Call function
greet "Vinod"
```

### Input/Output Handling

Input/output handling in shell scripts involves managing data flow between the script, user input, files, and other programs. Here are the key concepts:

1. **Reading User Input**:

   - `read` command gets input from user
   - `-p` flag allows showing a prompt
   - Can read multiple variables at once

   ```bash
   read -p "Enter name: " name
   read -p "Enter age and city: " age city
   ```

2. **Command Line Arguments**:

   - Scripts can accept arguments when called
   - Access using $1, $2, etc.
   - $0 contains script name

   ```bash
   ./script.sh arg1 arg2
   # Inside script: $1 is arg1, $2 is arg2
   ```

3. **File Operations**:

   - Redirect output using > (overwrite) or >> (append)
   - Read file contents line by line
   - Process file data using pipes |

   ```bash
   # Write to file
   echo "data" > file.txt

   # Read file
   cat file.txt | while read line; do
       echo "Processing: $line"
   done
   ```

4. **Standard Streams**:

   - stdin (0): Input stream
   - stdout (1): Output stream
   - stderr (2): Error stream

   ```bash
   # Redirect error messages
   command 2> error.log

   # Redirect both output and errors
   command &> all.log
   ```

5. **Here Documents**:
   - Multi-line input using <<
   - Useful for generating files or sending multi-line input
   ```bash
   cat << EOF > config.txt
   setting1=value1
   setting2=value2
   EOF
   ```

```bash
#!/bin/bash
# Read user input
read -p "Enter your name: " name
echo "Hello, $name!"

# Redirect output
echo "This goes to file" > output.txt
echo "This appends to file" >> output.txt

# Read from file
while read line; do
    echo "Line: $line"
done < input.txt
```

### Error Handling

```bash
#!/bin/bash
# Exit on error
set -e

# Check if command exists
if ! command -v program &> /dev/null; then
    echo "Program not found"
    exit 1
fi

# Trap errors
trap 'echo "Error occurred on line $LINENO"' ERR
```

## Additional Resources

- [Linux Network Administrator's Guide](https://tldp.org/LDP/nag2/index.html)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
