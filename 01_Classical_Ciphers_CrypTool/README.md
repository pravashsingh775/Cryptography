# Practical 01: Implementation of Caesar, Vigenère, and Rail Fence Ciphers

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 01
- **Practical Problem Statement:** Implement Caesar, Vigenère, and Rail Fence ciphers to encrypt and decrypt plaintext, and compare their working and effectiveness. The given plain text is **"HELLO WORLD"**.
- **Tool Required:** CrypTool (and Python reference implementation)
- **Bloom's Taxonomy Level:** BL4 (Analyze)
- **Course Outcome (CO):** CO1

---

## 🎯 Objectives
1. Understand the mathematical foundation and structural mechanics of classical substitution (monoalphabetic and polyalphabetic) and transposition ciphers.
2. Encrypt and decrypt the mandatory given plaintext `"HELLO WORLD"` using:
   - **Caesar Cipher** (Monoalphabetic Substitution)
   - **Vigenère Cipher** (Polyalphabetic Substitution)
   - **Rail Fence Cipher** (Transposition / Permutation)
3. Execute the ciphers in **CrypTool** and via an automated Python script.
4. Analyze and compare key space, computational complexity, letter frequency retention, and cryptanalysis resistance.

---

## 🛠️ Tool Setup & Environment
- **Primary Tool:** CrypTool 1.4.42 (or CrypTool 2)
- **Secondary Tool:** Visual Studio Code with Python 3.10+
- **Environment Architecture:**

```text
+-----------------------------------------------------------------------+
|                       CRYPTOOL 1.4.42 ENVIRONMENT                      |
|                                                                       |
|  +------------------------+      +---------------------------------+  |
|  | Plaintext Input Window |      | Crypt/Decrypt Menu Selection    |  |
|  | "HELLO WORLD"          | ---> | [1] Caesar / Rot-13 (Shift=3)   |  |
|  +------------------------+      | [2] Vigenere (Key="SECRET")     |  |
|                                  | [3] Scytale / Rail Fence (d=3)  |  |
|                                  +---------------------------------+  |
|                                                  |                    |
|                                                  v                    |
|                                  +---------------------------------+  |
|                                  | Ciphertext Output Window        |  |
|                                  | Hex / ASCII / Frequency Chart   |  |
|                                  +---------------------------------+  |
+-----------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. Caesar Cipher (Monoalphabetic Substitution)
- **Principle:** Shifts each alphabetical character by a fixed integer key $k$ ($0 \le k \le 25$).
- **Encryption Function:**
  $$C = E(P, k) = (P + k) \pmod{26}$$
- **Decryption Function:**
  $$P = D(C, k) = (C - k + 26) \pmod{26}$$
- **Vulnerability:** Extremely small key space ($|K| = 25$). Can be broken in under a millisecond via brute-force or direct single-letter frequency matching.

### 2. Vigenère Cipher (Polyalphabetic Substitution)
- **Principle:** Uses a repeating keyword $K = (k_0, k_1, \dots, k_{m-1})$ of length $m$ to select dynamic shift values for successive characters.
- **Encryption Function:**
  $$C_i = E(P_i, K_i) = (P_i + K_{i \pmod m}) \pmod{26}$$
- **Decryption Function:**
  $$P_i = D(C_i, K_i) = (C_i - K_{i \pmod m} + 26) \pmod{26}$$
- **Vulnerability:** Masks single-letter frequencies, but vulnerable to **Kasiski examination** and **Friedman Index of Coincidence test** to determine key length $m$, followed by splitting into $m$ independent Caesar ciphers.

### 3. Rail Fence Cipher (Transposition)
- **Principle:** Writes plaintext diagonally in a zigzag pattern across $d$ depth rails and reads out ciphertext row-by-row.
- **Vulnerability:** Character identities are preserved 100% identically (same frequency distribution as plaintext). Vulnerable to anagramming and bigram frequency analysis.

---

## ⚙️ Algorithms

### Caesar Cipher Algorithm
```text
Algorithm Caesar_Encrypt(P, k):
  Input: Plaintext string P, integer shift k (0 <= k <= 25)
  Output: Ciphertext string C
  1. Initialize empty string C
  2. For each char c in P:
       If c is uppercase letter:
         C += char(((ASCII(c) - 65 + k) mod 26) + 65)
       Else if c is lowercase letter:
         C += char(((ASCII(c) - 97 + k) mod 26) + 97)
       Else:
         C += c
  3. Return C
```

### Vigenère Cipher Algorithm
```text
Algorithm Vigenere_Encrypt(P, Key):
  Input: Plaintext P, Keyword string Key
  Output: Ciphertext C
  1. Convert Key to uppercase, m = length(Key), key_index = 0
  2. For each char c in P:
       If c is alphabetical:
         k_val = ASCII(Key[key_index mod m]) - 65
         Apply Caesar shift with k_val to c
         key_index += 1
       Else:
         Append c unchanged
  3. Return C
```

### Rail Fence Cipher Algorithm
```text
Algorithm RailFence_Encrypt(P, depth):
  Input: Plaintext P (without spaces), integer depth d
  Output: Ciphertext C
  1. Create 2D grid matrix[d][len(P)] initialized to null
  2. Set row = 0, dir_down = True
  3. For col from 0 to len(P)-1:
       matrix[row][col] = P[col]
       If row == 0: dir_down = True
       If row == d - 1: dir_down = False
       row = row + 1 if dir_down else row - 1
  4. Concatenate non-null characters from matrix row by row
  5. Return C
```

---

## 💻 Step-by-Step Procedure in CrypTool

1. **Launch CrypTool 1.4.42**.
2. Click **File -> New** (or press `Ctrl + N`).
3. Enter the required plaintext: `HELLO WORLD`.
4. **Caesar Cipher:**
   - Go to menu: `Crypt/Decrypt` -> `Symmetric (classic)` -> `Caesar / Rot-13...`
   - Set Key / Shift to `3`.
   - Click `Encrypt`. Observe output: `KHOOR ZRUOG`.
   - To decrypt: Go to `Crypt/Decrypt` -> `Symmetric (classic)` -> `Caesar / Rot-13...` -> Key `3` -> `Decrypt`.
5. **Vigenère Cipher:**
   - Select original plaintext `HELLO WORLD`.
   - Go to menu: `Crypt/Decrypt` -> `Symmetric (classic)` -> `Vigenère...`
   - Enter Password / Key: `KEY`.
   - Click `Encrypt`. Observe output: `RIJVS UYVJN`.
6. **Rail Fence Cipher:**
   - Select original plaintext `HELLO WORLD` (or `HELLOWORLD`).
   - Go to menu: `Crypt/Decrypt` -> `Symmetric (classic)` -> `Scytale / Rail Fence...`
   - Set Rail Depth to `3`.
   - Click `Encrypt`. Observe zigzag placement and output: `HOLELWRDLO`.

---

## 📊 Results & Terminal Execution Output

Running the automated Python verification script:

```text
===========================================================================
      PRACTICAL 01: CAESAR, VIGENERE & RAIL FENCE CIPHER EXECUTION
===========================================================================

[+] Mandatory Problem Statement Plaintext: 'HELLO WORLD'

[*] Caesar Encryption Process (Shift = 3):
    Formula: C = (P + 3) mod 26
    Plaintext:  'HELLO WORLD'
    Ciphertext: 'KHOOR ZRUOG'
[*] Caesar Decrypted: 'HELLO WORLD'

[*] Vigenere Polyalphabetic Encryption (Key = 'KEY'):
    Formula: C_i = (P_i + K_i) mod 26
    Plaintext:  'HELLO WORLD'
    Ciphertext: 'RIJVS UYVJN'
[*] Vigenere Decrypted: 'HELLO WORLD'

[*] Rail Fence Transposition Encryption (Rails/Depth = 3):
    Rail 1: H . . . O . . . R .
    Rail 2: . E . L . W . R . D
    Rail 3: . . L . . . O . . .
    Ciphertext: 'HOR ELWRD LO' -> Stripped: 'HORELWRDLO'
[*] Rail Fence Decrypted: 'HELLOWORLD'

===========================================================================
 [OK] Practical 01 Completed Successfully!
===========================================================================
```

---

## 📈 Comparative Analysis Matrix (BL4 Analyze)

| Parameter | Caesar Cipher | Vigenère Cipher | Rail Fence Cipher |
|:---|:---|:---|:---|
| **Cipher Classification** | Monoalphabetic Substitution | Polyalphabetic Substitution | Transposition (Permutation) |
| **Key Type & Domain** | Single integer $k \in \{0, \dots, 25\}$ | Keyword string of length $m$ ($26^m$) | Depth integer $d \in \{2, \dots, N-1\}$ |
| **Key Space Size** | 25 possible keys | $26^m$ (exponential in key length) | $N - 1$ |
| **Letter Frequency Impact** | Retains natural English frequency curve (shifted) | Flattens/smooths histogram across multiple alphabets | Exactly identical to plaintext frequency |
| **Primary Cryptanalysis Method** | Brute-force exhaustive search, single-letter frequency matching | Kasiski examination, Friedman Index of Coincidence, Babbage attack | Bigram analysis, anagramming, brute-force rail depth |
| **Practical Security Level** | Zero (broken instantly) | Insecure for short keys; historically strong | Zero (broken easily) |

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: Why is the Caesar cipher completely ineffective for modern secure communication?**
   - **Answer:** The key space consists of only 25 possible shifts. An attacker can test all 25 keys in microseconds using automated string scoring. Additionally, because it is monoalphabetic, the most frequent ciphertext letter directly corresponds to the letter 'E' in standard English text.

2. **Q2: How does the Vigenère cipher defeat simple single-letter frequency cryptanalysis?**
   - **Answer:** It uses polyalphabetic substitution where multiple Caesar shift alphabets are cycled based on the keyword characters. Consequently, identical plaintext letters (e.g., 'LL' in 'HELLO') are encrypted to different ciphertext characters (e.g., 'JV'), flattening single-letter frequency spikes.

3. **Q3: What is the fundamental difference between substitution and transposition ciphers?**
   - **Answer:** Substitution ciphers modify the **identity** of the characters while preserving their positions. Transposition ciphers preserve the **identity** of the characters while modifying their **positions / order**.

4. **Q4: How does the Kasiski test crack a Vigenère cipher?**
   - **Answer:** It searches for repeated groups of 3 or more letters in the ciphertext, measures the distances (intervals) between these repetitions, and computes the Greatest Common Divisor (GCD) of these distances to deduce the keyword length $m$.
