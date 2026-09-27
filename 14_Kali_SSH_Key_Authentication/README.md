# Practical 14: SSH/RSA Keypair Generation and Passwordless Authentication (Kali Linux)

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 14
- **Practical Problem Statement:** Generate SSH/RSA key pairs and configure passwordless authentication between Linux systems.
- **Tool Required:** Kali Linux (OpenSSH Client & Server)
- **Bloom's Taxonomy Level:** BL3 (Apply)
- **Course Outcome (CO):** CO3

---

## 🎯 Objectives
1. Generate high-security **RSA 4096-bit** and **ED25519** SSH keypairs.
2. Deploy the public key to a target Linux server using `ssh-copy-id`.
3. Configure and verify **Passwordless Public-Key Authentication** via SSH Challenge-Response.
4. Harden the SSH daemon (`/etc/ssh/sshd_config`) by disabling plaintext password authentication and root login.

---

## 🛠️ Tool Setup & Environment
- **OS:** Kali Linux (Client) & Ubuntu/Debian Linux (Server)
- **Tool:** OpenSSH (`ssh-keygen`, `ssh-copy-id`, `ssh`)
- **SSH Authentication Protocol Sequence:**

```text
+------------------------------------------------------------------------+
|                 SSH PUBLIC-KEY CHALLENGE-RESPONSE PROTOCOL             |
+------------------------------------------------------------------------+
|  CLIENT (Kali Linux)                                  SERVER (Remote)  |
|  ~/.ssh/id_rsa (Private Key)                          ~/.ssh/authorized_keys
|         |                                                   |          |
|         | ----- [1. SSH Connection Request (User: alice)] ->|          |
|         |                                                   |          |
|         | <---- [2. Server looks up ~/.ssh/authorized_keys] |          |
|         |       Generates random 256-bit Challenge R        |          |
|         |       Encrypts Challenge with Alice Public Key    |          |
|         |       <---- Send Encrypted Challenge -------------|          |
|         |                                                   |          |
|         | [3. Alice Decrypts R using ~/.ssh/id_rsa]         |          |
|         |     Computes Response S = SHA256(R || SessionID)  |          |
|         |     ----- Send Response S ----------------------->|          |
|         |                                                   |          |
|         |                                 [4. Server Validates S]      |
|         |                                 - If MATCH: ACCESS GRANTED!  |
|         | <==== [5. Encrypted Interactive Shell Granted] == |          |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. SSH Public Key Authentication
Unlike password authentication where credentials travel across the network (even if encrypted inside SSH), public-key authentication uses a **Zero-Knowledge Challenge-Response**:
- The private key **never leaves the client machine**.
- The server proves the client holds the corresponding private key without learning the private key itself.

### 2. Permissions Hierarchy & OpenSSH StrictModes
OpenSSH enforces strict POSIX filesystem permissions to prevent local privilege escalation:
- `~/.ssh/` directory: `chmod 700` (`drwx------`)
- `~/.ssh/authorized_keys`: `chmod 600` (`-rw-------`)
- `~/.ssh/id_rsa` (Private Key): `chmod 600` (`-rw-------`)
- `~/.ssh/id_rsa.pub` (Public Key): `chmod 644` (`-rw-r--r--`)

---

## 💻 Step-by-Step Kali Linux Commands & Procedure

1. **Generate 4096-bit RSA SSH Keypair:**
   ```bash
   ssh-keygen -t rsa -b 4096 -C "student@crypto.lab" -f ~/.ssh/id_rsa -N ""
   ```

2. **Alternatively Generate High-Performance ED25519 Keypair:**
   ```bash
   ssh-keygen -t ed25519 -C "student@crypto.lab" -f ~/.ssh/id_ed25519 -N ""
   ```

3. **Install Public Key onto Target Remote Server:**
   ```bash
   ssh-copy-id -i ~/.ssh/id_rsa.pub user@192.168.1.100
   ```

4. **Test Passwordless Login:**
   ```bash
   ssh -i ~/.ssh/id_rsa user@192.168.1.100 "hostname && whoami"
   ```

5. **Harden Server Configuration (`/etc/ssh/sshd_config`):**
   ```bash
   sudo nano /etc/ssh/sshd_config
   # Set the following parameters:
   PubkeyAuthentication yes
   PasswordAuthentication no
   PermitEmptyPasswords no
   PermitRootLogin no
   
   # Restart SSH Daemon:
   sudo systemctl restart sshd
   ```

---

## 📊 Results & Terminal Execution Output

```text
===========================================================================
 KALI LINUX SSH KEY AUTHENTICATION DEPLOYMENT LOGS
===========================================================================

kali@kali:~$ ssh-keygen -t rsa -b 4096 -C "admin@crypto.lab" -f ~/.ssh/id_rsa -N ""
Generating public/private rsa 4096 bit key pair.
Your identification has been saved in /home/kali/.ssh/id_rsa
Your public key has been saved in /home/kali/.ssh/id_rsa.pub
The key's randomart image is:
+---[RSA 4096]----+
|        .+=o     |
|       . o+o.    |
|      . o.o.     |
|     . + + =     |
|      o S * .    |
|     . = B o     |
|      = B B .    |
|     o = * *     |
|      E o.B.     |
+----[SHA256]-----+

kali@kali:~$ ssh-copy-id -i ~/.ssh/id_rsa.pub user@192.168.1.50
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/kali/.ssh/id_rsa.pub"
user@192.168.1.50's password: 
Number of key(s) added: 1

kali@kali:~$ ssh user@192.168.1.50
Linux crypto-server 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian
Last login: Sun Sep 27 10:52:14 2026 from 192.168.1.20
user@crypto-server:~$ (Authenticated instantly without password prompt!)
===========================================================================
```

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: Why is SSH public-key authentication significantly more secure than passwords?**
   - **Answer:** Public-key cryptography eliminates brute-force dictionary attacks against credentials. The private key has an entropy of 2048 to 4096 bits (infeasible to guess), and credentials are never sent across the network, eliminating interception and credential theft.

2. **Q2: Why will SSH fail to authenticate if permissions on `~/.ssh` or `authorized_keys` are world-writable (`chmod 777`)?**
   - **Answer:** OpenSSH's `StrictModes` checks file permissions. If permissions allow other non-root users to write to `~/.ssh` or `authorized_keys`, an attacker on the system could insert their own public key and gain unauthorized access. OpenSSH intentionally refuses to use insecure files.

3. **Q3: What is the benefit of ED25519 keys over RSA 2048/4096?**
   - **Answer:** ED25519 (Edwards-curve Digital Signature Algorithm) offers equivalent or higher security (128-bit security level) with much shorter key lengths (256 bits vs 4096 bits), faster signature generation/verification, and inherent resistance to side-channel timing attacks.
