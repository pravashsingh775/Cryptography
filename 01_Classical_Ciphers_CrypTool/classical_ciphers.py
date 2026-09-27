# -*- coding: utf-8 -*-
"""
Practical 01: Implementation of Caesar, Vigenère, and Rail Fence Ciphers
Course: Cryptography (CSL0509)
Faculty: Mr. Hirendra Singh Sengar
"""

def caesar_encrypt(plaintext: str, shift: int = 3) -> str:
    ciphertext = []
    print(f"\n[*] Caesar Encryption Process (Shift = {shift}):")
    print(f"    Formula: C = (P + {shift}) mod 26")
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            ciphertext.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            ciphertext.append(char)
    res = "".join(ciphertext)
    print(f"    Plaintext:  '{plaintext}'")
    print(f"    Ciphertext: '{res}'")
    return res

def caesar_decrypt(ciphertext: str, shift: int = 3) -> str:
    plaintext = []
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            plaintext.append(chr((ord(char) - base - shift + 26) % 26 + base))
        else:
            plaintext.append(char)
    res = "".join(plaintext)
    print(f"[*] Caesar Decrypted: '{res}'")
    return res

def vigenere_encrypt(plaintext: str, key: str = "KEY") -> str:
    ciphertext = []
    key_upper = key.upper()
    key_len = len(key_upper)
    print(f"\n[*] Vigenere Polyalphabetic Encryption (Key = '{key_upper}'):")
    print(f"    Formula: C_i = (P_i + K_i) mod 26")
    key_idx = 0
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            p_val = ord(char) - base
            k_val = ord(key_upper[key_idx % key_len]) - ord('A')
            ciphertext.append(chr((p_val + k_val) % 26 + base))
            key_idx += 1
        else:
            ciphertext.append(char)
    res = "".join(ciphertext)
    print(f"    Plaintext:  '{plaintext}'")
    print(f"    Ciphertext: '{res}'")
    return res

def vigenere_decrypt(ciphertext: str, key: str = "KEY") -> str:
    plaintext = []
    key_upper = key.upper()
    key_len = len(key_upper)
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            c_val = ord(char) - base
            k_val = ord(key_upper[key_idx % key_len]) - ord('A')
            plaintext.append(chr((c_val - k_val + 26) % 26 + base))
            key_idx += 1
        else:
            plaintext.append(char)
    res = "".join(plaintext)
    print(f"[*] Vigenere Decrypted: '{res}'")
    return res

def rail_fence_encrypt(plaintext: str, rails: int = 3) -> str:
    clean_text = "".join(plaintext.split())
    print(f"\n[*] Rail Fence Transposition Encryption (Rails/Depth = {rails}):")
    matrix = [["." for _ in range(len(clean_text))] for _ in range(rails)]
    row, direction = 0, 1
    for col, char in enumerate(clean_text):
        matrix[row][col] = char
        row += direction
        if row == 0 or row == rails - 1:
            direction = -direction
    for r in range(rails):
        print(f"    Rail {r+1}: " + " ".join(matrix[r]))
    ciphertext = [matrix[r][c] for r in range(rails) for c in range(len(clean_text)) if matrix[r][c] != "."]
    res = "".join(ciphertext)
    print(f"    Ciphertext: '{res}'")
    return res

def rail_fence_decrypt(ciphertext: str, rails: int = 3) -> str:
    matrix = [["." for _ in range(len(ciphertext))] for _ in range(rails)]
    row, direction = 0, 1
    for col in range(len(ciphertext)):
        matrix[row][col] = "*"
        row += direction
        if row == 0 or row == rails - 1:
            direction = -direction
    idx = 0
    for r in range(rails):
        for c in range(len(ciphertext)):
            if matrix[r][c] == "*" and idx < len(ciphertext):
                matrix[r][c] = ciphertext[idx]
                idx += 1
    plaintext = []
    row, direction = 0, 1
    for col in range(len(ciphertext)):
        plaintext.append(matrix[row][col])
        row += direction
        if row == 0 or row == rails - 1:
            direction = -direction
    res = "".join(plaintext)
    print(f"[*] Rail Fence Decrypted: '{res}'")
    return res

def main():
    print("=" * 75)
    print("      PRACTICAL 01: CAESAR, VIGENERE & RAIL FENCE CIPHER EXECUTION")
    print("=" * 75)
    
    # 1. Given plaintext in Problem Statement
    target_text = "HELLO WORLD"
    print(f"\n[+] Mandatory Problem Statement Plaintext: '{target_text}'")
    
    c1 = caesar_encrypt(target_text, shift=3)
    caesar_decrypt(c1, shift=3)
    
    v1 = vigenere_encrypt(target_text, key="KEY")
    vigenere_decrypt(v1, key="KEY")
    
    rf1 = rail_fence_encrypt(target_text, rails=3)
    rail_fence_decrypt(rf1, rails=3)
    
    # 2. Extended Practical Sample Text
    sample_text = "CRYPTOGRAPHY AND NETWORK SECURITY"
    print(f"\n\n[+] Extended Sample Plaintext: '{sample_text}'")
    
    c_cipher = caesar_encrypt(sample_text, shift=3)
    caesar_decrypt(c_cipher, shift=3)
    
    v_cipher = vigenere_encrypt(sample_text, key="SECRET")
    vigenere_decrypt(v_cipher, key="SECRET")
    
    rf_cipher = rail_fence_encrypt(sample_text, rails=3)
    rail_fence_decrypt(rf_cipher, rails=3)
    
    print("\n" + "=" * 75)
    print(" [OK] Practical 01 Completed Successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
    