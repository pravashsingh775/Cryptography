# -*- coding: utf-8 -*-
"""
Practical 07: Diffie-Hellman Key Exchange Implementation in Python
Student Name: Pravash Singh
Course: Cryptography (CSL0509) – B.Tech AIML V Semester
Faculty Name: Mr. Hirendra Singh Sengar
Academic Year: 2026-27
"""


def main():
    print("==== Diffie-Hellman Key Exchange ====")
    print("Student Name : Pravash Singh")
    print("Course       : Cryptography (CSL0509)")

    p = 23
    g = 5

    print(f"\nPublic Prime (p) : {p}")
    print(f"Public Generator (g) : {g}")

    # Private keys
    try:
        a_input = input("\nEnter Alice's private key (default 6): ").strip()
        a = int(a_input) if a_input else 6

        b_input = input("Enter Bob's private key (default 15): ").strip()
        b = int(b_input) if b_input else 15
    except (ValueError, EOFError):
        print("Using standard values: Alice=6, Bob=15")
        a, b = 6, 15

    # Alice calculates public key
    A = pow(g, a, p)

    # Bob calculates public key
    B = pow(g, b, p)

    print(f"\nAlice's public key : {A}")
    print(f"Bob's public key : {B}")

    # Shared secret calculated by Alice
    secret_alice = pow(B, a, p)

    # Shared secret calculated by Bob
    secret_bob = pow(A, b, p)

    print("\n==== Shared Secret ====")
    print(f"Alice's shared secret : {secret_alice}")
    print(f"Bob's shared secret : {secret_bob}")

    # Verify shared secret
    if secret_alice == secret_bob:
        print("\nKey Exchange Successful!")
        print("Both Alice and Bob have the same secret key.")
    else:
        print("\nKey Exchange Failed!")


#           DIFFIE-HELLMAN KEY EXCHANGE
#
#                 Public Values
#                p = 23, g = 5
#                      |
#           +----------+----------+
#           |                     |
#        ALICE                   BOB
#           |                     |
#     Private Key = 6       Private Key = 15
#           |                     |
#           v                     v
#     A = 5^6 mod 23        B = 5^15 mod 23
#           |                     |
#           v                     v
#      Public Key = 8        Public Key = 19
#           |                     |
#           |------ Exchange -----|
#           |                     |
#           v                     v
#    Receive B = 19          Receive A = 8
#           |                     |
#           v                     v
#    19^6 mod 23             8^15 mod 23
#           |                     |
#           v                     v
#       Secret = 2             Secret = 2
#           |                     |
#           +----------+----------+
#                      |
#                 SAME SECRET
#                      |
#            Key Exchange Successful

if __name__ == "__main__":
    main()
