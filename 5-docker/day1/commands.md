# Docker Commands Reference

## Basic Docker Commands

### System Information

- `docker version` - Display Docker version information
  ```bash
  docker version
  ```
- `docker info` - Display system-wide information about Docker
  ```bash
  docker info
  ```

### Image Management

- `docker images` - List all local images
  ```bash
  docker images
  # or
  docker image ls
  ```
- `docker pull <image>` - Download an image from a registry
  ```bash
  docker pull nginx:latest
  docker pull ubuntu:20.04
  ```
- `docker rmi <image>` - Remove an image
  ```bash
  docker rmi nginx:latest
  docker rmi -f ubuntu:20.04  # Force remove
  ```

### Container Management

- `docker ps` - List running containers
  ```bash
  docker ps          # Show running containers
  docker ps -a       # Show all containers (including stopped)
  docker ps -q       # Show only container IDs
  ```
- `docker run <image>` - Create and start a new container
  ```bash
  docker run nginx                    # Run in foreground
  docker run -d nginx                 # Run in detached mode
  docker run -p 8080:80 nginx         # Map port 8080 to container's port 80
  docker run --name my-nginx nginx    # Assign a name to container
  ```
- `docker start <container>` - Start a stopped container
  ```bash
  docker start my-nginx
  ```
- `docker stop <container>` - Stop a running container
  ```bash
  docker stop my-nginx
  ```
- `docker rm <container>` - Remove a container
  ```bash
  docker rm my-nginx
  docker rm -f my-nginx  # Force remove running container
  ```

### Container Interaction

- `docker exec <container> <command>` - Execute a command in a running container
  ```bash
  docker exec -it my-nginx bash       # Get interactive shell
  docker exec my-nginx ls /var/www    # Run single command
  ```
- `docker logs <container>` - View container logs

  ```bash
  docker logs my-nginx
  docker logs -f my-nginx             # Follow log output
  docker logs --tail 100 my-nginx     # Show last 100 lines
  ```

### System Cleanup

- `docker system prune` - Remove unused data
  ```bash
  docker system prune              # Remove unused containers, networks, images
  docker system prune -a          # Remove all unused images
  docker system prune -f          # Force removal without confirmation
  ```

## Common Use Cases

### Running a Web Server

```bash
# Pull and run Nginx web server
docker pull nginx
docker run -d -p 80:80 --name web-server nginx
```

### Running a Database

```bash
# Run MySQL database
docker run -d \
  --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=secret \
  -p 3306:3306 \
  mysql:latest
```

### Building a Custom Image

```bash
# Create a Dockerfile
FROM nginx:latest
COPY ./index.html /usr/share/nginx/html/

# Build the image
docker build -t my-custom-nginx:v1 .

# Run the custom image
docker run -d -p 8080:80 my-custom-nginx:v1
```
