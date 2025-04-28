# Day 3: Security and Automation in Unix/Linux

## Table of Contents

1. [Security and Authentication](#security-and-authentication)
   - [Encryption Basics](#encryption-basics)
   - [GPG and OpenSSL Usage](#gpg-and-openssl-usage)
   - [SSH Key Management](#ssh-key-management)
   - [OAuth Concepts](#oauth-concepts)
   - [Authentication Best Practices](#authentication-best-practices)
   - [Secure File Transfer](#secure-file-transfer)
2. [System Automation](#system-automation)
   - [Cron and At Scheduling](#cron-and-at-scheduling)
   - [Systemd Services](#systemd-services)
   - [Backup Strategies](#backup-strategies)
   - [Best Practices](#best-practices)

## Security and Authentication

### Encryption Basics

Encryption is the process of encoding information so that only authorized parties can access it. There are two main types of encryption:

1. **Symmetric Encryption**

   - Uses a single key for both encryption and decryption
   - Faster and simpler than asymmetric encryption
   - Common algorithms: AES, DES, 3DES
   - Key must be securely shared between parties
   - Best for encrypting large amounts of data

2. **Asymmetric Encryption**
   - Uses a pair of mathematically related keys:
     - Public key for encryption
     - Private key for decryption
   - More complex and computationally intensive
   - Common algorithms: RSA, ECC
   - No need to share secret keys
   - Often used for key exchange and digital signatures

Key concepts:

- **Plaintext**: The original, readable data
- **Ciphertext**: The encrypted, scrambled data
- **Key**: The secret information used to encrypt/decrypt
- **Algorithm**: The mathematical process used for encryption
- **Salt**: Random data added to increase security
- **Initialization Vector (IV)**: Random block used to add randomness

Common use cases:

- Securing communications (HTTPS, SSH)
- Protecting stored data
- Digital signatures
- Secure key exchange

#### Symmetric Encryption

Symmetric encryption uses the same key for both encryption and decryption. It's faster but requires secure key distribution.

Example using OpenSSL for symmetric encryption:

```bash
# Encrypt a file (using PBKDF2)
openssl enc -aes-256-cbc -pbkdf2 -salt -in secret.txt -out secret.enc


# Decrypt the file (use same options as encryption)
openssl enc -aes-256-cbc -pbkdf2 -d -in secret.enc -out secret.txt
```

Let's break down the symmetric encryption example:

- `-aes-256-cbc`: Specifies AES (Advanced Encryption Standard) encryption with:
  - 256-bit key length
  - CBC (Cipher Block Chaining) mode
- `-pbkdf2`: Uses PBKDF2 (Password-Based Key Derivation Function 2) for secure key derivation
- `-salt`: Adds random data to strengthen encryption
- `-in`: Input file to encrypt
- `-out`: Output file for encrypted data
- `-d`: Decrypt flag (for decryption)

The process:

1. OpenSSL prompts for a password
2. Password is securely converted to key using PBKDF2
3. File is encrypted/decrypted using AES
4. Salt is automatically prepended to encrypted file

#### Asymmetric Encryption

Asymmetric encryption uses a pair of keys: public and private. The public key encrypts data, while the private key decrypts it.

Example using GPG:

```bash
# Generate a key pair
gpg --full-generate-key

# Export public key
gpg --export --armor user@example.com > public.key

# Export private key
gpg --export-secret-keys --armor user@example.com > private.key
```

### GPG and OpenSSL Usage

#### GPG (GNU Privacy Guard)

GPG is a complete implementation of the OpenPGP standard. It provides a robust suite of encryption tools for secure communication and file protection. Key features include:

- Public/private key pair management for asymmetric encryption
- Digital signatures to verify message authenticity
- File encryption and decryption capabilities
- Key server integration for public key distribution
- Smart card support for enhanced security
- Integration with email clients for encrypted communication
- Support for multiple encryption algorithms and key sizes
- Command line and GUI interfaces available

GPG follows the OpenPGP standard (RFC 4880) ensuring interoperability with other PGP implementations. It's free, open source software that serves as a complete replacement for Symantec's PGP cryptographic software suite.

#### Client-Server Communication with GPG

GPG enables secure communication between clients and servers through asymmetric encryption. Here are the detailed steps for both machines:

Server-side Setup:

1. Generate key pair on server:

   ```bash
   # Generate new key pair
   gpg --full-generate-key

   # Export public key to share with clients
   gpg --export --armor server@example.com > server_public.key
   ```

2. Share public key with clients:
   - Send via email
   - Host on website
   - Upload to key server
   ```bash
   # Optional: Upload to key server
   gpg --keyserver keyserver.ubuntu.com --send-keys KEY_ID
   ```

Client-side Encryption:

1. Import server's public key:

   ```bash
   # Import server's public key
   gpg --import server_public.key

   # Trust the key
   gpg --edit-key server@example.com trust
   ```

2. Encrypt files/messages:

   ```bash
   # Encrypt file for server
   gpg --encrypt --recipient server@example.com sensitive_file.txt

   # Encrypt message
   echo "Secret message" | gpg --encrypt --recipient server@example.com > message.gpg
   ```

Server-side Decryption:

1. Receive encrypted file/message
2. Decrypt using private key:

   ```bash
   # Decrypt file
   gpg --decrypt sensitive_file.txt.gpg > decrypted_file.txt

   # Decrypt message
   gpg --decrypt message.gpg
   ```

Key Security Considerations:

- Server must keep private key secure and never share it
- Clients must verify authenticity of server's public key
- Regular key rotation and backups recommended
- Use strong passphrases for private keys

#### OpenSSL

OpenSSL (Open Secure Sockets Layer) is a robust toolkit for SSL (Secure Sockets Layer)/TLS (Transport Layer Security) protocols and general-purpose cryptography. It provides extensive functionality for:

- SSL/TLS implementation
- Certificate management
- Encryption/decryption
- Key generation and management
- Cryptographic operations

Here's a detailed guide on common OpenSSL operations:

1. **Generate Private Key and Public Key**:

   ```bash
   # Generate 2048-bit RSA private key
   openssl genrsa -out private.key 2048

   # Extract public key from private key
   openssl rsa -in private.key -pubout -out pubkey.pem
   ```

   Note: For encryption/decryption purposes, the client only needs the pubkey.pem file.

2. **Create Certificate (Optional - for SSL/TLS and Identity Verification)**:

   ```bash
   # Generate Certificate Signing Request (CSR)
   openssl req -new -key private.key -out certificate.csr

   # Generate self-signed certificate
   openssl x509 -req -days 365 -in certificate.csr -signkey private.key -out certificate.crt

   # View certificate contents
   openssl x509 -in certificate.crt -text -noout
   ```

3. **File Encryption/Decryption Process**:

   Server side (has private.key):

   ```bash
   # Generate private key and extract public key
   openssl genrsa -out private.key 2048
   openssl rsa -in private.key -pubout -out pubkey.pem

   # Share pubkey.pem with clients
   ```

   Client side (has pubkey.pem):

   ```bash
   # Generate random symmetric key
   openssl rand -out key.bin 32

   # Encrypt symmetric key with public key
   openssl pkeyutl -encrypt -pubin -inkey pubkey.pem -in key.bin -out key.bin.enc

   # Encrypt actual file using symmetric key
   openssl enc -aes-256-cbc -pbkdf2 -salt -in file.txt -out file.encrypted -kfile key.bin
   ```

   Server side (decryption):

   ```bash
   # Decrypt the symmetric key using private key
   openssl pkeyutl -decrypt -inkey private.key -in key.bin.enc -out key.bin

   # Decrypt the file using symmetric key
   openssl enc -d -pbkdf2 -aes-256-cbc -in file.encrypted -out decrypted.txt -kfile key.bin
   ```

4. **Format Conversions**:

   ```bash
   # Convert PEM (Privacy Enhanced Mail) to DER (Distinguished Encoding Rules)
   openssl x509 -in cert.pem -outform der -out cert.der

   # Convert PEM to PKCS#12
   openssl pkcs12 -export -out certificate.pfx -inkey private.key -in certificate.crt
   ```

Best Practices:

- Always use strong key sizes (minimum 2048 bits for RSA)
- Keep private keys secure and encrypted
- For file encryption, use the hybrid approach (asymmetric + symmetric) as shown above
- Certificates (.crt) are needed only for SSL/TLS and identity verification
- For simple encryption/decryption, clients only need the public key (pubkey.pem)

### SSH Key Management

SSH (Secure Shell) key management is a critical aspect of system administration and secure remote access.

What are SSH Keys?

- SSH keys are cryptographic key pairs used for secure authentication
- Consists of a private key (kept secret) and public key (shared with servers)
- More secure than password authentication
- Can be used for automated, passwordless logins

Why Use SSH Keys?

- Stronger security than passwords
- Resistant to brute force attacks
- Convenient automated access
- Can be easily revoked if compromised
- Supports key rotation and access control

How SSH Keys Work:

1. Client generates key pair (public + private)
2. Public key is placed on remote server in ~/.ssh/authorized_keys
3. During connection:
   - Server sends challenge encrypted with public key
   - Only matching private key can decrypt challenge
   - Successful decryption proves identity

Best Practices:

- Use strong key types (ED25519 or RSA 4096-bit)
- Protect private keys with passphrases
- Store private keys securely
- Regularly audit and rotate keys
- Remove unused authorized_keys entries
- Back up private keys safely

#### Generate SSH Keys

```bash
# Generate RSA key
ssh-keygen -t rsa -b 4096

# Generate ED25519 key (more modern)
ssh-keygen -t ed25519
```

#### SSH Configuration

Create/edit `~/.ssh/config`:

```bash
Host myserver
    HostName server.example.com
    User username
    IdentityFile ~/.ssh/id_ed25519
    Port 22
```

#### Key-based Authentication

```bash
# Copy public key to remote server
ssh-copy-id user@remote-server

# Test connection
ssh user@remote-server
```

### OAuth Concepts

OAuth (Open Authorization) is an open standard for access delegation, commonly used to grant websites or applications limited access to a user's information without exposing passwords.

### How OAuth Works (Simplified):

1. **Resource Owner (User):** The person who owns the data or account.
2. **Client (App):** The app trying to access the user's data.
3. **Authorization Server:** Issues tokens after the user grants permission.
4. **Resource Server:** Hosts the data the client wants to access.

### Typical Flow (OAuth 2.0 Authorization Code Grant):

1. **User Initiates Login:**
   - The user tries to log in to a third-party app (Client).
2. **Client Requests Authorization:**
   - The client redirects the user to the Authorization Server with a request for access (like asking Google to log in).
3. **User Grants Permission:**
   - The user logs into the Authorization Server (e.g., Google) and grants permission.
4. **Authorization Code is Issued:**
   - The Authorization Server redirects the user back to the Client with an **Authorization Code**.
5. **Client Requests Access Token:**
   - The client sends the Authorization Code to the Authorization Server (via a secure back-channel) along with its own credentials (Client ID & Secret).
6. **Access Token is Issued:**
   - The Authorization Server validates the request and issues an **Access Token**.
7. **Client Accesses Resource Server:**
   - The client uses the Access Token to request data from the Resource Server (like getting user profile info).
8. **Resource Server Responds:**
   - If the token is valid, the Resource Server responds with the requested data.

### Tokens:

- **Access Token:** Short-lived, used to access resources.
- **Refresh Token:** Longer-lived, used to obtain a new access token without re-prompting the user.

### OAuth Scopes:

Defines what the client can access (e.g., read-only access to email).

### Why Use OAuth?

- **Security:** Users don't have to share passwords.
- **Granular Access:** Only specific data is shared.
- **Revocable:** Users can revoke access tokens anytime.

### Common OAuth Providers:

- Google
- Facebook
- GitHub
- Twitter

### Authentication Best Practices

1. **Password Security**:

   - Use strong passwords
   - Implement password policies
   - Use password managers
   - Enable two-factor authentication

2. **Key Security**:

   - Protect private keys
   - Use key passphrases
   - Rotate keys regularly
   - Implement key backup strategies

3. **Access Control**:
   - Principle of least privilege
   - Regular access reviews
   - Audit logging
   - Session management

### Secure File Transfer

#### Using SCP

```bash
# Copy file to remote server
scp file.txt user@remote-server:/path/to/destination

# Copy directory
scp -r directory/ user@remote-server:/path/to/destination
```

#### Using SFTP

```bash
# Connect to SFTP server
sftp user@remote-server

# Upload file
put local-file.txt

# Download file
get remote-file.txt
```

## System Automation

### Cron and At Scheduling

#### Cron Jobs

Cron is a time-based job scheduler in Unix-like operating systems. It enables users to schedule jobs (commands or scripts) to run automatically at specified intervals. The cron daemon checks the crontab files every minute to determine if any scheduled tasks need to be executed.

Key features of cron:

- Runs jobs automatically at specified times
- Supports multiple scheduling formats (minutes, hours, days, months, weekdays)
- Each user can have their own crontab
- System-wide cron jobs are stored in /etc/crontab
- Logs job execution for monitoring

Cron schedule format:

```
- - - - - command to execute
| | | | |
| | | | +-- Day of week (0-7) (Sunday=0 or 7)
| | | +---- Month (1-12)
| | +------ Day of month (1-31)
| +-------- Hour (0-23)
+---------- Minute (0-59)

```
Special characters:

- - Any value

```
Example: * * * * *         # Run every minute
```

, - Value list separator (e.g., 1,3,5)

```
Example: 0 2,4,6 * * *     # Run at 2AM, 4AM and 6AM every day
```

- - Range of values (e.g., 1-5)

```
Example: 0 9-17 * * 1-5    # Run every hour from 9AM-5PM on weekdays
```

/ - Step values (e.g., \*/2 means every 2 units)

```
Example: */10 * * * *      # Run every 10 minutes
```

Edit crontab:

```bash
# Open crontab editor
crontab -e
```

Example crontab entries:

```bash
# Run backup every day at 2 AM
0 2 * * * /path/to/backup.sh

# Run script every hour
0 * * * * /path/to/script.sh

# Run script every 30 minutes
*/30 * * * * /path/to/script.sh
```

#### At Command

The `at` command is a utility for scheduling one-time tasks to run at a specific time. Unlike cron which handles recurring tasks, `at` is designed for jobs that only need to run once.

Key features of the `at` command:

- Schedule tasks for future execution
- Accepts various time formats
- Preserves the current environment
- Sends job output via email
- Queues jobs if system is down at scheduled time

Time specification formats:

Schedule one-time tasks:

```bash
# Schedule a task
at 2:00 PM
at> /path/to/script.sh
at> Ctrl+D

# List scheduled tasks
atq

# Remove scheduled task
atrm job_number
```

### Systemd Services

Systemd is the default init system and service manager for most modern Linux distributions. It provides a standardized way to:

- Start, stop and manage system services
- Handle system startup and shutdown sequences
- Monitor and control system resources
- Manage dependencies between services
- Configure service behavior and recovery
- Track service logs and status

Key benefits of systemd services include:

- Parallel startup for faster boot times
- On-demand service activation
- Automatic service recovery
- Detailed logging and monitoring
- Standardized configuration
- Resource control and isolation
- Clean service termination

Systemd uses unit files (with .service extension) to define services. These files contain metadata about the service, execution parameters, dependencies, and installation information.

#### Create a Service

Create `/etc/systemd/system/myapp.service`:

```ini
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=myuser
WorkingDirectory=/path/to/app
ExecStart=/path/to/app/start.sh
Restart=always

```

#### Manage Services

```bash
# Start service
sudo systemctl start myapp

# Enable service at boot
sudo systemctl enable myapp

# Check status
sudo systemctl status myapp

# View logs
sudo journalctl -u myapp
```

### Backup Strategies

#### Local Backups

```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="/path/to/backups"
SOURCE_DIR="/path/to/source"
DATE=$(date +%Y%m%d)

# Create backup
tar -czf "$BACKUP_DIR/backup-$DATE.tar.gz" "$SOURCE_DIR"

# Remove old backups (keep last 7 days)
find "$BACKUP_DIR" -name "backup-*.tar.gz" -mtime +7 -delete
```

#### Remote Backups

```bash
# Sync to remote server
rsync -avz --delete /path/to/source/ user@remote-server:/path/to/backup/

# Encrypted backup
tar -czf - /path/to/source | gpg -c | ssh user@remote-server "cat > /path/to/backup/backup-$(date +%Y%m%d).tar.gz.gpg"
```

### Best Practices

1. **Security**:

   - Regular security updates
   - Firewall configuration
   - Intrusion detection
   - Security monitoring

2. **Automation**:

   - Document all automated tasks
   - Implement error handling
   - Set up monitoring
   - Regular testing

3. **Backup**:

   - Multiple backup locations
   - Regular backup testing
   - Version control
   - Disaster recovery plan

4. **Monitoring**:
   - System resource monitoring
   - Service health checks
   - Log monitoring
   - Alert configuration

## Additional Resources

1. [GPG Documentation](https://gnupg.org/documentation/)
2. [OpenSSL Documentation](https://www.openssl.org/docs/)
3. [SSH Documentation](https://www.openssh.com/manual.html)
4. [Systemd Documentation](https://www.freedesktop.org/wiki/Software/systemd/)
5. [Cron Documentation](https://www.gnu.org/software/mcron/manual/html_node/Crontab-file.html)
