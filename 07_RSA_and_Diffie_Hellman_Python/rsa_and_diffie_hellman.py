# -*- coding: utf-8 -*-
"""
Practical 07: RSA & Diffie-Hellman Key Exchange Implementation in Python
Student Name: Pravash Singh
Course: Cryptography (CSL0509) – B.Tech AIML V Semester
Faculty Name: Mr. Hirendra Singh Sengar
Academic Year: 2026-27
"""

import random


def extended_gcd(a: int, b: int):
    """Extended Euclidean Algorithm returning (gcd, x, y) such that a*x + b*y = gcd."""
    if a == 0:
        return b, 0, 1
    g, y, x = extended_gcd(b % a, a)
    return g, x - (b // a) * y, y


def mod_inverse(e: int, phi: int) -> int:
    """Compute modular multiplicative inverse d = e^-1 mod phi."""
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % phi + phi) % phi


def run_rsa_demo(message: int = 65):
    """RSA Key Generation, Encryption and Decryption."""
    print("\n" + "=" * 60)
    print(" [A] RSA PUBLIC-KEY CRYPTOGRAPHY (PRIME ROOTS)")
    print("=" * 60)

    # Prime selection
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    d = mod_inverse(e, phi)

    print(f"Prime p: {p}, Prime q: {q}")
    print(f"Modulus n (p*q): {n}")
    print(f"Euler's Totient phi(n): {phi}")
    print(f"Public Key  (e, n): ({e}, {n})")
    print(f"Private Key (d, n): ({d}, {n})")

    # Encryption C = M^e mod n
    ciphertext = pow(message, e, n)

    # Decryption M = C^d mod n
    decrypted = pow(ciphertext, d, n)

    print(f"\nPlaintext Message  : {message}")
    print(f"Encrypted Ciphertext: {ciphertext}")
    print(f"Decrypted Message   : {decrypted}")
    print(f"Verification Check  : {message == decrypted} [100% Match]")
    return message == decrypted


def run_diffie_hellman_demo(alice_private: int = 6, bob_private: int = 15):
    """Diffie-Hellman Key Agreement Protocol."""
    print("\n" + "=" * 60)
    print(" [B] DIFFIE-HELLMAN KEY EXCHANGE PROTOCOL")
    print("=" * 60)

    # Public parameters
    p = 23
    g = 5
    print(f"Public Prime (p)     : {p}")
    print(f"Public Generator (g) : {g}")

    # Private keys
    a = alice_private
    b = bob_private
    print(f"\nAlice Private Key (a): {a}")
    print(f"Bob Private Key (b)  : {b}")

    # Calculate public keys
    A = pow(g, a, p)
    B = pow(g, b, p)
    print(f"Alice Public Key (A = g^a mod p): {A}")
    print(f"Bob Public Key   (B = g^b mod p): {B}")

    # Calculate shared secret
    secret_alice = pow(B, a, p)
    secret_bob = pow(A, b, p)

    print(f"\nAlice Computed Shared Secret (B^a mod p): {secret_alice}")
    print(f"Bob Computed Shared Secret   (A^b mod p): {secret_bob}")

    match = (secret_alice == secret_bob)
    print(f"Shared Secret Agreement Verified: {match} (Secret = {secret_alice})")
    return match


def main():
    print("=" * 75)
    print(" PRACTICAL 07: RSA & DIFFIE-HELLMAN ALGORITHMS IN PYTHON")
    print(" Student Name : Pravash Singh")
    print(" Course       : Cryptography (CSL0509) – B.Tech AIML V Semester")
    print("=" * 75)

    # Execute Both Core Algorithms
    run_rsa_demo(message=65)
    run_diffie_hellman_demo(alice_private=6, bob_private=15)

    print("\n" + "=" * 75)
    print(" [OK] Practical 07 Completed Successfully!")
    print("=" * 75)


if __name__ == "__main__":
    main()
