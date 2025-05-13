# Linux Commands Reference

This document provides a comprehensive list of Linux commands covered in the Unix Training Course, along with explanations and examples for each command.

## Navigation & File System

### pwd

**Purpose**: Print Working Directory - displays the current directory path.
**Examples**:

```bash
pwd
# Output: /home/username
```

### cd

**Purpose**: Change Directory - navigate to a different directory.
**Examples**:

```bash
cd /home/username/Documents    # Change to absolute path
cd Documents                   # Change to subdirectory
cd ..                          # Move up one directory
cd ~                           # Change to home directory
cd -                           # Return to previous directory
```

### ls

**Purpose**: List files and directories.
**Examples**:

```bash
ls                             # List files in current directory
ls -l                          # List in long format (permissions, size, date)
ls -a                          # List all files (including hidden)
ls -lh                         # Long format with human-readable file sizes
ls /etc                        # List files in /etc directory
```

### mkdir

**Purpose**: Make Directory - create new directories.
**Examples**:

```bash
mkdir new_folder               # Create a directory
mkdir -p parent/child/subchild # Create nested directories
```

### touch

**Purpose**: Create empty files or update file timestamps.
**Examples**:

```bash
touch file.txt                 # Create empty file or update timestamp
touch file1.txt file2.txt      # Create multiple files
```

### rm

**Purpose**: Remove files or directories.
**Examples**:

```bash
rm file.txt                    # Remove a file
rm -i file.txt                 # Remove with confirmation prompt
rm -r directory                # Remove directory and its contents
rm -rf directory               # Force remove without prompting (use with caution)
```

### cp

**Purpose**: Copy files and directories.
**Examples**:

```bash
cp file.txt backup.txt         # Copy file to new name
cp file.txt /path/to/directory # Copy to different directory
cp -r source_dir dest_dir      # Copy directory and its contents
```

### mv

**Purpose**: Move or rename files and directories.
**Examples**:

```bash
mv file.txt newname.txt        # Rename a file
mv file.txt /path/to/directory # Move file to directory
mv dir1 dir2                   # Move/rename directories
```

## File Searching

### find

**Purpose**: Search for files in a directory hierarchy based on various criteria.
**Examples**:

```bash
find /home -name "*.txt"       # Find all .txt files in /home
find . -type d                 # Find all directories in current location
find . -mtime -7               # Find files modified in the last 7 days
find . -size +10M              # Find files larger than 10MB
```

### locate

**Purpose**: Find files by name, using a pre-built database.
**Examples**:

```bash
locate filename.txt            # Find file by name
locate -i filename             # Case-insensitive search
sudo updatedb                  # Update the locate database
```

## Text Processing

### grep

**Purpose**: Search text patterns in files.
**Examples**:

```bash
grep "pattern" file.txt        # Search for pattern in file
grep -i "pattern" file.txt     # Case-insensitive search
grep -r "pattern" directory    # Recursive search in directory
grep -v "pattern" file.txt     # Show lines NOT matching pattern
grep -n "pattern" file.txt     # Show line numbers with matches
```

### sed

**Purpose**: Stream editor for filtering and transforming text.
**Examples**:

```bash
sed 's/old/new/' file.txt      # Replace first occurrence of 'old' with 'new'
sed 's/old/new/g' file.txt     # Replace all occurrences
sed -i 's/old/new/g' file.txt  # Edit file in-place
sed '5d' file.txt              # Delete line 5
sed '1,5d' file.txt            # Delete lines 1-5
```

### awk

**Purpose**: Pattern scanning and text processing language.
**Examples**:

```bash
awk '{print $1}' file.txt      # Print first column of each line
awk -F: '{print $1}' /etc/passwd # Use : as field separator
awk '{sum+=$1} END {print sum}' file.txt # Sum first column
awk '$3 > 100' file.txt        # Print lines where 3rd field > 100
```

### sort

**Purpose**: Sort lines of text files.
**Examples**:

```bash
sort file.txt                  # Sort lines alphabetically
sort -r file.txt               # Sort in reverse order
sort -n file.txt               # Sort numerically
sort -k2 file.txt              # Sort by second column
```

### uniq

**Purpose**: Report or omit repeated lines.
**Examples**:

```bash
uniq file.txt                  # Remove duplicate adjacent lines
sort file.txt | uniq           # Remove all duplicates (sort first)
uniq -c file.txt               # Count occurrences of lines
uniq -d file.txt               # Show only duplicate lines
```

## System Administration

### chmod

**Purpose**: Change file mode/permissions.
**Examples**:

```bash
chmod 755 file.txt             # rwx for owner, rx for group and others
chmod +x script.sh             # Add execute permission
chmod -w file.txt              # Remove write permission
chmod u+rwx,g+rx,o+r file.txt  # Symbolic notation
```

### chown

**Purpose**: Change file owner and group.
**Examples**:

```bash
chown user file.txt            # Change owner
chown user:group file.txt      # Change owner and group
chown -R user directory        # Change recursively for directory
```

### chgrp

**Purpose**: Change group ownership.
**Examples**:

```bash
chgrp group file.txt           # Change group ownership
chgrp -R group directory       # Change recursively
```

### ps

**Purpose**: Report process status.
**Examples**:

```bash
ps                             # Show processes for current terminal
ps aux                         # Show all processes in BSD format
ps -ef                         # Show all processes in full format
ps --forest                    # Show process tree
```

### top

**Purpose**: Display and update sorted processes.
**Examples**:

```bash
top                            # Interactive process viewer
top -u username                # Show only user's processes
```

### kill

**Purpose**: Send a signal to a process.
**Examples**:

```bash
kill PID                       # Send TERM signal to process
kill -9 PID                    # Force kill (SIGKILL)
killall process_name           # Kill processes by name
```

## Networking

### ifconfig / ip

**Purpose**: Configure network interfaces.
**Examples**:

```bash
ifconfig                       # Show all interfaces (deprecated)
ip addr show                   # Show all interfaces (modern)
ip addr add 192.168.1.10/24 dev eth0 # Add IP address
ip link set eth0 up            # Bring interface up
```

### ping

**Purpose**: Send ICMP ECHO_REQUEST to network hosts.
**Examples**:

```bash
ping google.com                # Ping continuously
ping -c 4 google.com           # Ping 4 times only
```

### netstat

**Purpose**: Show network connections, routing tables, interface statistics.
**Examples**:

```bash
netstat -tuln                  # Show listening TCP/UDP ports
netstat -r                     # Show routing table
ss -tuln                       # Modern alternative to netstat
```

### traceroute

**Purpose**: Print the route packets take to network host.
**Examples**:

```bash
traceroute google.com          # Trace route to google.com
traceroute -n google.com       # Don't resolve IP addresses
```

### ssh

**Purpose**: Secure Shell - remote login.
**Examples**:

```bash
ssh user@hostname              # Connect to remote host
ssh -p 2222 user@hostname      # Connect to specific port
ssh -i key.pem user@hostname   # Use identity file
```

### scp

**Purpose**: Secure Copy - copy files between hosts.
**Examples**:

```bash
scp file.txt user@host:/path   # Copy local file to remote host
scp user@host:/path/file.txt . # Copy remote file to local machine
scp -r directory user@host:/path # Copy directory recursively
```

### sftp

**Purpose**: Secure File Transfer Protocol.
**Examples**:

```bash
sftp user@host                 # Start SFTP session
get file.txt                   # Download file (within SFTP)
put file.txt                   # Upload file (within SFTP)
```

### curl

**Purpose**: Transfer data from or to a server.
**Examples**:

```bash
curl https://example.com       # Get website content
curl -o file.txt https://example.com # Save output to file
curl -X POST -d "data" https://example.com # Send POST request
```

### wget

**Purpose**: Non-interactive network downloader.
**Examples**:

```bash
wget https://example.com/file  # Download file
wget -c https://example.com/file # Continue interrupted download
wget -r -np https://example.com # Download website recursively
```

## Security Tools

### gpg

**Purpose**: GNU Privacy Guard - encryption and signing tool.
**Examples**:

```bash
gpg -c file.txt                # Encrypt file with passphrase
gpg file.txt.gpg               # Decrypt file
gpg --gen-key                  # Generate a new key pair
gpg -e -r recipient file.txt   # Encrypt for recipient
```

### openssl

**Purpose**: Cryptography toolkit.
**Examples**:

```bash
openssl genrsa -out key.pem 2048 # Generate RSA private key
openssl enc -aes-256-cbc -in file.txt -out file.enc # Encrypt file
openssl enc -d -aes-256-cbc -in file.enc -out file.txt # Decrypt
```

## System Automation

### cron

**Purpose**: Schedule periodic background work.
**Examples**:

```bash
crontab -e                     # Edit crontab file
# minute hour day month weekday command
# 0 5 * * * /path/to/script    # Run at 5:00 AM daily
```

### at

**Purpose**: Schedule commands to run once at a specific time.
**Examples**:

```bash
at 10:00 AM                    # Schedule job at 10 AM (enter commands, Ctrl+D to finish)
at now + 1 hour                # Schedule job 1 hour from now
atq                            # List scheduled jobs
atrm job_number                # Remove scheduled job
```

## Package Management (Ubuntu/Debian)

### apt / apt-get

**Purpose**: Package management.
**Examples**:

```bash
apt update                     # Update package lists
apt upgrade                    # Upgrade installed packages
apt install package_name       # Install package
apt remove package_name        # Remove package
apt search keyword             # Search for packages
```

## System Information

### uname

**Purpose**: Print system information.
**Examples**:

```bash
uname -a                       # All system information
uname -r                       # Kernel release
```

### df

**Purpose**: Report file system disk space usage.
**Examples**:

```bash
df -h                          # Human-readable sizes
df -i                          # Show inode information
```

### du

**Purpose**: Estimate file space usage.
**Examples**:

```bash
du -h file                     # Human-readable size of file
du -sh directory               # Size of directory (summarized)
```

### free

**Purpose**: Display amount of free and used memory.
**Examples**:

```bash
free -h                        # Show memory usage in human-readable format
free -m                        # Show in megabytes
```

## Systemd

### systemctl

**Purpose**: Control the systemd system and service manager.
**Examples**:

```bash
systemctl status service_name  # Check service status
systemctl start service_name   # Start a service
systemctl stop service_name    # Stop a service
systemctl enable service_name  # Enable service to start at boot
systemctl disable service_name # Disable service from starting at boot
```
