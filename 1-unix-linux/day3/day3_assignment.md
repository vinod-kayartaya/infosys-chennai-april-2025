# Day 3: Security and Automation Assignments

## Assignment 1: File Encryption with OpenSSL

Create a shell script called `encrypt_file.sh` that:

1. Takes a file path as input
2. Encrypts the file using AES-256-CBC with PBKDF2
3. Saves the encrypted file with a `.enc` extension
4. Includes error handling for missing files
5. Prompts for a password securely

Example usage:

```bash
./encrypt_file.sh secret.txt
```

## Assignment 2: File Decryption with OpenSSL

Create a shell script called `decrypt_file.sh` that:

1. Takes an encrypted file path as input
2. Decrypts the file using the same encryption method
3. Saves the decrypted file with the original name
4. Includes error handling for incorrect passwords
5. Prompts for the decryption password securely

Example usage:

```bash
./decrypt_file.sh secret.txt.enc
```

## Assignment 3: GPG Key Management

Create a shell script called `setup_gpg.sh` that:

1. Generates a new GPG key pair
2. Exports the public key to a file
3. Exports the private key to a secure file
4. Sets appropriate permissions on the key files
5. Displays the key fingerprint

Example usage:

```bash
./setup_gpg.sh "Your Name <your.email@example.com>"
```

## Assignment 4: SSH Key Setup

Create a shell script called `setup_ssh.sh` that:

1. Generates an ED25519 SSH key pair
2. Creates a proper SSH config file
3. Sets up key-based authentication for a remote server
4. Tests the connection
5. Includes error handling for connection failures

Example usage:

```bash
./setup_ssh.sh user@remote-server
```

## Assignment 5: Automated Backup System

Create a shell script called `backup_system.sh` that:

1. Takes source and destination directories as input
2. Creates timestamped backups
3. Implements rotation (keeps last 7 days of backups)
4. Uses encryption for sensitive data
5. Logs backup operations
6. Can be scheduled via cron

Example usage:

```bash
./backup_system.sh /path/to/source /path/to/backup
```

## Assignment 6: Secure File Transfer

Create a shell script called `secure_transfer.sh` that:

1. Takes source file, destination, and remote server as input
2. Implements both SCP and SFTP transfer methods
3. Verifies file integrity after transfer
4. Includes progress reporting
5. Handles connection errors gracefully

Example usage:

```bash
./secure_transfer.sh local_file.txt user@remote-server:/path/to/destination
```

## Submission Guidelines

1. Each script should:

   - Include proper error handling
   - Have clear usage instructions
   - Be well-documented with comments
   - Follow shell scripting best practices
   - Include input validation

2. Create a README.md file that:

   - Explains how to use each script
   - Lists dependencies and requirements
   - Provides example usage
   - Documents any assumptions or limitations

3. Testing:
   - Test each script with various inputs
   - Verify error handling works as expected
   - Ensure security measures are properly implemented
   - Document test cases and results

## Resources

- [OpenSSL Documentation](https://www.openssl.org/docs/)
- [GPG Documentation](https://gnupg.org/documentation/)
- [SSH Documentation](https://www.openssh.com/manual.html)
- [Shell Scripting Best Practices](https://google.github.io/styleguide/shellguide.html)
