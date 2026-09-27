#!/bin/bash
# Practical 14: SSH Keypair Generation & Passwordless Authentication
echo "=== Practical 14: SSH Keypair Authentication Setup ==="

KEY_FILE="$HOME/.ssh/id_rsa_cryptolab"

# 1. Generate 4096-bit RSA Keypair
echo "[+] Generating 4096-bit RSA SSH Keypair..."
ssh-keygen -t rsa -b 4096 -C "student@crypto.lab" -f "$KEY_FILE" -N ""

# 2. Set strict file permissions
echo "[+] Setting strict permissions..."
chmod 700 "$HOME/.ssh"
chmod 600 "$KEY_FILE"
chmod 644 "$KEY_FILE.pub"

# 3. Display Public Key to be deployed
echo "[+] Generated Public Key (deploy to ~/.ssh/authorized_keys on server):"
cat "$KEY_FILE.pub"

echo "\n[+] Use: ssh-copy-id -i $KEY_FILE.pub user@<remote_host>"
