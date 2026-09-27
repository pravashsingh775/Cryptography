# -*- coding: utf-8 -*-
"""
Practical 06: Self-Signed X.509 Digital Certificate Runner
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
    print(" PRACTICAL 06: X.509 CERTIFICATE GENERATION & ATTRIBUTE DISSECTION")
    print("=" * 75)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 1. Generate self-signed cert
    cmd = (
        'openssl req -x509 -newkey rsa:2048 -nodes -keyout server_key.pem -out server_cert.crt -days 365 '
        '-subj "/C=IN/ST=Maharashtra/L=Mumbai/O=EngineeringCollege/CN=crypto.lab.local"'
    )
    run_cmd(cmd)
    
    # 2. Parse attributes
    issuer = run_cmd("openssl x509 -in server_cert.crt -issuer -noout").stdout.strip()
    subject = run_cmd("openssl x509 -in server_cert.crt -subject -noout").stdout.strip()
    dates = run_cmd("openssl x509 -in server_cert.crt -dates -noout").stdout.strip()
    fingerprint = run_cmd("openssl x509 -in server_cert.crt -fingerprint -sha256 -noout").stdout.strip()
    
    print("\n[+] Certificate 'server_cert.crt' created successfully!")
    print(f"    {issuer}")
    print(f"    {subject}")
    for d in dates.splitlines():
        print(f"    {d}")
    print(f"    {fingerprint}")
    
    print("=" * 75)

if __name__ == "__main__":
    main()
