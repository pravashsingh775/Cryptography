# -*- coding: utf-8 -*-
"""
Practical 08: Secure Text Messaging Application (AES-256 + SHA-256)
Course: Cryptography (CSL0509)
Faculty: Mr. Hirendra Singh Sengar
"""

import os
import hmac
import hashlib
import base64

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

def derive_keys(master_pass: str):
    h = hashlib.sha256(master_pass.encode('utf-8')).digest()
    enc_key = hashlib.sha256(h + b"ENC").digest()
    mac_key = hashlib.sha256(h + b"MAC").digest()
    return enc_key, mac_key

def secure_send(msg: str, master_pass: str) -> dict:
    enc_key, mac_key = derive_keys(master_pass)
    iv = os.urandom(16)
    
    if HAS_CRYPTO:
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(msg.encode('utf-8')) + padder.finalize()
        cipher = Cipher(algorithms.AES(enc_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    else:
        # Fallback XOR simulation
        ciphertext = bytes([b ^ enc_key[i % 32] for i, b in enumerate(msg.encode('utf-8'))])
        
    tag = hmac.new(mac_key, iv + ciphertext, hashlib.sha256).hexdigest()
    return {
        "iv": base64.b64encode(iv).decode('ascii'),
        "ciphertext": base64.b64encode(ciphertext).decode('ascii'),
        "tag": tag
    }

def secure_receive(payload: dict, master_pass: str) -> str:
    enc_key, mac_key = derive_keys(master_pass)
    iv = base64.b64decode(payload["iv"])
    ciphertext = base64.b64decode(payload["ciphertext"])
    received_tag = payload["tag"]
    
    expected_tag = hmac.new(mac_key, iv + ciphertext, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_tag, received_tag):
        raise ValueError("AUTHENTICATION FAILED: Message has been tampered with!")
        
    if HAS_CRYPTO:
        cipher = Cipher(algorithms.AES(enc_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
        return plaintext.decode('utf-8')
    else:
        plaintext = bytes([b ^ enc_key[i % 32] for i, b in enumerate(ciphertext)])
        return plaintext.decode('utf-8')

def main():
    print("=" * 75)
    print(" PRACTICAL 08: AES-256 & SHA-256 SECURE MESSAGING")
    print("=" * 75)
    
    secret_pass = "TopSecretSharedKey2026"
    msg = "Mission Directive: Transfer operative to safehouse Alpha at 0200 hrs."
    
    print(f"\n[+] Alice Sends: '{msg}'")
    payload = secure_send(msg, secret_pass)
    print(f"[+] Ciphertext (Base64): {payload['ciphertext'][:40]}...")
    print(f"[+] HMAC-SHA256 Tag:    {payload['tag']}")
    
    decrypted = secure_receive(payload, secret_pass)
    print(f"\n[+] Bob Decrypted: '{decrypted}'")
    
    # Tamper simulation
    print("\n[+] Simulating Adversarial Tampering...")
    tampered_payload = payload.copy()
    tampered_payload["ciphertext"] = base64.b64encode(b"TamperedDataBytes123456").decode('ascii')
    try:
        secure_receive(tampered_payload, secret_pass)
    except ValueError as e:
        print(f"[+] Tamper Defense Result: {e}")
        
    print("\n" + "=" * 75)
    print(" [OK] Practical 08 Completed Successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
