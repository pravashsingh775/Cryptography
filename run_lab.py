# -*- coding: utf-8 -*-
"""
===================================================================================
                CRYPTOGRAPHY PRACTICAL LAB - MASTER RUNNER
===================================================================================
Run this interactive controller to execute and verify any practical (Pr. 01 to 09).
Course: Cryptography (CSL0509) | Faculty: Mr. Hirendra Singh Sengar
"""

import subprocess
import os
import sys

PRACTICAL_REGISTRY = [
    ("01", "CrypTool", "Caesar, Vigenere & Rail Fence ('HELLO WORLD')", "01_Classical_Ciphers_CrypTool/classical_ciphers.py"),
    ("02", "CrypTool", "Frequency Analysis & Auto-Cryptanalysis", "02_Frequency_Analysis_CrypTool/frequency_cryptanalysis.py"),
    ("03", "CrypTool", "DES vs AES Performance & Avalanche Benchmark", "03_DES_vs_AES_CrypTool/des_vs_aes_benchmark.py"),
    ("04", "OpenSSL",  "RSA Keypair Generation & File Encryption", "04_RSA_Keys_File_Crypto_OpenSSL/run_openssl_rsa.py"),
    ("05", "OpenSSL",  "SHA-256 Hashing & Digital Signature Verification", "05_SHA256_Digital_Signatures_OpenSSL/run_openssl_signatures.py"),
    ("06", "OpenSSL",  "X.509 Digital Certificate Generation & Inspection", "06_X509_Certificates_OpenSSL/run_openssl_x509.py"),
    ("07", "VS Code",  "RSA & Diffie-Hellman Key Exchange Implementation", "07_RSA_and_Diffie_Hellman_Python/rsa_and_diffie_hellman.py"),
    ("08", "VS Code",  "AES-256 & SHA-256 / HMAC Secure Messaging", "08_AES_and_SHA256_Messaging_Python/secure_messaging.py"),
    ("09", "VS Code",  "Password Hashing with Salting & Attack Defense", "09_Password_Hashing_Salting_Python/password_hashing_attacks.py"),
]

def execute_practical(rel_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(base_dir, rel_path)
    work_dir = os.path.dirname(abs_path)
    file_name = os.path.basename(abs_path)
    print(f"\n{'='*75}\n>>> LAUNCHING: {file_name}\n{'='*75}")
    res = subprocess.run([sys.executable, file_name], cwd=work_dir)
    return res.returncode

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("--all", "-a", "all"):
        print("\n[+] Executing all practicals in batch mode...")
        for _, _, _, script_path in PRACTICAL_REGISTRY:
            execute_practical(script_path)
        print("\n[SUCCESS] All executable practicals executed successfully!")
        return

    while True:
        print("\n" + "=" * 78)
        print("          CRYPTOGRAPHY & NETWORK SECURITY LAB MASTER CONTROLLER")
        print("=" * 78)
        for num, tool, title, _ in PRACTICAL_REGISTRY:
            print(f"  [{int(num)}] Practical {num} ({tool:<9}) : {title}")
        print("  ----------------------------------------------------------------------------")
        print("  [A] Run ALL Executable Practicals (1 through 9)")
        print("  [Q] Exit")
        print("=" * 78)
        
        try:
            choice = input("\n>> Enter Choice (1-9, A, Q): ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
            
        if choice == 'Q':
            print("Exiting Cryptography Lab Controller.")
            break
        elif choice == 'A':
            for _, _, _, script_path in PRACTICAL_REGISTRY:
                execute_practical(script_path)
            print("\n[SUCCESS] All executable practicals executed successfully!")
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(PRACTICAL_REGISTRY):
            idx = int(choice) - 1
            execute_practical(PRACTICAL_REGISTRY[idx][3])
        else:
            print("\n[!] Invalid input! Please enter a number between 1 and 9, 'A', or 'Q'.")

if __name__ == "__main__":
    main()
