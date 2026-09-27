# -*- coding: utf-8 -*-
"""
Practical 07: Pure Python Implementation of RSA and Diffie-Hellman
Course: Cryptography (CSL0509)
Faculty: Mr. Hirendra Singh Sengar
"""

import random

def is_prime(n: int, k: int = 5) -> bool:
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits: int = 14) -> int:
    while True:
        p = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(p):
            return p

def egcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def mod_inv(e: int, phi: int) -> int:
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % phi + phi) % phi

def generate_rsa_keys():
    p = generate_prime(14)
    q = generate_prime(14)
    while q == p:
        q = generate_prime(14)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if egcd(e, phi)[0] != 1:
        e = 3
    d = mod_inv(e, phi)
    return (e, n), (d, n), p, q, phi

def rsa_encrypt(msg: str, pub_key) -> list:
    e, n = pub_key
    return [pow(ord(char), e, n) for char in msg]

def rsa_decrypt(cipher_list: list, priv_key) -> str:
    d, n = priv_key
    return "".join(chr(pow(char_code, d, n)) for char_code in cipher_list)

def diffie_hellman_demo():
    p = 7919
    g = 7
    a = random.randint(100, 1000)
    b = random.randint(100, 1000)
    
    A = pow(g, a, p)
    B = pow(g, b, p)
    
    s_alice = pow(B, a, p)
    s_bob = pow(A, b, p)
    
    return p, g, a, b, A, B, s_alice, s_bob

def main():
    print("=" * 75)
    print(" PRACTICAL 07: RSA & DIFFIE-HELLMAN KEY EXCHANGE")
    print("=" * 75)
    
    # 1. RSA
    pub, priv, p, q, phi = generate_rsa_keys()
    print(f"[+] RSA Key Generation:")
    print(f"    p: {p}, q: {q} | Modulus n: {pub[1]}")
    print(f"    Public Key (e, n):  {pub}")
    print(f"    Private Key (d, n): {priv}")
    
    msg = "CONFIDENTIAL_KEY_2026"
    ct = rsa_encrypt(msg, pub)
    dec = rsa_decrypt(ct, priv)
    
    print(f"\n    Plaintext:  '{msg}'")
    print(f"    Ciphertext: {ct[:6]}...")
    print(f"    Decrypted:  '{dec}' (Verified: {msg == dec})")
    
    # 2. Diffie-Hellman
    p_dh, g_dh, a, b, A, B, s_alice, s_bob = diffie_hellman_demo()
    print(f"\n[+] Diffie-Hellman Shared Secret Agreement:")
    print(f"    Parameters: Prime p = {p_dh}, Generator g = {g_dh}")
    print(f"    Alice Public A = {A} | Bob Public B = {B}")
    print(f"    Alice Secret: {s_alice} | Bob Secret: {s_bob} | Match: {s_alice == s_bob}")
    
    print("\n" + "=" * 75)
    print(" [OK] Practical 07 Completed Successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
