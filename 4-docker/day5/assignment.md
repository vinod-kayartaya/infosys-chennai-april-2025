# Assignment: Containers with SSH access

## Overview

In this assignment, you will create a local lab environment using Docker containers. You will set up three Ubuntu containers and configure SSH key-based authentication.

## Learning Objectives

- Set up Docker containers as Ansible managed nodes
- Configure SSH key-based authentication

## Assignment Tasks

### Task 1: Create the Project Structure

2. Create the following directory/file structure:
   ```
   lab/
   ├── docker-compose.yml
   ├── Dockerfile
   ├── ssh/
   ```

### Task 2: Create the Dockerfile

Create a Dockerfile that:

- Uses Ubuntu 22.04 as the base image
- Installs SSH server, Python, and other necessary packages
- Creates a user named "testuser" with sudo privileges
- Configures SSH to accept key-based authentication
- Sets up the appropriate directories for SSH keys

Write the Dockerfile with appropriate comments explaining each section.

### Task 3: Create the Docker Compose File

Create a `docker-compose.yml` file that:

- Defines three services named ubuntu-vm-1, ubuntu-vm-2, and ubuntu-vm-3
- Uses the Dockerfile you created
- Assigns static IP addresses to each container (e.g., 172.20.0.2, 172.20.0.3, 172.20.0.4)
- Configures volume mounting for the SSH authorized_keys file
- Creates a custom network for the containers

### Task 4: Set Up SSH Key Authentication

In the ./ssh folder:

1. Generate an SSH key pair
2. Create an `authorized_keys` file with the public key

### Task 5: Launch the Environment

1. Start the containers:

   ```bash
   docker-compose up -d
   ```

2. Verify the containers are running:
   ```bash
   docker ps
   ```

### Task 6: Test the Connection

1. Verify SSH connectivity to each container:
   ```bash
   ssh -i ssh/rsa_id testuser@172.20.0.2
   ssh -i ssh/rsa_id testuser@172.20.0.3
   ssh -i ssh/rsa_id testuser@172.20.0.4
   ```
