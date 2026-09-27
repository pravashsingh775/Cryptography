#!/bin/bash
# Practical 05: OpenSSL SHA-256 Hashing & Digital Signatures
echo "=== Practical 05: OpenSSL Digital Signatures ==="

# 1. Generate Signing Keypair
openssl genpkey -algorithm RSA -out sender_private.pem -pkeyopt rsa_keygen_bits:2048
openssl pkey -in sender_private.pem -pubout -out sender_public.pem

# 2. Create Document
echo "AUTHORIZE WIRE TRANSFER: AMOUNT=\$50,000 TO ACCOUNT: 987654321" > transaction.txt

# 3. SHA-256 Hash
openssl dgst -sha256 transaction.txt

# 4. Digital Signature
openssl dgst -sha256 -sign sender_private.pem -out signature.bin transaction.txt

# 5. Verify Authentic Signature
openssl dgst -sha256 -verify sender_public.pem -signature signature.bin transaction.txt

# 6. Tamper Test
echo "AUTHORIZE WIRE TRANSFER: AMOUNT=\$99,999 TO ACCOUNT: 987654321" > transaction.txt
openssl dgst -sha256 -verify sender_public.pem -signature signature.bin transaction.txt
