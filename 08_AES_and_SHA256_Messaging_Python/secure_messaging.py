# -*- coding: utf-8 -*-
"""
Practical 08: Secure Text Messaging Application (AES-GCM/CBC & SHA-256)
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
    """Convert bytes into a clean hexadecimal string."""
    return data.hex()


def main():
    print("=" * 75)
    print(" PRACTICAL 08: AES ENCRYPTION & SHA-256 SECURE MESSAGING")
    print(" Student Name : Pravash Singh")
    print(" Course       : Cryptography (CSL0509) – B.Tech AIML V Semester")
    print("=" * 75)

    message = "Mission Directive: Transfer operative to safehouse Alpha at 0200 hrs."
    data = message.encode("utf-8")
    print(f"\n[+] Input Plaintext Message:\n    '{message}'")

    # Step 1: Generate 128-bit key and random 96-bit IV
    key = AESGCM.generate_key(bit_length=128)
    iv = secrets.token_bytes(12)

    # Step 2: AES-GCM Authenticated Encryption
    aes = AESGCM(key)
    ciphertext = aes.encrypt(iv, data, None)

    print("\n--- [1] AES ENCRYPTION (GCM Authenticated Mode) ---")
    print(f"    AES Key (128-bit) : {to_hex(key)}")
    print(f"    Random IV (96-bit): {to_hex(iv)}")
    print(f"    Ciphertext + Tag  : {to_hex(ciphertext)}")

    # Step 3: Decryption
    decrypted = aes.decrypt(iv, ciphertext, None)
    recovered_text = decrypted.decode("utf-8")

    print("\n--- [2] AES DECRYPTION ---")
    print(f"    Decrypted Message : '{recovered_text}'")

    # Step 4: SHA-256 Hash Digest
    hash_value = hashlib.sha256(data).hexdigest()

    print("\n--- [3] SHA-256 MESSAGE INTEGRITY HASH ---")
    print(f"    SHA-256 Digest    : {hash_value}")

    # Step 5: Verification & Tamper Resistance Test
    print("\n--- [4] AUTHENTICATION & TAMPER TEST ---")
    is_valid = (message == recovered_text)
    print(f"    Original vs Decrypted Match : {is_valid}")

    # Tamper simulation: alter 1 byte in ciphertext
    tampered_ct = bytearray(ciphertext)
    tampered_ct[0] ^= 0xFF
    try:
        aes.decrypt(iv, bytes(tampered_ct), None)
        print("    Tamper Test Result: FAILED (Tamper was not detected)")
    except Exception:
        print("    Tamper Test Result: SUCCESS (Tampered ciphertext rejected by GCM tag!)")

    print("\n" + "=" * 75)
    print(" [OK] Practical 08 Completed Successfully!")
    print("=" * 75)


if __name__ == "__main__":
    main()
