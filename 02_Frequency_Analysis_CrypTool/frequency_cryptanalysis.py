# -*- coding: utf-8 -*-
"""
Practical 02: Frequency Analysis on Classical Cipher Texts
Course: Cryptography (CSL0509)
Faculty: Mr. Hirendra Singh Sengar
"""

import collections
import string

ENGLISH_FREQ = {
    'A': 0.0817, 'B': 0.0150, 'C': 0.0278, 'D': 0.0425, 'E': 0.1270,
    'F': 0.0223, 'G': 0.0202, 'H': 0.0609, 'I': 0.0697, 'J': 0.0015,
    'K': 0.0077, 'L': 0.0403, 'M': 0.0241, 'N': 0.0675, 'O': 0.0751,
    'P': 0.0193, 'Q': 0.0010, 'R': 0.0599, 'S': 0.0633, 'T': 0.0906,
    'U': 0.0276, 'V': 0.0098, 'W': 0.0236, 'X': 0.0015, 'Y': 0.0197,
    'Z': 0.0007
}

def calculate_ioc(text: str) -> float:
    clean = [c.upper() for c in text if c.isalpha()]
    n = len(clean)
    if n <= 1:
        return 0.0
    counts = collections.Counter(clean)
    numerator = sum(count * (count - 1) for count in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator

def plot_histogram(text: str, label: str, top_n: int = 8):
    clean = [c.upper() for c in text if c.isalpha()]
    n = len(clean)
    counts = collections.Counter(clean)
    print(f"\n--- {label} (Top {top_n} Letters) ---")
    for char, count in counts.most_common(top_n):
        pct = (count / n) * 100
        bar = "#" * int(pct * 2)
        print(f"  {char}: {pct:5.2f}% | {bar}")

def auto_crack_caesar(ciphertext: str):
    clean = [c.upper() for c in ciphertext if c.isalpha()]
    n = len(clean)
    best_shift = 0
    min_chi2 = float('inf')
    
    for shift in range(26):
        decrypted = [chr((ord(c) - 65 - shift + 26) % 26 + 65) for c in clean]
        counts = collections.Counter(decrypted)
        chi2 = 0.0
        for char, expected_prob in ENGLISH_FREQ.items():
            observed = counts.get(char, 0)
            expected = n * expected_prob
            chi2 += ((observed - expected) ** 2) / expected
        
        if chi2 < min_chi2:
            min_chi2 = chi2
            best_shift = shift
            
    return best_shift, min_chi2

def main():
    print("=" * 75)
    print(" PRACTICAL 02: FREQUENCY ANALYSIS & AUTOMATED CRYPTANALYSIS")
    print("=" * 75)
    
    plaintext = (
        "Cryptography is the practice and study of techniques for secure communication in the "
        "presence of adversarial third parties. Modern cryptography heavily relies on mathematical "
        "theory and computer science practice."
    )
    
    print(f"\n[+] Analyzing Natural English Sample (N = {len([c for c in plaintext if c.isalpha()])} characters)...")
    ioc_plain = calculate_ioc(plaintext)
    print(f"    Plaintext IoC: {ioc_plain:.4f} (Characteristic of English ~0.0667)")
    plot_histogram(plaintext, "English Plaintext Distribution")
    
    # Caesar Encryption with Shift 11
    shift = 11
    caesar_ct = "".join(
        chr((ord(c) - 65 + shift) % 26 + 65) if c.isupper() else
        chr((ord(c) - 97 + shift) % 26 + 97) if c.islower() else c
        for c in plaintext
    )
    ioc_caesar = calculate_ioc(caesar_ct)
    print(f"\n[+] Encrypted with Caesar (Secret Shift = {shift}):")
    print(f"    Caesar Ciphertext IoC: {ioc_caesar:.4f} (Identical roughness preserved!)")
    plot_histogram(caesar_ct, "Caesar Ciphertext Distribution")
    
    recovered_shift, chi2 = auto_crack_caesar(caesar_ct)
    print(f"\n[*] Auto-Cracking Caesar via Chi-Square: Recovered Shift = {recovered_shift} (Chi2 = {chi2:.2f})")
    recovered_pt = "".join(
        chr((ord(c) - 65 - recovered_shift + 26) % 26 + 65) if c.isupper() else
        chr((ord(c) - 97 - recovered_shift + 26) % 26 + 97) if c.islower() else c
        for c in caesar_ct
    )
    print(f"    Decrypted: '{recovered_pt[:65]}...'")
    
    # Vigenere Encryption
    key = "CIPHER"
    key_upper = key.upper()
    vigenere_ct = []
    k_idx = 0
    for c in plaintext:
        if c.isalpha():
            base = 65 if c.isupper() else 97
            k_val = ord(key_upper[k_idx % len(key_upper)]) - 65
            vigenere_ct.append(chr((ord(c) - base + k_val) % 26 + base))
            k_idx += 1
        else:
            vigenere_ct.append(c)
    vigenere_str = "".join(vigenere_ct)
    ioc_vig = calculate_ioc(vigenere_str)
    print(f"\n[+] Vigenere Ciphertext (Key='{key}'):")
    print(f"    Vigenere IoC: {ioc_vig:.4f} (Flattened polyalphabetic distribution!)")
    plot_histogram(vigenere_str, "Vigenere Smoothed Distribution")
    
    print("\n" + "=" * 75)
    print(" [OK] Practical 02 Completed Successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
