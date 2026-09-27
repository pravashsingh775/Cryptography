# -*- coding: utf-8 -*-
"""
Practical 09: Password Hashing with/without Salting & Attack Evaluation
Course: Cryptography (CSL0509)
Faculty: Mr. Hirendra Singh Sengar
"""

import hashlib
import os
import time

def hash_unsalted(pwd: str) -> str:
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()

def hash_salted(pwd: str, salt: bytes) -> str:
    return hashlib.sha256(salt + pwd.encode('utf-8')).hexdigest()

def hash_pbkdf2(pwd: str, salt: bytes, iterations: int = 100000) -> str:
    return hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), salt, iterations).hex()

def main():
    print("=" * 75)
    print(" PRACTICAL 09: PASSWORD HASHING, SALTING & ATTACK EVALUATION")
    print("=" * 75)
    
    users = {
        "alice": "dragon123",
        "bob": "dragon123",
        "charlie": "admin123"
    }
    
    unsalted_db = {u: hash_unsalted(p) for u, p in users.items()}
    
    salts = {u: os.urandom(16) for u in users}
    salted_db = {u: hash_pbkdf2(p, salts[u], 50000) for u, p in users.items()}
    
    print("\n[+] Unsalted (Notice Alice and Bob have SAME hash):")
    for u, h in unsalted_db.items():
        print(f"    {u:<10}: {h[:20]}...")
        
    dictionary = ["123456", "password", "dragon123", "admin123", "letmein", "qwerty"]
    
    # Attack Unsalted
    start = time.perf_counter()
    cracked_unsalted = {}
    for word in dictionary:
        h = hash_unsalted(word)
        for u, target_h in unsalted_db.items():
            if h == target_h and u not in cracked_unsalted:
                cracked_unsalted[u] = word
    t_unsalted = time.perf_counter() - start
    
    # Attack Salted
    start = time.perf_counter()
    cracked_salted = {}
    for u, target_h in salted_db.items():
        user_salt = salts[u]
        for word in dictionary:
            h = hash_pbkdf2(word, user_salt, 50000)
            if h == target_h:
                cracked_salted[u] = word
                break
    t_salted = time.perf_counter() - start
    
    print(f"\n[+] Unsalted Attack: Cracked in {t_unsalted*1000:.4f} ms -> {cracked_unsalted}")
    print(f"[+] Salted Attack:   Cracked in {t_salted:.4f} s ({t_salted*1000:.2f} ms)")
    
    speedup = t_salted / max(t_unsalted, 1e-9)
    print(f"\n[SUCCESS] Salted PBKDF2 is {speedup:,.1f}x slower for attacker!")
    print("=" * 75)

if __name__ == "__main__":
    main()
