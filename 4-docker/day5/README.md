# Docker Compose (contd.), Networking, Volumes and Advanced Topics

## Table of Contents

- [Docker Networking](#docker-networking)
- [Service Discovery](#service-discovery)
- [Docker Volumes](#docker-volumes)
- [Storage Management](#storage-management)
- [Security and Best Practices](#security-and-best-practices)

## Docker Networking

Docker networking enables communication between containers, as well as between containers and the outside world.

### Network Drivers

Docker supports several network drivers, each with its own use case:

1. **bridge**: The default network driver. It creates an internal network where containers can communicate with each other.
2. **host**: Removes network isolation between the container and the Docker host.
3. **overlay**: Connects multiple Docker daemons and enables Swarm services to communicate.
4. **macvlan**: Assigns a MAC address to a container, making it appear as a physical device on the network.
5. **none**: Disables networking for a container.

**Example: Using Different Network Drivers**

```yaml
version: '3.8'
networks:
  default_bridge:
    driver: bridge

  direct_host:
    driver: host

  swarm_network:
    driver: overlay
    attachable: true

  virtual_devices:
    driver: macvlan
    driver_opts:
      parent: eth0
```

### Network Types

In Docker Compose, you can define different types of networks:

1. **Default Network**: Automatically created for each Compose project.
2. **Custom Networks**: User-defined networks with specific configurations.
3. **External Networks**: Networks created outside of Compose but used by Compose services.

**Example: Network Types**

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    networks:
      - frontend

  database:
    image: postgres:13
    networks:
      - backend

networks:
  frontend:
    name: custom_frontend
    driver: bridge

  backend:
    external: true
    name: existing_backend_network
```

In this example:

- `frontend` is a custom network that will be created by Compose
- `backend` is an external network that must exist before running `docker-compose up`

### Network Configuration

Docker networks can be configured with various options to control IP allocation, subnet, gateway, and more.

**Example: Advanced Network Configuration**

```yaml
version: '3.8'
networks:
  app_network:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
          ip_range: 172.28.5.0/24
          gateway: 172.28.5.254
    driver_opts:
      com.docker.network.bridge.default_bridge: 'false'
      com.docker.network.bridge.enable_icc: 'true'
      com.docker.network.bridge.enable_ip_masquerade: 'true'
```

### Network Security

Docker provides several features to secure your container networks:

1. **Network Isolation**: By using multiple networks, you can isolate containers from each other.
2. **Internal Networks**: Networks marked as `internal` cannot communicate with the outside world.
3. **Network Aliases**: Allow containers to be discoverable by multiple names.

**Example: Network Security Configuration**

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    networks:
      frontend:
        aliases:
          - web.local
      internal:
        aliases:
          - web.internal

  api:
    image: node:14
    networks:
      - internal

  database:
    image: postgres:13
    networks:
      - internal

networks:
  frontend:
    driver: bridge

  internal:
    driver: bridge
    internal: true # Prevents access from outside Docker
```

In this example:

- The `web` service is accessible from both the `frontend` and `internal` networks
- The `api` and `database` services are only accessible from the `internal` network
- Containers in the `internal` network can refer to the `web` service as `web.internal`
- External clients cannot directly access the `internal` network

## Service Discovery

Service discovery is the process of automatically detecting and connecting to services on a network.

### DNS Configuration

Docker provides automatic DNS resolution for containers within the same network. Containers can communicate with each other using service names.

**Example: DNS Resolution**

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    networks:
      - app_network

  api:
    image: node:14
    networks:
      - app_network
    environment:
      - API_URL=http://web:80 # Using service name for DNS resolution

networks:
  app_network:
    driver: bridge
```

In this example, the `api` service can communicate with the `web` service using the hostname `web`.

You can also configure custom DNS settings:

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    dns:
      - 8.8.8.8
      - 8.8.4.4
    dns_search:
      - example.com
      - internal.local
```

### Load Balancing

Docker Swarm provides built-in load balancing for services with multiple replicas.

**Example: Load Balancing with Docker Swarm**

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    deploy:
      replicas: 3
      endpoint_mode: vip # Virtual IP for load balancing (default)
    ports:
      - '8080:80'

  api:
    image: node:14
    deploy:
      replicas: 5
      endpoint_mode: dnsrr # DNS Round Robin for load balancing
```

In this example:

- The `web` service uses VIP (Virtual IP) mode, where Docker assigns a virtual IP to the service and load balances requests
- The `api` service uses DNS Round Robin, where DNS resolution returns different IPs for each request

### Service Communication

Services communicate with each other using DNS names over the Docker network.

**Example: Service Communication**

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    networks:
      - frontend

  api:
    image: node:14
    networks:
      - frontend
      - backend
    environment:
      - DATABASE_URL=postgres://user:password@database:5432/appdb

  database:
    image: postgres:13
    networks:
      - backend
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=appdb

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

In this example:

- The `api` service connects to the `database` service using the hostname `database`
- The connection is secured because the `database` service is only accessible through the `backend` network, which is internal

### Network Troubleshooting

When troubleshooting Docker networking issues, several commands are useful:

1. **Inspect Networks**:

   ```bash
   docker network ls
   docker network inspect <network_name>
   ```

2. **Inspect Containers**:

   ```bash
   docker inspect <container_name>
   ```

3. **Check Connectivity from inside a Container**:

   ```bash
   docker exec -it <container_name> ping <other_container_name>
   docker exec -it <container_name> curl <other_container_name>:<port>
   ```

4. **View Network Statistics**:

   ```bash
   docker stats <container_name>
   ```

5. **Check Container Logs**:
   ```bash
   docker logs <container_name>
   ```

**Example: Diagnosing Network Issues**

Let's say you have the following Compose file:

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - '8080:80'
    networks:
      - frontend

  api:
    image: node:14
    networks:
      - frontend
      - backend

  database:
    image: postgres:13
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

If the `web` service cannot communicate with the `database` service, you can troubleshoot as follows:

1. Verify network configuration:

   ```bash
   docker network inspect frontend
   docker network inspect backend
   ```

2. Check container connectivity:

   ```bash
   # From web container to api
   docker exec -it <web_container> ping api

   # From api container to database
   docker exec -it <api_container> ping database
   ```

3. Examine container network settings:
   ```bash
   docker inspect <web_container> | grep -A 20 "Networks"
   docker inspect <database_container> | grep -A 20 "Networks"
   ```

The issue would be that the `web` and `database` services don't share a common network. The `api` service can communicate with both because it's connected to both networks, but `web` can't directly reach `database`.

## Docker Volumes

### Volume Types

Docker offers several different ways to manage data in containers:

1. **Named Volumes**: Docker-managed volumes that exist independently of containers
2. **Bind Mounts**: Maps a host directory directly into a container
3. **tmpfs Mounts**: Temporary file storage in memory (Linux only)
4. **Anonymous Volumes**: Similar to named volumes but with automatically generated names

#### Named Volumes Example

```bash
# Create a named volume
docker volume create my_data

# Run a container with the volume mounted
docker run -d --name my_app --volume my_data:/app/data nginx
```

In this example, we:

- Create a volume called `my_data`
- Run an Nginx container that mounts this volume at `/app/data` inside the container
- Any data written to `/app/data` will persist even if the container is removed

#### Bind Mount Example

```bash
# Run a container with a bind mount
docker run -d --name web_server -v $(pwd)/html:/usr/share/nginx/html nginx
```

Here, we mount the local `html` directory from the current working directory into the container at `/usr/share/nginx/html`. This is useful during development when you want to see changes immediately reflected in the container.

#### tmpfs Mount Example

```bash
# Create a container with a temporary in-memory filesystem
docker run -d --name temp_processor --tmpfs /app/temp:rw,noexec,nosuid,size=100m alpine sh -c "while true; do sleep 1000; done"
```

This creates a temporary filesystem at `/app/temp` with a size limit of 100MB. The data will be stored in memory and not persist when the container stops.

Here's what each part means:

- `docker run`: Creates and starts a new Docker container
- `-d`: Runs the container in detached mode (in the background)
- `--name temp_processor`: Names the container "temp_processor" for easy reference
- `--tmpfs /app/temp:rw,noexec,nosuid,size=100m`: Creates a temporary filesystem mounted at `/app/temp` in the container with these options:
  - `rw`: Read-write permissions
  - `noexec`: Prevents executing files from this filesystem
  - `nosuid`: Prevents the use of setuid/setgid bits
  - `size=100m`: Limits the size to 100 megabytes
- `alpine`: Uses the lightweight Alpine Linux image
- `sh -c "while true; do sleep 1000; done"`: Runs a simple shell command that keeps the container running indefinitely by creating an infinite loop that sleeps for 1000 seconds each iteration

This container is essentially setting up a secure, memory-based temporary storage area limited to 100MB that applications can use for processing temporary files without writing to disk. The container will continue running until manually stopped, and any data in the tmpfs will be automatically cleared when the container stops.

You can achieve similar functionality without using `tmpfs` by simply creating the `/app/temp` directory in a regular Docker container. Let me explain the key differences:

#### Using a regular directory instead of tmpfs

You could replace your original command with something like:

```bash
docker run -d --name regular_processor alpine sh -c "mkdir -p /app/temp && while true; do sleep 1000; done"
```

#### Key differences

1. **Storage location**:

   - Regular directory: Stored on the container's filesystem (which uses the host's disk)
   - tmpfs: Stored in RAM, not on disk

2. **Performance**:

   - Regular directory: Normal disk I/O speeds
   - tmpfs: Much faster since it's in RAM

3. **Data persistence**:

   - Regular directory: Data remains until the container is removed
   - tmpfs: Data is completely lost when the container stops

4. **Security**:

   - Regular directory: Data can potentially be recovered from disk
   - tmpfs: Data is never written to disk (useful for sensitive information)

5. **Resource usage**:
   - Regular directory: Uses disk space
   - tmpfs: Uses RAM (which might be more limited)

**Use a regular directory when**:

- You need to persist the data
- You're working with large files that would consume too much RAM
- Performance isn't critical
- The security benefit of in-memory-only storage isn't needed

**Use tmpfs when**:

- You need very high-speed temporary storage
- You're working with sensitive data that shouldn't be written to disk
- You want the data to be automatically cleaned up
- You need the security benefits of noexec, nosuid, etc.

So, for many use cases, simply creating `/app/temp` as a regular directory would work fine, especially if you don't need the specific benefits that tmpfs provides.

### Volume Drivers

Docker supports various volume drivers to extend storage capabilities:

1. **local**: Default driver that stores volumes on the host filesystem
2. **nfs**: For mounting NFS shares
3. **cifs**: For Windows file shares
4. **Amazon EBS**: For AWS EC2 instances
5. **Azure File Storage**: For Azure cloud services
6. **GCE-PD**: For Google Cloud Platform

#### Using an NFS Volume Example

```bash
# Create a volume using the NFS driver
docker volume create --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.10,rw \
  --opt device=:/path/to/share \
  nfs_storage

# Use the volume with a container
docker run -d --name nfs_user --volume nfs_storage:/data alpine
```

This creates a volume that connects to an NFS server at 192.168.1.10 and mounts the share to `/data` in the container.

### Volume Management

Docker provides commands to manage volumes throughout their lifecycle:

#### Listing Volumes

```bash
# List all volumes
docker volume ls

# Filter volumes by driver
docker volume ls --filter driver=local
```

#### Inspecting Volumes

```bash
# Get detailed information about a volume
docker volume inspect my_data
```

This returns details including:

- Mount point on the host
- Driver information
- Volume labels
- Creation time

#### Removing Volumes

```bash
# Remove a specific volume
docker volume rm my_data

# Remove all unused volumes
docker volume prune
```

Be careful with `docker volume prune` as it removes all volumes not used by at least one container.

### Data Persistence

The primary purpose of volumes is data persistence. Let's explore a practical scenario:

```bash
# Create a PostgreSQL container with a volume for data
docker volume create pg_data

docker run -d \
  --name my_postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v pg_data:/var/lib/postgresql/data \
  postgres:13
```

Now let's simulate a container failure:

```bash
# Stop and remove the container
docker stop my_postgres
docker rm my_postgres

# Create a new container using the same volume
docker run -d \
  --name new_postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v pg_data:/var/lib/postgresql/data \
  postgres:13
```

The new container will have access to all the data created in the previous container, demonstrating how volumes enable data persistence across container lifecycle events.

## Storage Management

### Volume Backup

Backing up volumes is crucial for data safety. Here are methods to back up your Docker volumes:

#### Using tar for Volume Backup

```bash
# Create a temporary container to backup the volume
docker run --rm \
  -v pg_data:/source:ro \
  -v $(pwd):/backup \
  alpine tar -czf /backup/pg_data_backup.tar.gz -C /source .
```

This command:

1. Creates a temporary Alpine container
2. Mounts our PostgreSQL volume as read-only at `/source`
3. Mounts the current directory at `/backup`
4. Uses `tar` to create a compressed backup file

### Volume Restore

Restoring from backups is equally important:

#### Restoring from tar Backup

```bash
# Create a new volume if needed
docker volume create pg_data_restored

# Restore the backup to the new volume
docker run --rm \
  -v pg_data_restored:/destination \
  -v $(pwd):/backup \
  alpine sh -c "tar -xzf /backup/pg_data_backup.tar.gz -C /destination"
```

This process:

1. Creates a temporary container
2. Mounts our backup file and target volume
3. Extracts the tar archive to the destination volume

#### Testing the Restored Volume

```bash
# Start a container with the restored volume
docker run -d \
  --name restored_postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v pg_data_restored:/var/lib/postgresql/data \
  postgres:13
```

### Data Migration

Sometimes you need to migrate data between environments:

#### Migration Between Hosts Example

Assuming you have SSH access to both hosts:

```bash
# On source host: Create a backup
docker run --rm \
  -v pg_data:/source:ro \
  -v $(pwd):/backup \
  alpine tar -czf /backup/pg_data_backup.tar.gz -C /source .

# Transfer the backup to the destination host
scp pg_data_backup.tar.gz user@destination-host:/tmp/

# On destination host: Restore the backup
docker volume create pg_data
docker run --rm \
  -v pg_data:/destination \
  -v /tmp:/backup \
  alpine sh -c "tar -xzf /backup/pg_data_backup.tar.gz -C /destination"
```

#### Migration to Cloud Storage

For larger volumes, consider using cloud storage services:

```bash
# Backup to AWS S3
docker run --rm \
  -v pg_data:/source:ro \
  -e AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY \
  -e AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY \
  amazon/aws-cli \
  s3 sync /source s3://my-bucket/pg_data_backup

# Restore from AWS S3
docker run --rm \
  -v pg_data_new:/destination \
  -e AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY \
  -e AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY \
  amazon/aws-cli \
  s3 sync s3://my-bucket/pg_data_backup /destination
```

### Storage Optimization

Managing storage efficiently prevents resource waste:

#### Volume Cleanup Strategies

```bash
# Remove containers that aren't running
docker container prune

# Remove all unused volumes
docker volume prune

# Remove all unused images, containers, networks, and volumes
docker system prune -a --volumes
```

#### Monitoring Volume Usage

```bash
# Check overall Docker disk usage
docker system df

# Get detailed volume usage
docker system df -v
```

#### Compression for Database Volumes

For database containers, enable compression when available:

```bash
# For PostgreSQL, enable compression
docker run -d \
  --name postgres_compressed \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e PGSQL_COMPRESSION=TRUE \
  -v pg_data:/var/lib/postgresql/data \
  postgres:13
```

## Security and Best Practices

### Container Security

#### Principle of Least Privilege

Always run containers with minimal permissions:

```bash
# Run a container with a non-root user
docker run -d --name secure_app \
  --user 1000:1000 \
  nginx
```

#### Read-Only Filesystem

Make the container filesystem read-only where possible:

```bash
# Run with read-only filesystem, providing writable temporary storage where needed
docker run -d --name secure_web \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /var/cache/nginx \
  nginx
```

#### Resource Limits

Set memory and CPU limits to prevent container DoS:

```bash
# Limit container to 512MB RAM and 1 CPU
docker run -d --name limited_app \
  --memory="512m" \
  --cpus="1.0" \
  nginx
```

#### Linux Security Modules

Use security modules like AppArmor or SELinux:

```bash
# Run with a specific AppArmor profile
docker run -d --name secure_nginx \
  --security-opt apparmor=docker-nginx \
  nginx
```

### Image Security

#### Use Official and Verified Images

Always prefer official images from Docker Hub:

```bash
# Use the official image with a specific version tag
docker pull nginx:1.21.6-alpine

# Avoid using the 'latest' tag in production
```

#### Build Secure Images

Create a minimal image with fewer attack vectors:

```dockerfile
# Use a minimal base image
FROM alpine:3.15

# Install only what's needed
RUN apk add --no-cache nodejs npm

# Run as non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Set up the application
WORKDIR /app
COPY --chown=appuser:appgroup . .
RUN npm ci --production

# Use specific ports
EXPOSE 3000

CMD ["node", "server.js"]
```

#### Multi-Stage Builds

Use multi-stage builds to reduce image size and attack surface:

```dockerfile
# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./

USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### Network Security

#### Create Network Isolation

```bash
# Create a custom bridge network
docker network create --driver bridge app_network

# Run containers in the isolated network
docker run -d --name api --network app_network api_service
docker run -d --name db --network app_network postgres
```

#### Restrict External Access

```bash
# Only expose necessary ports
docker run -d --name web \
  --network app_network \
  -p 443:443 \
  nginx
```

#### Encrypt Container Communications

For sensitive data, use encrypted networks:

```bash
# Create an overlay network with encryption (for Docker Swarm)
docker network create --driver overlay --opt encrypted=true secure_network
```
