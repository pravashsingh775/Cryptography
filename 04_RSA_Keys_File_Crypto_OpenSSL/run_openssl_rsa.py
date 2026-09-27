# -*- coding: utf-8 -*-
"""
Practical 04: OpenSSL RSA Keypair Generation & File Encryption Runner
Course: Cryptography (CSL0509)
Faculty: Mr. Hirendra Singh Sengar
"""

import subprocess
import hashlib
import os

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res

def main():
    print("=" * 75)
    print(" PRACTICAL 04: OPENSSL RSA KEYPAIR GENERATION & FILE ENCRYPTION")
    print("=" * 75)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 1. Key generation
    print("[+] Generating 2048-bit RSA Private Key (private_key.pem)...")
    run_cmd("openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048")
    
    print("[+] Extracting RSA Public Key (public_key.pem)...")
    run_cmd("openssl pkey -in private_key.pem -pubout -out public_key.pem")
    
    # 2. Plaintext
    pt_msg = "Confidential Payload: Engineering Cryptography OpenSSL Practical Verification."
    with open("plaintext.txt", "w", encoding="utf-8") as f:
        f.write(pt_msg)
    h_orig = hashlib.sha256(pt_msg.encode('utf-8')).hexdigest()
    print(f"\n[+] Plaintext Message: '{pt_msg}'")
    print(f"    Original SHA-256: {h_orig}")
    
    # 3. Encrypt with OAEP
    print("\n[+] Encrypting 'plaintext.txt' with public_key.pem (RSA-OAEP)...")
    run_cmd("openssl pkeyutl -encrypt -pubin -inkey public_key.pem -in plaintext.txt -out ciphertext.bin -pkeyopt rsa_padding_mode:oaep")
    
    if os.path.exists("ciphertext.bin"):
        c_size = os.path.getsize("ciphertext.bin")
        print(f"    Ciphertext generated: 'ciphertext.bin' ({c_size} bytes)")
    
    # 4. Decrypt
    print("\n[+] Decrypting 'ciphertext.bin' with private_key.pem...")
    run_cmd("openssl pkeyutl -decrypt -inkey private_key.pem -in ciphertext.bin -out decrypted.txt -pkeyopt rsa_padding_mode:oaep")
    
    if os.path.exists("decrypted.txt"):
        with open("decrypted.txt", "r", encoding="utf-8") as f:
            dec_msg = f.read()
        h_dec = hashlib.sha256(dec_msg.encode('utf-8')).hexdigest()
        print(f"    Decrypted Content: '{dec_msg}'")
        print(f"    Decrypted SHA-256: {h_dec}")
        
        if h_orig == h_dec:
            print("\n[SUCCESS] RSA Encryption & Decryption 100% Verified! (SHA-256 Match)")
        else:
            print("\n[ERROR] Integrity Check Failed!")
            
    print("\n" + "=" * 75)
    print(" [OK] Practical 04 Completed Successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
