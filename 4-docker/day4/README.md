# Docker Compose

This tutorial provides a comprehensive guide to Docker Compose and Docker networking concepts, from fundamentals to advanced techniques. Each section includes practical examples to help you understand and apply these concepts in real-world scenarios.

## Table of Contents

- [Docker Compose Fundamentals](#docker-compose-fundamentals)
- [Advanced Docker Compose](#advanced-docker-compose)

## Docker Compose Fundamentals

Docker Compose is a tool for defining and running multi-container Docker applications. It uses YAML files to configure application services and allows you to create and start all services with a single command.

### Compose File Structure

The Docker Compose file (typically named `docker-compose.yml`) follows a specific structure:

```yaml
version: '3.8' # Compose file version

services: # Container definitions
  service1:
    # service configuration

  service2:
    # service configuration

volumes: # Volume definitions (optional)
  volume1:
    # volume configuration

networks: # Network definitions (optional)
  network1:
    # network configuration
```

The current stable version is 3.8, though Docker Compose also supports older versions.

- Each version may have different features and syntax. The version key is no longer required starting with Docker Compose v1.27.0, as the Compose file format was unified into a single specification.
- The Compose Specification supports backward compatibility with earlier file formats like 2, 2.1, 3, 3.7, etc., but you should now omit the version key when writing new docker-compose.yml files.
- All Compose implementations (CLI, Compose V2 plugin, etc.) now automatically infer the capabilities based on the defined services and configuration.

### Service Definitions

Services are the core of a Docker Compose file. Each service defines a container that will be created when you run Docker Compose.

**Example: Basic Web Application with Database**

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - '8080:80'

  database:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: example
      MYSQL_DATABASE: myapp
```

In this example:

- We define two services: `web` and `database`
- The `web` service uses the latest Nginx image and maps port 8080 on the host to port 80 in the container
- The `database` service uses MySQL 8.0 with some environment variables

Here's a more detailed service definition with common configuration options:

```yaml
services:
  webapp:
    build: ./webapp # Build from Dockerfile in ./webapp directory
    image: myapp:latest # Image name (if built)
    container_name: myapp # Custom container name
    restart: always # Restart policy
    ports:
      - '3000:3000' # Port mapping (host:container)
    volumes:
      - ./app:/app # Volume mount
    environment: # Environment variables
      NODE_ENV: production
    command: npm start # Override default command
    depends_on: # Service dependencies
      - database
```

### Network Configuration

Docker Compose automatically creates a default network for your application. However, you can define custom networks for more control.

**Example: Custom Network Configuration**

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

  database:
    image: postgres:13
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true # This network is not accessible from outside
```

In this example:

- We define two networks: `frontend` and `backend`
- The `web` service is only connected to the `frontend` network
- The `api` service is connected to both networks and can communicate with both `web` and `database`
- The `database` service is only connected to the `backend` network and is isolated from the `web` service
- The `backend` network is internal, meaning it's not accessible from outside the Docker host

### Volume Configuration

Volumes are used to persist data and share files between the host and containers.

**Example: Volume Configuration**

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    volumes:
      - ./html:/usr/share/nginx/html # Bind mount
      - nginx_logs:/var/log/nginx # Named volume

  database:
    image: postgres:13
    volumes:
      - db_data:/var/lib/postgresql/data # Named volume for persistence

volumes:
  nginx_logs: # Named volume definition
    driver: local

  db_data: # Named volume definition
    driver: local
```

In this example:

- The `web` service uses a bind mount to map the local `./html` directory to `/usr/share/nginx/html` in the container
- It also uses a named volume `nginx_logs` for storing logs
- The `database` service uses a named volume `db_data` to persist the database data

## Advanced Docker Compose

### Environment Variables

Environment variables can be set directly in the Compose file or loaded from external files.

**Example: Environment Variables**

```yaml
version: '3.8'
services:
  web:
    image: node:14
    environment:
      - NODE_ENV=production
      - API_URL=http://api:3000

  api:
    image: node:14
    env_file:
      - ./api.env # Load environment variables from file
```

The `api.env` file might look like:

```
NODE_ENV=production
DB_HOST=database
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=secret
```

You can also reference environment variables from the shell:

```yaml
services:
  web:
    image: node:14
    environment:
      - NODE_ENV=${NODE_ENV:-development} # Use shell variable with default
```

### Service Dependencies

Service dependencies define the order in which services are started. The `depends_on` option ensures that services are started in the correct order.

**Example: Service Dependencies**

```yaml
version: '3.8'
services:
  web:
    image: myapp:latest
    depends_on:
      - api
      - redis

  api:
    image: myapi:latest
    depends_on:
      - database

  redis:
    image: redis:latest

  database:
    image: postgres:13
```

In this example:

- The `web` service depends on both `api` and `redis`
- The `api` service depends on `database`
- Docker Compose will start the services in the correct order: first `database` and `redis`, then `api`, and finally `web`

**Note**: `depends_on` only waits for services to start, not for them to be "ready" (e.g., database initialization). For that, you need health checks.

### Health Checks

Health checks allow Docker to determine if a container is running correctly.

When a healthcheck fails:

1. The container is marked as unhealthy
2. Docker will report the container's status as unhealthy in `docker ps` and `docker container ls` output
3. If the container is part of a service with `depends_on` conditions, dependent services may be affected
4. The container continues running unless configured otherwise
5. Docker will keep retrying the healthcheck according to the specified interval

**Example: Health Checks**

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost']
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  database:
    image: postgres:13
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U postgres']
      interval: 10s
      timeout: 5s
      retries: 5
```

You can also use health checks with `depends_on` for more robust service dependencies:

```yaml
version: '3.8'
services:
  web:
    image: myapp:latest
    depends_on:
      database:
        condition: service_healthy

  database:
    image: postgres:13
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U postgres']
      interval: 10s
      timeout: 5s
      retries: 5
```

In this example, the `web` service will only start after the `database` service passes its health check.

In the healthcheck configuration:

- `CMD`: Runs the command directly in the container without a shell. The command is specified as an array of strings, where each element is a separate argument. This is more efficient and secure as it doesn't involve a shell process.

  ```yaml
  healthcheck:
    test: ['CMD', 'curl', '-f', 'http://localhost'] # Runs: curl -f http://localhost
  ```

- `CMD-SHELL`: Runs the command through a shell (/bin/sh -c in Linux or cmd /S /C in Windows). This allows you to use shell features like pipes, redirections, and environment variables, but is slightly less secure and efficient due to the additional shell process.
  ```yaml
  healthcheck:
    test: ['CMD-SHELL', 'curl -f http://localhost || exit 1'] # Runs through shell
  ```

### Scaling Services

Docker Compose allows you to run multiple instances of a service, which is useful for load balancing and high availability.

**Example: Scaling Services**

```yaml
version: '3.8'
services:
  worker:
    image: myworker:latest
    deploy:
      mode: replicated
      replicas: 3

  database:
    image: postgres:13
    deploy:
      mode: global # One instance per swarm node
```

To start the services with dynamic scaling:

```bash
docker-compose up --scale worker=5
```

This command will start 5 instances of the `worker` service.
