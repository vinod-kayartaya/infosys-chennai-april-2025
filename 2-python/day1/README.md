# Day 1: Python Fundamentals and DevOps Automation

## Table of Contents

1. [Python Basics and Best Practices](#python-basics-and-best-practices)
2. [Essential Python Features](#essential-python-features)
3. [DevOps Automation with Python](#devops-automation-with-python)
4. [Network Operations](#network-operations)

## Python Basics and Best Practices

### Python Installation and Environment Setup

1. **Install Python 3.9+**

   ```bash
   # For macOS (using Homebrew)
   brew install python@3.9

   # For Ubuntu/Debian
   sudo apt update
   sudo apt install python3.9
   ```

2. **Create a Virtual Environment**

   ```bash
   # Create a new virtual environment
   python3 -m venv myenv

   # Activate the virtual environment
   # On macOS/Linux
   source myenv/bin/activate
   # On Windows
   myenv\Scripts\activate
   ```

3. **Install Required Packages**
   ```bash
   pip install requests
   ```

### PEP 8 Style Guide

PEP 8 is Python's official style guide. Here are key points:

1. **Indentation**: Use 4 spaces for indentation

   ```python
   def my_function():
       print("This is properly indented")
   ```

2. **Line Length**: Maximum 79 characters for code, 72 for docstrings

   ```python
   # Good
   def long_function_name(
           parameter_one, parameter_two,
           parameter_three, parameter_four):
       print("This follows PEP 8 line length guidelines")
   ```

3. **Imports**: Group imports in the following order:

   ```python
   # Standard library imports
   import os
   import sys

   # Third-party imports
   import requests

   # Local application imports
   from mypackage import mymodule
   ```

### Code Organization and Structure

1. **Project Structure**

   ```
   myproject/
   ├── README.md
   ├── requirements.txt
   ├── src/
   │   ├── __init__.py
   │   ├── main.py
   │   └── utils.py
   ├── tests/
   │   ├── __init__.py
   │   └── test_main.py
   └── docs/
       └── documentation.md
   ```

2. **Module Organization**

   ```python
   # main.py
   def main():
       """Main function that serves as the entry point."""
       pass

   if __name__ == "__main__":
       main()
   ```

## Essential Python Features

### Data Types and Structures

1. **Basic Types**

   ```python
   # Numbers
   integer = 42
   float_num = 3.14
   complex_num = 1 + 2j

   # Strings
   string = "Hello, World!"
   multi_line = """This is a
   multi-line string"""

   # Boolean
   is_true = True
   is_false = False
   ```

2. **Collections**

   ```python
   # Lists (mutable)
   my_list = [1, 2, 3, 4, 5]
   my_list.append(6)

   # Tuples (immutable)
   my_tuple = (1, 2, 3)

   # Dictionaries
   my_dict = {
       "name": "John",
       "age": 30,
       "city": "New York"
   }

   # Sets
   my_set = {1, 2, 3, 4, 5}
   ```

### Control Flow and Functions

1. **Conditional Statements**

   ```python
   age = 18
   if age >= 18:
       print("Adult")
   elif age >= 13:
       print("Teenager")
   else:
       print("Child")
   ```

2. **Loops**

   ```python
   # For loop
   for i in range(5):
       print(i)

   # While loop
   count = 0
   while count < 5:
       print(count)
       count += 1
   ```

3. **Functions**

   ```python
   def greet(name, greeting="Hello"):
       """Greet a person with a custom message."""
       return f"{greeting}, {name}!"

   # Function with type hints
   def calculate_area(length: float, width: float) -> float:
       return length * width
   ```

### Error Handling

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("This always executes")
```

### File I/O Operations

```python
# Writing to a file
with open("example.txt", "w") as f:
    f.write("Hello, World!")

# Reading from a file
with open("example.txt", "r") as f:
    content = f.read()
    print(content)

# Reading line by line
with open("example.txt", "r") as f:
    for line in f:
        print(line.strip())
```

## DevOps Automation with Python

### Working with System Modules

1. **OS Module**

   ```python
   import os

   # Get current working directory
   current_dir = os.getcwd()

   # List directory contents
   files = os.listdir(current_dir)

   # Create directory
   os.makedirs("new_directory", exist_ok=True)
   ```

2. **Sys Module**

   ```python
   import sys

   # Get Python version
   print(sys.version)

   # Get command line arguments
   print(sys.argv)
   ```

3. **Subprocess Module**

   ```python
   import subprocess

   # Run a command
   result = subprocess.run(["ls", "-l"], capture_output=True, text=True)
   print(result.stdout)

   # Run with shell
   subprocess.run("echo 'Hello, World!'", shell=True)
   ```

### File and Directory Operations

```python
import os
import shutil

# Copy file
shutil.copy("source.txt", "destination.txt")

# Move file
shutil.move("old_location.txt", "new_location.txt")

# Remove file
os.remove("file_to_delete.txt")

# Remove directory
shutil.rmtree("directory_to_delete")
```

### Process Management

```python
import psutil

# Get CPU usage
cpu_percent = psutil.cpu_percent(interval=1)

# Get memory usage
memory = psutil.virtual_memory()
print(f"Memory usage: {memory.percent}%")

# Get disk usage
disk = psutil.disk_usage('/')
print(f"Disk usage: {disk.percent}%")
```

### System Monitoring

```python
import psutil
import time

def monitor_system():
    while True:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"CPU Usage: {cpu_percent}%")

        # Memory usage
        memory = psutil.virtual_memory()
        print(f"Memory Usage: {memory.percent}%")

        # Disk usage
        disk = psutil.disk_usage('/')
        print(f"Disk Usage: {disk.percent}%")

        time.sleep(5)

# Run monitoring
monitor_system()
```

## Network Operations

### Requests Library

1. **Basic HTTP Requests**

   ```python
   import requests

   # GET request
   response = requests.get("https://api.example.com/data")
   print(response.status_code)
   print(response.json())

   # POST request
   data = {"name": "John", "age": 30}
   response = requests.post("https://api.example.com/users", json=data)
   ```

2. **Error Handling**
   ```python
   try:
       response = requests.get("https://api.example.com/data")
       response.raise_for_status()
   except requests.exceptions.RequestException as e:
       print(f"An error occurred: {e}")
   ```

### Working with APIs

```python
import requests

class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def get_data(self, endpoint):
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self.headers
        )
        return response.json()

    def post_data(self, endpoint, data):
        response = requests.post(
            f"{self.base_url}/{endpoint}",
            headers=self.headers,
            json=data
        )
        return response.json()

# Usage
client = APIClient("https://api.example.com", "your-api-key")
data = client.get_data("users")
```

## Additional Resources

1. [Python Official Documentation](https://docs.python.org/3/)
2. [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
3. [Requests Library Documentation](https://docs.python-requests.org/)
4. [psutil Documentation](https://psutil.readthedocs.io/)

## Next Steps

1. Practice writing Python scripts following PEP 8 guidelines
2. Experiment with different system monitoring tools
3. Create your own automation scripts for common tasks
4. Explore more advanced features of the requests library
5. Learn about error handling and logging best practices
