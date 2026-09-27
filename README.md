# Cryptography (CSL0509) — Laboratory Activity Manual & Repository

## 🏛️ Academic Course Details
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Activity Document:** ABCA ACTIVITY DOCUMENT — Cryptography – Laboratory Activity
- **Total Marks:** 40 Marks (Lab Experiments — GitHub Deployment)

---

## 🎯 Activity Description & Objectives

This repository contains the complete laboratory practical portfolio for the **Cryptography and Network Security** curriculum. It provides hands-on implementation, mathematical modeling, simulation, and security analysis using industry-standard tools including **CrypTool, OpenSSL, Visual Studio Code (Python), Wireshark, Kali Linux, and Cisco Packet Tracer**.

### Objectives
1. **Apply** classical and modern cryptographic algorithms for data encryption, decryption, and key exchange.
2. **Analyze** the strength, vulnerabilities, and performance characteristics of cryptographic ciphers, hashing functions, and security protocols.
3. Gain hands-on exposure to real-world security engineering tools used in research and industry.
4. Maintain a structured, version-controlled practical portfolio deployed on GitHub.

---

## 📊 Bloom's Taxonomy Coverage

| Level | Classification | Description | Experiments Covered |
|:---:|:---:|:---|:---|
| **BL3** | **Apply** | Implement cryptographic algorithms, generate keys, establish VPNs, and configure network security protocols. | Practicals 04, 05, 07, 08, 14, 15, 16 |
| **BL4** | **Analyze** | Dissect cipher vulnerability, evaluate frequency distributions, benchmark speed/avalanche metrics, and audit packet streams. | Practicals 01, 02, 03, 06, 09, 10, 11, 12, 13 |

---

## 🗂️ Laboratory Directory Structure & Practical Index

```text
Cryptography/
│
├── README.md                                    # Master Laboratory Portfolio Index & Syllabus
├── run_lab.py                                   # Master 1-Click Interactive & Batch Test Controller
├── Tools_Setup/                                 # CrypTool installer and setup assets
│   └── SetupCrypTool_1_4_42_en.exe
│
├── 01_Classical_Ciphers_CrypTool/               # Caesar, Vigenère & Rail Fence ("HELLO WORLD")
│   ├── README.md
│   └── classical_ciphers.py
│
├── 02_Frequency_Analysis_CrypTool/              # Letter Frequency & Automated Cryptanalysis
│   ├── README.md
│   └── frequency_cryptanalysis.py
│
├── 03_DES_vs_AES_CrypTool/                      # DES vs AES Performance & Avalanche Benchmark
│   ├── README.md
│   └── des_vs_aes_benchmark.py
│
├── 04_RSA_Keys_File_Crypto_OpenSSL/             # OpenSSL RSA 2048-bit Keypair & OAEP File Crypto
│   ├── README.md
│   ├── run_openssl_rsa.py
│   └── rsa_crypto.sh
│
├── 05_SHA256_Digital_Signatures_OpenSSL/        # OpenSSL SHA-256 Signatures & Tamper Testing
│   ├── README.md
│   ├── run_openssl_signatures.py
│   └── signatures.sh
│
├── 06_X509_Certificates_OpenSSL/                # OpenSSL Self-Signed X.509 Certificate Generation
│   ├── README.md
│   ├── run_openssl_x509.py
│   └── x509_cert.sh
│
├── 07_RSA_and_Diffie_Hellman_Python/            # Pure Python RSA & Diffie-Hellman from Math
│   ├── README.md
│   └── rsa_and_diffie_hellman.py
│
├── 08_AES_and_SHA256_Messaging_Python/          # AES-256-CBC + SHA-256/HMAC Secure Messaging
│   ├── README.md
│   └── secure_messaging.py
│
├── 09_Password_Hashing_Salting_Python/          # Salted PBKDF2 vs Unsalted SHA-256 Attack Audit
│   ├── README.md
│   └── password_hashing_attacks.py
│
├── 10_Wireshark_HTTPS_TLS_Handshake/            # TLS 1.2/1.3 Handshake, Certs & Cipher Suites
│   ├── README.md
│   └── tls_handshake_guide.md
│
├── 11_Wireshark_VPN_vs_Unencrypted_Traffic/     # VPN Tunnel vs Plaintext Traffic Comparison
│   ├── README.md
│   └── vpn_traffic_guide.md
│
├── 12_Wireshark_Secure_vs_Insecure_Protocols/   # HTTP/HTTPS, Telnet/SSH, FTP/SFTP Analysis
│   ├── README.md
│   └── protocol_audit_guide.md
│
├── 13_Kali_John_The_Ripper/                     # Password Auditing with John the Ripper
│   ├── README.md
│   └── audit_demo.sh
│
├── 14_Kali_SSH_Key_Authentication/              # SSH 4096-bit Passwordless Authentication Setup
│   ├── README.md
│   └── setup_ssh_keys.sh
│
├── 15_Kali_OpenVPN_Configuration/               # OpenVPN Server/Client PKI & Secure Tunnel
│   ├── README.md
│   ├── server.conf
│   └── client.ovpn
│
└── 16_PacketTracer_WPA2_AES_Wireless/           # WPA2-Personal (AES) Wireless Network Simulation
    ├── README.md
    └── cisco_wlan_config.ios
```

---

## 📋 Comprehensive Syllabus Mapping & Practical Registry

| S.No. | Practical Problem Statement | Tool Required | Bloom's Level | Folder Link |
|:---:|:---|:---:|:---:|:---|
| **01** | Implement Caesar, Vigenère, and Rail Fence ciphers to encrypt and decrypt plaintext, and compare their working and effectiveness. The given plain text is **"HELLO WORLD"**. | **CrypTool** | **BL4 (Analyze)** | [01_Classical_Ciphers_CrypTool](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/01_Classical_Ciphers_CrypTool/README.md) |
| **02** | Perform frequency analysis on classical cipher texts and analyze their vulnerability to cryptanalysis attacks using CrypTool. | **CrypTool** | **BL4 (Analyze)** | [02_Frequency_Analysis_CrypTool](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/02_Frequency_Analysis_CrypTool/README.md) |
| **03** | Encrypt sample data using DES and AES algorithms, and compare their security features and performance. | **CrypTool** | **BL4 (Analyze)** | [03_DES_vs_AES_CrypTool](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/03_DES_vs_AES_CrypTool/README.md) |
| **04** | Generate RSA public and private key pairs and perform secure file encryption and decryption using OpenSSL. | **OpenSSL** | **BL3 (Apply)** | [04_RSA_Keys_File_Crypto_OpenSSL](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/04_RSA_Keys_File_Crypto_OpenSSL/README.md) |
| **05** | Generate SHA-256 hash values, create digital signatures, and verify their authenticity using OpenSSL. | **OpenSSL** | **BL3 (Apply)** | [05_SHA256_Digital_Signatures_OpenSSL](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/05_SHA256_Digital_Signatures_OpenSSL/README.md) |
| **06** | Create a self-signed X.509 digital certificate and analyze its attributes, validity, and security features. | **OpenSSL** | **BL4 (Analyze)** | [06_X509_Certificates_OpenSSL](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/06_X509_Certificates_OpenSSL/README.md) |
| **07** | Implement RSA and Diffie–Hellman algorithms to demonstrate secure key exchange and public-key cryptography using VS Code. | **Visual Studio Code** | **BL3 (Apply)** | [07_RSA_and_Diffie_Hellman_Python](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/07_RSA_and_Diffie_Hellman_Python/README.md) |
| **08** | Develop an application to secure text messages using AES encryption and SHA-256 hashing using VS Code. | **Visual Studio Code** | **BL3 (Apply)** | [08_AES_and_SHA256_Messaging_Python](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/08_AES_and_SHA256_Messaging_Python/README.md) |
| **09** | Implement password hashing with and without salting, and evaluate resistance against common password attacks using VS Code. | **Visual Studio Code** | **BL4 (Analyze)** | [09_Password_Hashing_Salting_Python](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/09_Password_Hashing_Salting_Python/README.md) |
| **10** | Capture HTTPS network traffic using Wireshark and analyze the TLS handshake, digital certificates, and cipher suites. | **Wireshark** | **BL4 (Analyze)** | [10_Wireshark_HTTPS_TLS_Handshake](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/10_Wireshark_HTTPS_TLS_Handshake/README.md) |
| **11** | Capture and analyze encrypted VPN traffic using Wireshark, and compare it with unencrypted network communication. | **Wireshark** | **BL4 (Analyze)** | [11_Wireshark_VPN_vs_Unencrypted_Traffic](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/11_Wireshark_VPN_vs_Unencrypted_Traffic/README.md) |
| **12** | Analyze captured network packets to identify secure and insecure communication protocols and their security implications. | **Wireshark** | **BL4 (Analyze)** | [12_Wireshark_Secure_vs_Insecure_Protocols](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/12_Wireshark_Secure_vs_Insecure_Protocols/README.md) |
| **13** | Perform password auditing using John the Ripper and evaluate password strength against dictionary and brute-force attacks. | **Kali Linux** | **BL4 (Analyze)** | [13_Kali_John_The_Ripper](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/13_Kali_John_The_Ripper/README.md) |
| **14** | Generate SSH/RSA key pairs and configure passwordless authentication between Linux systems. | **Kali Linux** | **BL3 (Apply)** | [14_Kali_SSH_Key_Authentication](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/14_Kali_SSH_Key_Authentication/README.md) |
| **15** | Configure a secure VPN using OpenVPN and verify encrypted communication between connected systems. | **Kali Linux** | **BL3 (Apply)** | [15_Kali_OpenVPN_Configuration](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/15_Kali_OpenVPN_Configuration/README.md) |
| **16** | Design and implement a secure wireless network using WPA2 encryption (AES) in Cisco Packet Tracer, and verify secure communication. | **Cisco Packet Tracer** | **BL3 (Apply)** | [16_PacketTracer_WPA2_AES_Wireless](file:///c:/Users/PRAVASH/Desktop/5th_Sem_Acadmics/Cryptography/16_PacketTracer_WPA2_AES_Wireless/README.md) |

---

## 🚀 Quick Execution Guide

To execute and verify all executable practicals (Practicals 01 to 09) via the master controller:

```bash
# Run the interactive runner:
python run_lab.py

# Or run in non-interactive all-tests mode:
python run_lab.py --all
```

---

## ✅ Student Submission Checklist

- [x] GitHub repository created and deployed.
- [x] All 16 experiments documented in separate, clearly labeled directories.
- [x] Detailed working procedures included for every practical.
- [x] Tool setup and environment architecture illustrations provided.
- [x] Algorithms included in mathematical and pseudocode formulations.
- [x] Verbatim terminal outputs, verification logs, and packet dissections recorded.
- [x] Viva-Voce questions with comprehensive technical answers included for each experiment.
