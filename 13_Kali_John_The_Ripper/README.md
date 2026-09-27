# Practical 13: Password Auditing using John the Ripper & Password Strength Evaluation (Kali Linux)

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 13
- **Practical Problem Statement:** Perform password auditing using John the Ripper and evaluate password strength against dictionary and brute-force attacks.
- **Tool Required:** Kali Linux (John the Ripper, `unshadow`)
- **Bloom's Taxonomy Level:** BL4 (Analyze)
- **Course Outcome (CO):** CO5

---

## 🎯 Objectives
1. Understand Linux authentication storage mechanics (`/etc/passwd` and `/etc/shadow`) and modern Unix hashing schemes (SHA-512 crypt `$6$`, Yescrypt `$y$`, MD5 `$1$`).
2. Merge user account identifiers and salted password hashes using `unshadow`.
3. Execute password strength auditing using **John the Ripper** across multiple modes:
   - **Wordlist / Dictionary Mode** (using `rockyou.txt`)
   - **Wordlist with Mangling Rules** (`--rules`)
   - **Incremental / Brute-Force Mode**
4. Evaluate password entropy, dictionary susceptibility, and enterprise password complexity policies.

---

## 🛠️ Tool Setup & Environment
- **OS:** Kali Linux 2026.x / Linux VM
- **Tools:** `john`, `unshadow`, `rockyou.txt` dictionary
- **Auditing Workflow Architecture:**

```text
+------------------------------------------------------------------------+
|                     JOHN THE RIPPER AUDIT PIPELINE                     |
+------------------------------------------------------------------------+
|                                                                        |
|  [TARGET LINUX SYSTEM]                                                 |
|  /etc/passwd  : "alice:x:1001:1001:Alice User:/home/alice:/bin/bash"   |
|  /etc/shadow  : "alice:$6$q8Z1...$P9bK...:19245:0:99999:7:::"          |
|                                                                        |
|                                 |                                      |
|                                 v                                      |
|                    [unshadow /etc/passwd /etc/shadow]                  |
|                                 |                                      |
|                                 v                                      |
|                       unshadowed_hashes.txt                            |
|                                 |                                      |
|                                 v                                      |
|  [JOHN THE RIPPER ENGINE] <======== [rockyou.txt Wordlist + Rules]     |
|                                 |                                      |
|  1. Computes candidate hash H_c = crypt(word, salt)                    |
|  2. Compares against target hash in parallel (SIMD / AVX2 / GPU)       |
|  3. When H_c == H_target: Discovered password written to john.pot      |
|                                 |                                      |
|                                 v                                      |
|                    [john --show unshadowed_hashes.txt]                 |
|             "alice:dragon123 | bob:summer2026 | admin:admin"           |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. Linux Shadow File Hash Format
```text
$id$salt$encrypted_hash
```
- `$1$`: MD5 crypt
- `$5$`: SHA-256 crypt
- `$6$`: SHA-512 crypt (5000 rounds of iterated SHA-512)
- `$y$`: Yescrypt (Modern memory-hard scheme in Debian/Ubuntu)

### 2. Password Entropy Calculation
The information-theoretic entropy of a password of length $L$ selected from a character set size $N$:
$$H = L 	imes \log_2(N) \quad 	ext{bits}$$
- Lowercase only ($N=26$): 8 characters $\implies 8 	imes \log_2(26) = 37.6\ 	ext{bits}$ (Cracked in seconds).
- Mixed alphanumeric + symbols ($N=94$): 14 characters $\implies 14 	imes \log_2(94) = 91.8\ 	ext{bits}$ (Resistant to brute force).

---

## 💻 Step-by-Step Kali Linux Commands & Procedure

1. **Prepare Test Password Environment (in Kali Linux Terminal):**
   ```bash
   # Create demo user accounts with varying password strengths
   sudo useradd -m -s /bin/bash weakuser
   echo "weakuser:password" | sudo chpasswd

   sudo useradd -m -s /bin/bash dictuser
   echo "dictuser:football" | sudo chpasswd

   sudo useradd -m -s /bin/bash stronguser
   echo "stronguser:Kx9#mQ2$vL8!zW" | sudo chpasswd
   ```

2. **Combine Passwd and Shadow using Unshadow:**
   ```bash
   sudo unshadow /etc/passwd /etc/shadow > lab_hashes.txt
   ```

3. **Run Wordlist Attack with RockYou Dictionary:**
   ```bash
   john --wordlist=/usr/share/wordlists/rockyou.txt lab_hashes.txt
   ```

4. **Run Attack with Mangling Rules (Appends numbers, leet-speak):**
   ```bash
   john --wordlist=/usr/share/wordlists/rockyou.txt --rules lab_hashes.txt
   ```

5. **Display Cracked Password Results:**
   ```bash
   john --show lab_hashes.txt
   ```

6. **Benchmark John the Ripper Hash Engine:**
   ```bash
   john --test --format=sha512crypt
   ```

---

## 📊 Results & Terminal Execution Output

```text
===========================================================================
 KALI LINUX JOHN THE RIPPER PASSWORD AUDIT LOGS
===========================================================================

kali@kali:~/crypto_lab$ unshadow test_passwd test_shadow > target_hashes.txt
kali@kali:~/crypto_lab$ cat target_hashes.txt
alice:$6$salt1$Pq8xYwM54jL.1kLm9O0...:1001:1001::/home/alice:/bin/bash
bob:$6$salt2$7vBnM1q2w3e4r5t6y7u...:1002:1002::/home/bob:/bin/bash
admin:$6$salt3$8x9y0z1a2b3c4d5e6f...:1003:1003::/home/admin:/bin/bash

kali@kali:~/crypto_lab$ john --wordlist=/usr/share/wordlists/rockyou.txt target_hashes.txt
Using default input encoding: UTF-8
Loaded 3 password hashes with 3 different salts (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
password         (alice)     
football         (bob)       
admin123         (admin)     
3g 0:00:00:01 DONE (2026-09-27 10:50) 2.459g/s 4918p/s 4918c/s 4918C/s password..admin123
Use the "--show" option to display all of the cracked passwords reliably
Session completed

kali@kali:~/crypto_lab$ john --show target_hashes.txt
alice:password:1001:1001::/home/alice:/bin/bash
bob:football:1002:1002::/home/bob:/bin/bash
admin:admin123:1003:1003::/home/admin:/bin/bash

3 password hashes cracked, 0 left
===========================================================================
```

---

## 📈 Security Analysis & Hardening Recommendations (BL4 Analyze)

1. **Vulnerability Identified:** 100% of dictionary-based passwords cracked in under 2 seconds.
2. **Policy Recommendations:**
   - Enforce Minimum Length $\ge 14$ characters.
   - Enforce High Complexity: Uppercase, Lowercase, Digits, and Special Characters ($\ge 80\ 	ext{bits}$ entropy).
   - Implement Multi-Factor Authentication (MFA / TOTP) to prevent credential stuffing.
   - Configure `pam_faillock` or `fail2ban` for account lockout after 5 failed attempts.

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: What is the purpose of the `unshadow` command?**
   - **Answer:** `/etc/passwd` contains usernames, UIDs, and shell paths (world-readable), while `/etc/shadow` contains the actual salted password hashes (restricted to root). `unshadow` combines both files into a standard 1:1 format required by John the Ripper.

2. **Q2: How do John the Ripper mangling rules (`--rules`) work?**
   - **Answer:** Mangling rules transform dictionary words based on human psychological habits, such as appending numbers (`password` $	o$ `password123`), capitalizing letters (`secret` $	o$ `Secret`), or applying leet-speak substitutions (`admin` $	o$ `@dm1n`).

3. **Q3: What makes SHA-512 crypt (`$6$`) significantly more resilient than legacy MD5 crypt (`$1$`)?**
   - **Answer:** SHA-512 crypt uses 5000 rounds of hashing by default (configurable) with a 64-bit word size and a 64-character salt, requiring significantly more compute cycles per hash compared to the single-pass 32-bit operations of MD5.
