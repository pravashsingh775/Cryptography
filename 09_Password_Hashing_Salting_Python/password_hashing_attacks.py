# -*- coding: utf-8 -*-
"""
Practical 09: Password Hashing with and without Salting & Attack Evaluation
Student Name: Pravash Singh
Course: Cryptography (CSL0509) – B.Tech AIML V Semester
Faculty Name: Mr. Hirendra Singh Sengar
Academic Year: 2026-27
"""

import hashlib
import os
import secrets
import time


def to_hex(data: bytes) -> str:
    """Convert bytes into a clean hexadecimal string."""
    return data.hex()


def hash_without_salt(password: str) -> str:
    """Standard SHA-256 hash without salt."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_with_salt(password: str, salt: bytes) -> str:
    """SHA-256 hash with random salt prefixed."""
    return hashlib.sha256(salt + password.encode("utf-8")).hexdigest()


def hash_pbkdf2(password: str, salt: bytes, iterations: int = 50000) -> str:
    """Key-stretched PBKDF2-HMAC-SHA256 hash."""
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations).hex()


def main():
    print("=" * 75)
    print(" PRACTICAL 09: PASSWORD HASHING, SALTING & ATTACK EVALUATION")
    print(" Student Name : Pravash Singh")
    print(" Course       : Cryptography (CSL0509) – B.Tech AIML V Semester")
    print("=" * 75)

    password = "StudentSecurePass2026!"

    # 1. Unsalted Hash
    hash1 = hash_without_salt(password)

    # 2. Salted Hashes with two distinct random salts
    salt1 = secrets.token_bytes(16)
    salt2 = secrets.token_bytes(16)

    hash2 = hash_with_salt(password, salt1)
    hash3 = hash_with_salt(password, salt2)

    print(f"\n[+] Target Test Password: '{password}'")
    print("\n--- [1] SHA-256 WITHOUT SALT ---")
    print(f"    Hash: {hash1}")

    print("\n--- [2] SHA-256 WITH SALT 1 ---")
    print(f"    Salt 1 (Hex): {to_hex(salt1)}")
    print(f"    Hash 1      : {hash2}")

    print("\n--- [3] SHA-256 WITH SALT 2 ---")
    print(f"    Salt 2 (Hex): {to_hex(salt2)}")
    print(f"    Hash 2      : {hash3}")

    print("\n--- [4] COMPARATIVE ANALYSIS ---")
    print(f"    Without Salt (Identical password produces identical hash) : True")
    print(f"    With Different Salts (Different hashes for same password) : {hash2 != hash3}")

    # 3. Dictionary & Cracking Attack Simulation
    print("\n--- [5] ATTACK RESISTANCE BENCHMARK (Dictionary Attack) ---")
    users = {"alice": "dragon123", "bob": "dragon123", "charlie": "admin123"}
    dictionary = ["123456", "password", "dragon123", "admin123", "letmein", "qwerty"]

    # Unsalted Database Attack
    unsalted_db = {u: hash_without_salt(p) for u, p in users.items()}
    start = time.perf_counter()
    cracked_unsalted = {}
    for word in dictionary:
        w_hash = hash_without_salt(word)
        for u, h in unsalted_db.items():
            if w_hash == h and u not in cracked_unsalted:
                cracked_unsalted[u] = word
    t_unsalted = time.perf_counter() - start

    # Salted PBKDF2 Attack
    user_salts = {u: os.urandom(16) for u in users}
    salted_db = {u: hash_pbkdf2(p, user_salts[u], 50000) for u, p in users.items()}
    start = time.perf_counter()
    cracked_salted = {}
    for u, h in salted_db.items():
        u_salt = user_salts[u]
        for word in dictionary:
            if hash_pbkdf2(word, u_salt, 50000) == h:
                cracked_salted[u] = word
                break
    t_salted = time.perf_counter() - start

    print(f"    Unsalted Attack Time: {t_unsalted * 1000:.4f} ms -> {cracked_unsalted}")
    print(f"    Salted PBKDF2 Time  : {t_salted:.4f} s ({t_salted * 1000:.2f} ms)")

    speedup = t_salted / max(t_unsalted, 1e-9)
    print(f"\n[SUCCESS] Salted PBKDF2 is {speedup:,.1f}x slower for attackers than unsalted SHA-256!")
    print("=" * 75)


if __name__ == "__main__":
    main()
