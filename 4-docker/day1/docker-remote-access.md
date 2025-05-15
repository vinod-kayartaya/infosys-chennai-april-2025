It is possible for a Docker CLI to interact with a remote Docker Engine. This can be done by setting the `DOCKER_HOST` environment variable or using the `--host` (or `-H`) flag in your Docker commands.

### How It Works

By default, Docker CLI talks to the Docker Engine using a Unix socket on the local machine. To communicate with a remote Docker Engine, you can point the CLI to a remote API endpoint.

### Example Setup

1. **Enable Remote API on Docker Engine:**

   On the remote machine (where Docker Engine runs), configure Docker to listen on a TCP socket:

   - Edit or create the systemd service override:

     ```bash
     sudo systemctl edit docker
     ```

   - Add the following override (or modify the existing one):

     ```ini
     [Service]
     ExecStart=
     ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
     ```

   - Reload and restart Docker:

     ```bash
     sudo systemctl daemon-reexec
     sudo systemctl restart docker
     ```

   **Warning**: Port `2375` is insecure (unencrypted and unauthenticated). Use TLS (`2376`) for production.

2. **From Your Local Machine:**
   Set the environment variable or pass the host in CLI:

   ```bash
   export DOCKER_HOST=tcp://<remote-ip>:2375
   docker ps
   ```

   Or use the host flag:

   ```bash
   docker -H tcp://<remote-ip>:2375 ps
   ```

3. **(Optional) Secure with TLS:**
   For secure remote access, configure the Docker Engine with TLS certificates and connect like this:

   ```bash
   export DOCKER_HOST=tcp://<remote-ip>:2376
   export DOCKER_TLS_VERIFY=1
   export DOCKER_CERT_PATH=~/.docker/certs
   docker ps
   ```
