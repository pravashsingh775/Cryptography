#!/bin/bash
# Practical 04: RSA Public & Private Keypair Generation & File Encryption
echo "=== Practical 04: OpenSSL RSA File Crypto ==="

# 1. Generate Private Key
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

# 2. Extract Public Key
openssl pkey -in private_key.pem -pubout -out public_key.pem

# 3. Create Plaintext
echo "Confidential Payload: Engineering Cryptography OpenSSL Practical Verification." > plaintext.txt

# 4. Encrypt with OAEP
openssl pkeyutl -encrypt -pubin -inkey public_key.pem -in plaintext.txt -out ciphertext.bin -pkeyopt rsa_padding_mode:oaep

# 5. Decrypt
openssl pkeyutl -decrypt -inkey private_key.pem -in ciphertext.bin -out decrypted.txt -pkeyopt rsa_padding_mode:oaep

# 6. Verify
diff -s plaintext.txt decrypted.txt
