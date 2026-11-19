# -*- coding: utf-8 -*-
"""
Practical 07: RSA Cryptosystem Implementation in Python
Student Name: Pravash Singh
Course: Cryptography (CSL0509) – B.Tech AIML V Semester
Faculty Name: Mr. Hirendra Singh Sengar
Academic Year: 2026-27
"""


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % phi + phi) % phi


def main():
    print("====== RSA Key Generation & Encryption ======")
    print("Student Name : Pravash Singh")
    print("Course       : Cryptography (CSL0509)")

    # Step 1: Choose two prime numbers
    p = 61
    q = 53

    # Step 2: Multiply p and q
    n = p * q

    # Step 3: Calculate phi = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Step 4: Choose public exponent
    e = 17

    # Step 5: Calculate private key d = e^-1 mod phi
    d = mod_inverse(e, phi)

    # Display RSA keys
    print("\nP =", p)
    print("Q =", q)
    print("N =", n)
    print("Phi =", phi)

    print(f"\nPublic Key  = ({e}, {n})")
    print(f"Private Key = ({d}, {n})")

    # Input message
    try:
        msg_input = input(f"\nEnter a numerical message (less than {n}, default 65): ").strip()
        message = int(msg_input) if msg_input else 65
    except (ValueError, EOFError):
        message = 65

    # Check message boundary
    if message >= n or message < 0:
        print(f"Message must be between 0 and {n - 1}")
        return

    # Encryption: C = M^e mod n
    ciphertext = pow(message, e, n)

    # Decryption: M = C^d mod n
    decrypted_message = pow(ciphertext, d, n)

    # Display results
    print("\n===== RSA Encryption Results =====")
    print("Original Message  :", message)
    print("Encrypted Message :", ciphertext)
    print("Decrypted Message :", decrypted_message)
    print("Verification      :", message == decrypted_message)


if __name__ == "__main__":
    main()
