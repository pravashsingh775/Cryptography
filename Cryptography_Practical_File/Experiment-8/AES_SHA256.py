# -*- coding: utf-8 -*-
"""
Practical 08: AES Encryption & SHA-256 Hashing Application in Python
Student Name: Pravash Singh
Course: Cryptography (CSL0509) – B.Tech AIML V Semester
Faculty Name: Mr. Hirendra Singh Sengar
Academic Year: 2026-27
"""

import hashlib
import os
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def to_hex(data: bytes) -> str:
    """Convert byte array into hexadecimal string."""
    return data.hex()


def main():
    print("=" * 55)
    print("       AES-GCM ENCRYPTION & SHA-256 HASHING")
    print("Student Name : Pravash Singh")
    print("Course       : Cryptography (CSL0509)")
    print("=" * 55)

    try:
        raw_input = input("\nEnter message (default: 'Hello, Cryptography!'): ").strip()
        message = raw_input if raw_input else "Hello, Cryptography!"
    except EOFError:
        message = "Hello, Cryptography!"

    data = message.encode("utf-8")

    # Generate AES-128 key and random 12-byte IV (Standard for GCM)
    key = AESGCM.generate_key(bit_length=128)
    iv = secrets.token_bytes(12)

    # AES Encryption using GCM
    aes = AESGCM(key)
    encrypted = aes.encrypt(iv, data, None)

    print("\n--- AES ENCRYPTION (GCM Mode) ---")
    print("Generated 128-bit Key :", to_hex(key))
    print("Random 96-bit IV      :", to_hex(iv))
    print("Encrypted Message     :", to_hex(encrypted))

    # AES Decryption
    decrypted = aes.decrypt(iv, encrypted, None)
    decrypted_str = decrypted.decode("utf-8")

    print("\n--- AES DECRYPTION ---")
    print("Decrypted Message     :", decrypted_str)

    # SHA-256 Hashing
    hash_bytes = hashlib.sha256(data).digest()

    print("\n--- SHA-256 HASH ---")
    print("Hash Value (Hex)      :", to_hex(hash_bytes))

    # Verify recovered message
    is_valid = (message == decrypted_str)
    print(f"\nMessage Verification  : {is_valid}")
    if is_valid:
        print("[SUCCESS] Data integrity and confidentiality verified!")


if __name__ == "__main__":
    main()
