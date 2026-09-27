# Practical 12: Network Packet Analysis to Identify Secure and Insecure Protocols & Security Implications

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 12
- **Practical Problem Statement:** Analyze captured network packets to identify secure and insecure communication protocols and their security implications.
- **Tool Required:** Wireshark Network Protocol Analyzer
- **Bloom's Taxonomy Level:** BL4 (Analyze)
- **Course Outcome (CO):** CO4

---

## 🎯 Objectives
1. Capture, isolate, and contrast traditional **insecure cleartext protocols** against modern **cryptographically secured alternatives**:
   - **HTTP (Port 80)** vs **HTTPS (Port 443)**
   - **Telnet (Port 23)** vs **SSH (Port 22)**
   - **FTP (Port 21)** vs **SFTP (Port 22)** / **FTPS (Port 990)**
   - **DNS (Port 53)** vs **DNS-over-HTTPS (DoH - Port 443)**
2. Reconstruct transmission streams using Wireshark **Follow TCP Stream** to demonstrate credential harvesting.
3. Analyze security implications: Man-in-the-Middle (MITM), Session Hijacking, Eavesdropping, and Data Tampering.

---

## 🛠️ Tool Setup & Environment
- **Tool:** Wireshark
- **Protocol Security Matrix Architecture:**

```text
+------------------------------------------------------------------------+
|                 INSECURE PROTOCOLS VS SECURE PROTOCOLS                 |
+------------------------------------------------------------------------+
|                                                                        |
|  [INSECURE LEGACY PROTOCOLS]            [SECURE CRYPTOGRAPHIC EQUIV.]  |
|                                                                        |
|  1. HTTP (TCP 80)     ===============>  1. HTTPS (TLS/TCP 443)         |
|     - Plaintext headers & HTML             - AEAD Encrypted (AES-GCM)  |
|                                                                        |
|  2. Telnet (TCP 23)   ===============>  2. SSH (TCP 22)                |
|     - Plaintext keystrokes & login         - Encrypted asymmetric auth |
|                                                                        |
|  3. FTP (TCP 21)      ===============>  3. SFTP / FTPS (TCP 22/990)    |
|     - USER & PASS in cleartext             - Encrypted SSH data stream |
|                                                                        |
|  4. DNS (UDP 53)      ===============>  4. DoH / DoT (TCP 443 / 853)   |
|     - Unauthenticated queries              - Encrypted TLS tunnel      |
+------------------------------------------------------------------------+
```

---

## 💻 Step-by-Step Wireshark Packet Inspection & Stream Following

1. **Inspect Telnet (Port 23) vs SSH (Port 22):**
   - Wireshark filter: `telnet`
   - Select packet -> **Follow -> TCP Stream**.
   - Output reveals login credentials and typed shell commands in raw ASCII!
   - Wireshark filter: `ssh`
   - Select packet -> **Follow -> TCP Stream**.
   - Output reveals random encrypted binary stream.
2. **Inspect FTP (Port 21) vs SFTP (Port 22):**
   - Wireshark filter: `ftp`
   - Filter `ftp.request.command == "USER" || ftp.request.command == "PASS"`
   - Observe plaintext `USER admin` and `PASS SecretPassword123`.

---

## 📊 Results & Protocol Dissection Comparison

```text
===========================================================================
 PROTOCOL PACKET AUDIT & STREAM EXTRACTION RESULTS
===========================================================================

[1] INSECURE TELNET STREAM (TCP Stream 3):
---------------------------------------------------------------------------
Connected to lab-router.local.
login: network_admin
Password: RouterMasterPassword2026#
Router# configure terminal
Router(config)# interface gigabitEthernet 0/1
Router(config-if)# ip address 192.168.10.1 255.255.255.0
---------------------------------------------------------------------------
-> VULNERABILITY: Total credential and configuration compromise!

[2] SECURE SSH STREAM (TCP Stream 5):
---------------------------------------------------------------------------
SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u2
......k.9...diffie-hellman-group-exchange-sha256,curve25519-sha256...
.Z#...$.f.x..8.N.......s......l.L...%.9.....[ENCRYPTED PAYLOAD BYTES]
---------------------------------------------------------------------------
-> SECURITY STATUS: Confidentiality, Integrity, and Server Auth preserved!

[3] INSECURE FTP CAPTURE:
  Frame 84: Request: USER student
  Frame 86: Response: 331 Please specify the password.
  Frame 88: Request: PASS LabPassword2026!
  Frame 90: Response: 230 Login successful.
-> VULNERABILITY: Cleartext password harvested in 4 packets!
===========================================================================
```

---

## 📈 Protocol Security Comparison Table (BL4 Analyze)

| Feature / Metric | Insecure Legacy Protocols | Secure Cryptographic Protocols | Security Risk / Implication |
|:---|:---|:---|:---|
| **Web Browsing** | **HTTP** (TCP 80) | **HTTPS** (TCP 443 / TLS) | Session hijacking, cookie theft, MITM content injection |
| **Remote Shell** | **Telnet** (TCP 23) | **SSH** (TCP 22) | Total credential capture, arbitrary command injection |
| **File Transfer** | **FTP** (TCP 21) | **SFTP** (TCP 22) / **FTPS** | Plaintext password capture, file contents exfiltration |
| **Domain Resolution** | **DNS** (UDP 53) | **DoH** (Port 443) / **DoT** (Port 853)| DNS spoofing, cache poisoning, ISP surveillance |
| **Email Retrieval** | **POP3 / IMAP** (110/143) | **POP3S / IMAPS** (995/993) | Email message exposure, account hijacking |

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: Why is Telnet considered obsolete and dangerous on modern networks?**
   - **Answer:** Telnet transmits all data, including usernames, passwords, and administrative commands, as unencrypted plaintext. Anyone on the local network or path can capture full credentials using a basic packet sniffer.

2. **Q2: What is the primary difference between SFTP and FTPS?**
   - **Answer:**
     - **SFTP (SSH File Transfer Protocol):** Runs as a subsystem over an encrypted **SSH connection** on port 22.
     - **FTPS (FTP over SSL/TLS):** Standard FTP encapsulated inside a **TLS tunnel** on ports 989/990 or explicit TLS on port 21.

3. **Q3: What attack does DNSSEC prevent compared to standard DNS?**
   - **Answer:** Standard DNS is unauthenticated and vulnerable to **DNS Cache Poisoning** and spoofing. DNSSEC adds cryptographic digital signatures to DNS records (RRSIG), allowing resolvers to verify the authenticity and integrity of DNS responses.
