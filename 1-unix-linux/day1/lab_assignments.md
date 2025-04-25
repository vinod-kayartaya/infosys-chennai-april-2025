# Day 1 Lab Assignments

## Assignment 1: File System Navigation and Basic Commands

### Learning Objectives

- Understand and use basic file system navigation commands
- Master file and directory manipulation
- Practice using command-line interface effectively

### Tasks

1. **Directory Navigation**

   ```bash
   # Create a directory structure
   mkdir -p lab1/{documents,images,backup}
   cd lab1
   ```

   - Create the directory structure shown above
   - Navigate through the directories using `cd`
   - Use `pwd` to verify your current location
   - Use `ls` with different options to view directory contents

2. **File Operations**

   ```bash
   # Create and manipulate files
   touch documents/{file1.txt,file2.txt,file3.txt}
   cp documents/file1.txt backup/
   mv documents/file2.txt images/
   ```

   - Create the files as shown
   - Copy and move files between directories
   - Verify file locations using `ls`
   - Practice using different `ls` options

3. **File Content Management**
   ```bash
   # Create and edit file content
   echo "This is a test file" > documents/file1.txt
   cat documents/file1.txt
   echo "Adding more content" >> documents/file1.txt
   ```
   - Create file content using `echo`
   - View file content using `cat`
   - Append content to files
   - Practice using `head` and `tail`

### Deliverables

- Screenshots or output of all commands executed
- Explanation of what each command does
- List of any errors encountered and how they were resolved

## Assignment 2: File Permissions and User Management

### Learning Objectives

- Understand Unix file permissions
- Learn to manage file access rights
- Practice user and group management

### Tasks

1. **File Permissions**

   ```bash
   # Create test files and set permissions
   touch test1.txt test2.txt test3.txt
   chmod 644 test1.txt
   chmod 755 test2.txt
   chmod 600 test3.txt
   ```

   - Create the test files
   - Set different permissions for each file
   - Use `ls -l` to verify permissions
   - Explain the meaning of each permission set

2. **User and Group Management**

   ```bash
   # Create test user and group
   sudo useradd vinod
   sudo groupadd finacle
   sudo usermod -aG finacle vinod
   ```

   - Create a test user and group
   - Add user to the group
   - Verify group membership
   - Set file ownership

3. **Permission Testing**
   ```bash
   # Test file access
   sudo chown vinod:finacle test1.txt
   sudo -u vinod cat test1.txt
   ```
   - Test file access with different users
   - Verify permission effectiveness
   - Document access results

### Deliverables

- Screenshots of permission settings
- Output of user and group management commands
- Documentation of permission testing results
- Explanation of permission numbers and their meaning

## Assignment 3: Process Management and System Monitoring

### Learning Objectives

- Understand process management in Unix
- Learn to monitor system resources
- Practice using system monitoring tools

### Tasks

1. **Process Management**

   ```bash
   # Start and manage processes
   sleep 100 &
   ps aux | grep sleep
   kill %1
   ```

   - Start background processes
   - List running processes
   - Kill processes using different methods
   - Monitor process status

2. **System Monitoring**

   ```bash
   # Monitor system resources
   top
   free -h
   df -h
   ```

   - Use `top` to monitor system processes
   - Check memory usage with `free`
   - Monitor disk usage with `df`
   - Identify resource-intensive processes

3. **System Information**
   ```bash
   # Gather system information
   uname -a
   cat /etc/os-release
   lscpu
   ```
   - Collect system information
   - Document system specifications
   - Analyze system configuration

### Deliverables

- Screenshots of process management commands
- System resource usage reports
- Documentation of system information
- Analysis of resource-intensive processes

## Assignment 4: Text Processing and File Searching

### Learning Objectives

- Master text processing commands
- Learn efficient file searching techniques
- Practice using regular expressions

### Tasks

1. **Text Processing**

   ```bash
   # Create and process text files
   echo -e "line1\nline2\nline3" > text.txt
   sort text.txt
   uniq text.txt
   grep "line" text.txt
   ```

   - Create sample text files
   - Practice sorting and filtering
   - Use grep for pattern matching
   - Combine commands using pipes

2. **File Searching**

   ```bash
   # Search for files
   find . -name "*.txt"
   find . -type f -mtime -1
   locate *.txt
   ```

   - Use `find` with different criteria
   - Search by file type and modification time
   - Use `locate` for quick searches
   - Update locate database

3. **Advanced Text Processing**
   ```bash
   # Process text with sed and awk
   sed 's/line/LINE/g' text.txt
   awk '{print $1}' text.txt
   ```
   - Use `sed` for text substitution
   - Process text with `awk`
   - Combine multiple commands
   - Create complex search patterns

### Deliverables

- Sample text files created
- Output of text processing commands
- Search results and patterns used
- Documentation of command combinations

## Additional Resources

- [Unix/Linux Command Reference](https://www.tldp.org/LDP/GNU-Linux-Tools-Summary/html/index.html)
- [Bash Scripting Guide](https://tldp.org/LDP/abs/html/)
- [Linux Documentation Project](https://tldp.org/)
- [Shell Scripting Tutorial](https://www.shellscript.sh/)
