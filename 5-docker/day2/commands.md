# Docker Container Management Commands

## Container Lifecycle and States

### Container States Management

- `docker ps` - List containers with their states
  ```bash
  docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.State}}"
  ```
- `docker pause <container>` - Pause a running container
  ```bash
  docker pause my-nginx
  ```
- `docker unpause <container>` - Unpause a paused container
  ```bash
  docker unpause my-nginx
  ```
- `docker restart <container>` - Restart a container
  ```bash
  docker restart my-nginx
  docker restart --time 30 my-nginx  # Wait 30 seconds before killing
  ```

## Container Configuration

### Environment Variables

- `docker run -e` - Set environment variables

  ```bash
  # Single variable
  docker run -e MYSQL_ROOT_PASSWORD=secret mysql:latest

  # Using env file
  docker run --env-file ./config.env mysql:latest
  ```

### Port Mapping

- `docker run -p` - Map container ports to host

  ```bash
  # Basic port mapping
  docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=secret mysql:latest

  # Multiple ports
  docker run -p 3306:3306 -p 33060:33060 -e MYSQL_ROOT_PASSWORD=secret mysql:latest

  # Specific host interface
  docker run -p 127.0.0.1:3306:3306 -e MYSQL_ROOT_PASSWORD=secret mysql:latest
  docker run -p 192.168.204.132:3306:3306 -e MYSQL_ROOT_PASSWORD=secret mysql:latest

  # Bind to any available port
  docker run -p ::3306 -e MYSQL_ROOT_PASSWORD=secret mysql:latest
  ```

### Volume Mounting

- `docker run -v` - Mount volumes

  ```bash
  # Mount a directory
  docker run -v /host/path:/container/path nginx

  # Named volume
  docker run -v my-data:/data nginx

  # Read-only volume
  docker run -v /host/path:/container/path:ro nginx
  ```

### Resource Limits

- `docker run --memory` - Set memory limits
  ```bash
  docker run --memory="2g" --memory-swap="2g" nginx
  ```
- `docker run --cpus` - Set CPU limits
  ```bash
  docker run --cpus="1.5" nginx
  ```
- `docker run --cpu-shares` - Set CPU shares
  ```bash
  docker run --cpu-shares=512 nginx
  ```

### Container Linking

- `docker run --link` - Link containers (legacy)
  ```bash
  docker run --name web --link db:db nginx
  ```
- `docker run --network` - Connect to network
  ```bash
  docker run --network my-network nginx
  ```

### Container Health Checks

- `docker run --health-cmd` - Define health check
  ```bash
  docker run --health-cmd="curl -f http://localhost || exit 1" \
             --health-interval=30s \
             --health-timeout=3s \
             --health-retries=3 \
             nginx
  ```
- `docker inspect` - Check container health
  ```bash
  docker inspect --format='{{.State.Health.Status}}' my-nginx
  ```

## Monitoring and Logging

### Container Stats

- `docker stats` - Monitor container resource usage
  ```bash
  docker stats
  docker stats --no-stream  # One-time stats
  docker stats my-nginx     # Specific container
  ```

### Advanced Logging

- `docker logs` - View container logs with advanced options

  ```bash
  # Timestamp logs
  docker logs -t my-nginx

  # Since specific time
  docker logs --since 2024-03-20T10:00:00 my-nginx

  # Until specific time
  docker logs --until 2024-03-20T11:00:00 my-nginx
  ```

## Security and Best Practices

### Security Commands

- `docker run --read-only` - Run container in read-only mode
  ```bash
  docker run --read-only nginx
  ```
- `docker run --cap-drop` - Drop capabilities
  ```bash
  docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx
  ```
- `docker run --security-opt` - Set security options
  ```bash
  docker run --security-opt=no-new-privileges nginx
  ```

### Resource Monitoring

- `docker events` - Monitor Docker events
  ```bash
  docker events --filter 'container=my-nginx'
  ```
- `docker top` - Display running processes
  ```bash
  docker top my-nginx
  ```

## Common Container Management Scenarios

### Multi-Container Application

```bash
# Create network
docker network create app-network

# Run database
docker run -d \
  --name db \
  --network app-network \
  -e POSTGRES_PASSWORD=secret \
  postgres:latest

# Run application
docker run -d \
  --name app \
  --network app-network \
  -e DB_HOST=db \
  -p 8080:80 \
  my-app:latest
```

### Container with Resource Limits

```bash
docker run -d \
  --name resource-limited \
  --memory="1g" \
  --cpus="0.5" \
  --pids-limit=100 \
  -v app-data:/data \
  my-app:latest
```

### Health-Checked Container

```bash
docker run -d \
  --name health-checked \
  --health-cmd="curl -f http://localhost/health || exit 1" \
  --health-interval=30s \
  --health-timeout=3s \
  --health-retries=3 \
  --health-start-period=40s \
  my-app:latest
```

## Practical examples

### MySQL Container Example

```bash
# Create a named volume for MySQL data persistence
docker volume create mysql-data

# Run MySQL container with specified configurations
docker run -d \
  --name mysqldbserver \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=topsecret \
  -e MYSQL_USER=wordpressuser \
  -e MYSQL_PASSWORD=wordpresspassword \
  -e MYSQL_DATABASE=wordpress \
  -v mysql-data:/var/lib/mysql \
  --restart unless-stopped \
  mysql:latest

# Verify the container is running
docker ps | grep mysqldbserver

# Check container logs
docker logs mysqldbserver

# Connect to MySQL (from host machine)
docker exec -it mysqldbserver mysql -uroot -ptopsecret
```

### WordPress Container Example

```bash
# Create a named volume for WordPress data persistence
docker volume create wordpress-data

# Run WordPress container linked to MySQL
docker run -d \
  --name wordpress \
  --link mysqldbserver:mysql \
  -p 8080:80 \
  -e WORDPRESS_DB_HOST=mysqldbserver \
  -e WORDPRESS_DB_USER=wordpressuser \
  -e WORDPRESS_DB_PASSWORD=wordpresspassword \
  -e WORDPRESS_DB_NAME=wordpress \
  -v wordpress-data:/var/www/html \
  --restart unless-stopped \
  wordpress:latest

# Verify both containers are running
docker ps | grep -E 'wordpress|mysqldbserver'

# Check WordPress container logs
docker logs wordpress

# Access WordPress
# Open your browser and navigate to: http://localhost:8080
```

Note:

- WordPress will be accessible at http://localhost:8080
- The WordPress data will persist in the named volume 'wordpress-data'
- Both containers will automatically restart unless explicitly stopped
- The WordPress container is linked to the MySQL container using the `--link` flag
- WordPress will automatically create the database if it doesn't exist

### Jenkins Container Example

```bash
# Create a named volume for Jenkins data persistence
docker volume create jenkins-data

# Run Jenkins container with persistent storage
docker run -d \
  --name jenkins \
  -p 8081:8080 \
  -p 50000:50000 \
  -v jenkins-data:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --restart unless-stopped \
  jenkins/jenkins:lts

# Get the initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Verify the container is running
docker ps | grep jenkins

# Check Jenkins container logs
docker logs jenkins

# Access Jenkins
# Open your browser and navigate to: http://localhost:8081
```

Note for Jenkins:

- Jenkins will be accessible at http://localhost:8081
- The Jenkins data will persist in the named volume 'jenkins-data'
- Port 50000 is used for Jenkins agent communication
- The container has access to the host's Docker socket for running Docker commands
- Initial setup requires the admin password from the container logs
- The container will automatically restart unless explicitly stopped
- Using the LTS (Long Term Support) version for stability
- Jenkins home directory is persisted in the named volume
