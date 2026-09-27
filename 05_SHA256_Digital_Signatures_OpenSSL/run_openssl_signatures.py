# -*- coding: utf-8 -*-
"""
Practical 05: SHA-256 Hash Values & Digital Signatures with OpenSSL
Course: Cryptography (CSL0509)
Faculty: Mr. Hirendra Singh Sengar
"""

import subprocess
import os

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res

def main():
    print("=" * 75)
    print(" PRACTICAL 05: OPENSSL SHA-256 HASHING & DIGITAL SIGNATURES")
    print("=" * 75)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 1. Generate keys
    run_cmd("openssl genpkey -algorithm RSA -out sender_private.pem -pkeyopt rsa_keygen_bits:2048")
    run_cmd("openssl pkey -in sender_private.pem -pubout -out sender_public.pem")
    
    # 2. Document
    doc_content = "AUTHORIZE WIRE TRANSFER: AMOUNT=$50,000 TO ACCOUNT: 987654321\n"
    with open("transaction.txt", "w", encoding="utf-8") as f:
        f.write(doc_content)
        
    # 3. Hash
    h_res = run_cmd("openssl dgst -sha256 transaction.txt")
    print(f"[+] SHA-256: {h_res.stdout.strip()}")
    
    # 4. Sign
    run_cmd("openssl dgst -sha256 -sign sender_private.pem -out signature.bin transaction.txt")
    print("[+] Digital Signature generated (256 bytes)")
    
    # 5. Verify authentic
    v_res = run_cmd("openssl dgst -sha256 -verify sender_public.pem -signature signature.bin transaction.txt")
    print(f"[+] Authentic Verification: {v_res.stdout.strip()}")
    
    # 6. Tamper
    with open("transaction.txt", "w", encoding="utf-8") as f:
        f.write("AUTHORIZE WIRE TRANSFER: AMOUNT=$90,000 TO ACCOUNT: 987654321\n")
        
    t_res = run_cmd("openssl dgst -sha256 -verify sender_public.pem -signature signature.bin transaction.txt")
    status = "TAMPER DETECTED / REJECTED" if "Verification Failure" in t_res.stdout or "Verification Failure" in t_res.stderr or t_res.returncode != 0 else "FAIL"
    print(f"[+] Tamper Test Result: {status}")
    
    # Restore
    with open("transaction.txt", "w", encoding="utf-8") as f:
        f.write(doc_content)
        
    print("=" * 75)

if __name__ == "__main__":
    main()
