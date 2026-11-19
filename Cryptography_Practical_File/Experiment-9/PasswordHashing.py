# -*- coding: utf-8 -*-
"""
Practical 09: Password Hashing With and Without Salting in Python
Student Name: Pravash Singh
Course: Cryptography (CSL0509) – B.Tech AIML V Semester
Faculty Name: Mr. Hirendra Singh Sengar
Academic Year: 2026-27
"""

import hashlib
import secrets


def to_hex(data: bytes) -> str:
    """Convert byte array into hexadecimal string."""
    return data.hex()


def hash_without_salt(password: str) -> str:
    """SHA-256 hashing without salt."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_with_salt(password: str, salt: bytes) -> str:
    """SHA-256 hashing with random salt."""
    hasher = hashlib.sha256()
    hasher.update(salt)
    hasher.update(password.encode("utf-8"))
    return hasher.hexdigest()


def main():
    print("=" * 55)
    print("      PASSWORD HASHING WITH & WITHOUT SALTING")
    print("Student Name : Pravash Singh")
    print("Course       : Cryptography (CSL0509)")
    print("=" * 55)

    try:
        pwd_input = input("\nEnter password (default: 'StudentSecurePass2026!'): ").strip()
        password = pwd_input if pwd_input else "StudentSecurePass2026!"
    except EOFError:
        password = "StudentSecurePass2026!"

    # Hash without salt
    hash1 = hash_without_salt(password)

    # Generate random 16-byte salts
    salt1 = secrets.token_bytes(16)
    salt2 = secrets.token_bytes(16)

    # Hash with different salts
    hash2 = hash_with_salt(password, salt1)
    hash3 = hash_with_salt(password, salt2)

    print("\n--- Password Hashing Results ---")
    print("Password :", password)

    print("\nHash Without Salt:")
    print(hash1)

    print("\nSalt 1:")
    print(to_hex(salt1))
    print("Hash With Salt 1:")
    print(hash2)

    print("\nSalt 2:")
    print(to_hex(salt2))
    print("Hash With Salt 2:")
    print(hash3)

    print("\n--- Comparison & Analysis ---")
    print(f"Without Salt Hashes are identical for same password : True")
    print(f"With Different Salts, Hashes are different           : {hash2 != hash3}")

    print("\nConclusion:")
    print("1. Same password produces the exact same unsalted hash (vulnerable to Rainbow Tables).")
    print("2. Different random salts ensure unique hashes for identical passwords.")
    print("3. Salting prevents dictionary and precomputed rainbow table attacks.")


if __name__ == "__main__":
    main()
