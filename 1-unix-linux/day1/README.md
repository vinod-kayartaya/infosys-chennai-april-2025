# Day 1: Environment, Tools, and System Management

## Table of Contents

1. [Introduction to Unix Operating System](#introduction-to-unix-operating-system)
2. [Getting Started](#getting-started)
3. [Essential Commands and File System](#essential-commands-and-file-system)
4. [System Administration Basics](#system-administration-basics)
5. [Lab Exercise](#lab-exercise)

## Introduction to Unix Operating System

### What is Unix?

Unix is a powerful, multi-user, multi-tasking operating system that was developed in the 1970s at Bell Labs. It was designed to be portable, flexible, and efficient, making it one of the most influential operating systems in computing history. Unix has become the foundation for many modern operating systems, including Linux, macOS, and various BSD variants.

### Unix Evolution Timeline

- 1969 - Unix development begins at Bell Labs
- 1971 - First edition of Unix released
- 1973 - Unix rewritten in C programming language
- 1975 - Sixth Edition Unix (V6) widely distributed to universities
- 1977 - BSD Unix development begins at UC Berkeley
- 1983 - System V Unix released by AT&T
- 1991 - Linux kernel development begins
- 1993 - FreeBSD released
- 2000s - Unix principles influence modern OS development including macOS
- 2010s+ - Unix/Linux dominates server market and powers Android

### Key Characteristics of Unix

1. **Multi-user System**

   - Multiple users can access the system simultaneously
   - Each user has their own account and permissions
   - System resources are shared efficiently among users

2. **Multi-tasking**

   - Can run multiple processes simultaneously
   - Processes can run in the background
   - Efficient process scheduling and management

3. **Portability**

   - Written in C programming language
   - Can run on various hardware platforms
   - Easy to adapt to different environments

4. **Hierarchical File System**

   - Organized directory structure
   - Everything is treated as a file
   - Consistent file naming and access methods

5. **Shell Interface**
   - Command-line interface for system interaction
   - Powerful scripting capabilities
   - Piping and redirection for command chaining

### Unix Architecture

The Unix operating system is built on several key components:

1. **Kernel**

   - Core of the operating system
   - Manages hardware resources
   - Handles process scheduling
   - Manages memory and file systems

2. **Shell**

   - User interface to the system
   - Interprets user commands
   - Provides programming environment
   - Manages command execution

3. **File System**

   - Hierarchical directory structure
   - File permissions and security
   - Device and process representation
   - Standard file operations

4. **Utilities and Applications**
   - Built-in command-line tools
   - System administration tools
   - User applications
   - Development tools

### Unix Philosophy

The Unix philosophy is a set of cultural norms and philosophical approaches to software development. It emphasizes:

1. **Modularity**

   - Programs should do one thing well
   - Complex tasks should be broken into simpler ones
   - Programs should be small and focused

2. **Composition**

   - Programs should work together
   - Use text streams for communication
   - Chain programs together with pipes

3. **Simplicity**

   - Keep things simple
   - Avoid unnecessary complexity
   - Focus on clarity and efficiency

4. **Transparency**
   - Make programs easy to understand
   - Use plain text for data storage
   - Provide clear documentation

### Unix vs. Other Operating Systems

1. **Unix vs. Windows**

   - Unix: Command-line focused, modular design
   - Windows: GUI-focused, monolithic design
   - Different file system structures
   - Different security models

2. **Unix vs. Linux**

   - Unix: Proprietary, commercial
   - Linux: Open-source, free
   - Similar architecture and philosophy
   - Different licensing and distribution models

3. **Unix vs. macOS**
   - macOS: Built on Unix foundation
   - Similar command-line interface
   - Different GUI and user experience
   - Different application ecosystem

## Getting Started

### Terminal Basics

The terminal (or shell) is a text-based interface to interact with the operating system. Common shells include:

- **Bash** (Bourne Again Shell): Most common default shell
- **Zsh**: Enhanced version of Bash with additional features
- **Fish**: User-friendly shell with advanced features

### Command Structure

Basic command structure:

```bash
command [options] [arguments]
```

Example:

```bash
ls -l /home/user
```

- `ls`: command
- `-l`: option (long format)
- `/home/user`: argument (directory path)

### Basic Navigation

Essential navigation commands:

- `pwd`: Print Working Directory
- `cd`: Change Directory
- `ls`: List Directory Contents
- `clear`: Clear terminal screen
- `history`: Show command history

## Essential Commands and File System

### Basic Commands

#### 1. File System Navigation Commands

##### `pwd` (Print Working Directory)

- **Purpose**: Shows the current working directory
- **Syntax**: `pwd [options]`
- **Options**:
  - `-L`: Display logical path (default)
  - `-P`: Display physical path (resolves symbolic links)
- **Examples**:

  ```bash
  $ pwd
  /home/user/documents

  $ pwd -P
  /home/user/documents
  ```

##### `cd` (Change Directory)

- **Purpose**: Changes the current working directory
- **Syntax**: `cd [directory]`
- **Special Paths**:
  - `cd ~` or `cd`: Go to home directory
  - `cd ..`: Go to parent directory
  - `cd -`: Go to previous directory
- **Examples**:
  ```bash
  $ cd /home/user/documents
  $ cd ..
  $ cd ~/downloads
  $ cd -
  ```

##### `ls` (List Directory Contents)

- **Purpose**: Lists files and directories
- **Syntax**: `ls [options] [file/directory]`
- **Common Options**:
  - `-l`: Long format (detailed listing)
  - `-a`: Show hidden files
  - `-h`: Human-readable file sizes
  - `-R`: Recursive listing
- **Examples**:

  ```bash
  $ ls
  file1.txt  file2.txt  directory1

  $ ls -l
  total 32
  drwxr-xr-x 2 user group 4096 Mar 15 10:00 directory1
  -rw-r--r-- 1 user group  123 Mar 15 09:30 file1.txt
  -rw-r--r-- 1 user group  456 Mar 15 09:35 file2.txt

  $ ls -la
  .  ..  .hidden  file1.txt  file2.txt  directory1
  ```

#### 2. File Manipulation Commands

##### `mkdir` (Make Directory)

- **Purpose**: Creates new directories
- **Syntax**: `mkdir [options] directory_name`
- **Options**:
  - `-p`: Create parent directories if needed
  - `-m`: Set permissions
- **Examples**:
  ```bash
  $ mkdir new_directory
  $ mkdir -p parent/child/grandchild
  $ mkdir -m 755 public_directory
  ```

##### `touch` (Create/Update File)

- **Purpose**: Creates empty files or updates timestamps
- **Syntax**: `touch [options] filename`
- **Options**:
  - `-a`: Change access time only
  - `-m`: Change modification time only
  - `-t`: Set specific timestamp
- **Examples**:
  ```bash
  $ touch new_file.txt
  $ touch -t 202403151200 file.txt
  $ touch -a file.txt
  ```

##### `rm` (Remove)

- **Purpose**: Removes files and directories
- **Syntax**: `rm [options] file/directory`
- **Options**:
  - `-r`: Recursive removal
  - `-f`: Force removal without confirmation
  - `-i`: Interactive mode
- **Examples**:
  ```bash
  $ rm file.txt
  $ rm -r directory
  $ rm -i file.txt
  $ rm -rf directory
  ```

##### `cp` (Copy)

- **Purpose**: Copies files and directories
- **Syntax**: `cp [options] source destination`
- **Options**:
  - `-r`: Recursive copy
  - `-p`: Preserve permissions
  - `-i`: Interactive mode
  - `-v`: Verbose output
- **Examples**:
  ```bash
  $ cp file.txt /backup/
  $ cp -r directory /backup/
  $ cp -p file.txt /backup/
  $ cp -v file.txt /backup/
  ```

##### `mv` (Move)

- **Purpose**: Moves or renames files and directories
- **Syntax**: `mv [options] source destination`
- **Options**:
  - `-i`: Interactive mode
  - `-f`: Force move
  - `-v`: Verbose output
- **Examples**:
  ```bash
  $ mv file.txt /new/location/
  $ mv old_name.txt new_name.txt
  $ mv -i file.txt /new/location/
  $ mv -v directory /new/location/
  ```

#### 3. File Content Commands

##### `cat` (Concatenate)

- **Purpose**: Displays file contents
- **Syntax**: `cat [options] file`
- **Options**:
  - `-n`: Number lines
  - `-b`: Number non-empty lines
  - `-s`: Squeeze multiple empty lines
- **Examples**:
  ```bash
  $ cat file.txt
  $ cat -n file.txt
  $ cat file1.txt file2.txt > combined.txt
  ```

##### `less` (View File)

- **Purpose**: Views file contents page by page
- **Syntax**: `less [options] file`
- **Navigation**:
  - Space: Next page
  - b: Previous page
  - /: Search
  - q: Quit
- **Examples**:
  ```bash
  $ less large_file.txt
  $ less -N file.txt
  ```

##### `head` (View Start of File)

- **Purpose**: Displays first lines of a file
- **Syntax**: `head [options] file`
- **Options**:
  - `-n`: Number of lines to show
  - `-c`: Number of bytes to show
- **Examples**:
  ```bash
  $ head file.txt
  $ head -n 5 file.txt
  $ head -c 100 file.txt
  ```

##### `tail` (View End of File)

- **Purpose**: Displays last lines of a file
- **Syntax**: `tail [options] file`
- **Options**:
  - `-n`: Number of lines to show
  - `-f`: Follow file updates
  - `-c`: Number of bytes to show
- **Examples**:
  ```bash
  $ tail file.txt
  $ tail -n 5 file.txt
  $ tail -f log.txt
  ```

#### 4. File Search Commands

##### `find` (Search Files)

- **Purpose**: Searches for files in directory hierarchy
- **Syntax**: `find [path] [expression]`
- **Common Expressions**:
  - `-name`: Search by name
  - `-type`: Search by type
  - `-size`: Search by size
  - `-mtime`: Search by modification time
- **Examples**:
  ```bash
  $ find /home -name "*.txt"
  $ find . -type f -size +1M
  $ find /var/log -mtime -7
  $ find . -name "*.log" -exec rm {} \;
  ```

##### `grep` (Search Text)

- **Purpose**: Searches for patterns in files
- **Syntax**: `grep [options] pattern [file]`
- **Options**:
  - `-i`: Case-insensitive
  - `-r`: Recursive search
  - `-n`: Show line numbers
  - `-v`: Invert match
- **Examples**:
  ```bash
  $ grep "error" log.txt
  $ grep -i "ERROR" log.txt
  $ grep -r "function" /src
  $ grep -n "warning" log.txt
  ```

##### `locate` (Find Files)

- **Purpose**: Finds files by name
- **Syntax**: `locate [options] pattern`
- **Options**:
  - `-i`: Case-insensitive
  - `-c`: Count matches
  - `-l`: Limit results
- **Examples**:
  ```bash
  $ locate config.txt
  $ locate -i "*.log"
  $ locate -c "*.txt"
  $ locate -l 5 "*.conf"
  ```

#### 5. Text Processing Commands

##### `sort` (Sort Lines)

- **Purpose**: Sorts text files
- **Syntax**: `sort [options] [file]`
- **Options**:
  - `-n`: Numeric sort
  - `-r`: Reverse sort
  - `-u`: Remove duplicates
  - `-k`: Sort by key
- **Examples**:
  ```bash
  $ sort file.txt
  $ sort -n numbers.txt
  $ sort -r file.txt
  $ sort -k2 file.txt
  ```

##### `uniq` (Remove Duplicates)

- **Purpose**: Removes duplicate lines
- **Syntax**: `uniq [options] [file]`
- **Options**:
  - `-c`: Count occurrences
  - `-d`: Show duplicates only
  - `-u`: Show unique lines only
- **Examples**:

  ```bash
  $ uniq file.txt
  $ uniq -c file.txt
  $ uniq -d file.txt
  $ sort file.txt | uniq
  ```

## System Administration Basics

### File Permissions

Linux uses a permission system with three types of permissions:

- **Read (r)**: 4
- **Write (w)**: 2
- **Execute (x)**: 1

Permission commands:

```bash
# Change permissions
chmod 755 file  # rwxr-xr-x
chmod u+x file  # Add execute for user

# Change ownership
chown user:group file
chgrp group file
```

### User and Group Management

```bash
# Add user
useradd username

# Set password
passwd username

# Add to group
usermod -aG groupname username

# Create group
groupadd groupname
```

Example:

```
sudo groupadd finacle
sudo useradd john
sudo passwd john
sudo usermod -aG finacle john
sudo mkdir /home/john
sudo chown john:finacle /home/john
```

### Process Management

```bash
# List processes
ps aux
ps -ef

# Interactive process viewer
top

# Kill process
kill PID
kill -9 PID  # Force kill
```

### Package Management

Ubuntu/Debian:

```bash
# Update package list
sudo apt update

# Install package
sudo apt install package_name

# Remove package
sudo apt remove package_name
```

CentOS/RHEL:

```bash
# Update package list
sudo yum update

# Install package
sudo yum install package_name

# Remove package
sudo yum remove package_name
```

### System Monitoring

```bash
# Disk usage
df -h
du -sh directory

# Memory usage
free -h

# System information
uname -a
```

### Additional Resources

- [Linux Documentation Project](https://tldp.org/)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- [Linux Journey](https://linuxjourney.com/)
- [Explain Shell](https://explainshell.com/)
