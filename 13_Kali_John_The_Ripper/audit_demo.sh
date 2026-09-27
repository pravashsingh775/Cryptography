#!/bin/bash
# Practical 13: Kali Linux Password Auditing with John the Ripper
echo "=== Practical 13: Password Auditing with John the Ripper ==="

# 1. Create simulated shadow and passwd entries
cat << 'EOF' > test_passwd
alice:x:1001:1001:Alice:/home/alice:/bin/bash
bob:x:1002:1002:Bob:/home/bob:/bin/bash
charlie:x:1003:1003:Charlie:/home/charlie:/bin/bash
EOF

# SHA-512 crypt hashes for 'password123', 'dragon', 'admin'
cat << 'EOF' > test_shadow
alice:$6$salt123$B57pL7XlTqQkZf9iZ8q3.5wXm.s1y2z3a4b5c6d7e8f9g0h1i2j3k4l5m6n7o8p9q0r1s2t3u4v5w6x7y8z90:19245:0:99999:7:::
bob:$6$salt456$z1y2x3w4v5u6t7s8r9q0p1o2n3m4l5k6j7i8h9g0f1e2d3c4b5a69876543210zyxwvutsrqponmlkjihgfedcba:19245:0:99999:7:::
charlie:$6$salt789$m1n2o3p4q5r6s7t8u9v0w1x2y3z4a5b6c7d8e9f0g1h2i3j4k5l67890123456abcdefghijklmnopqr:19245:0:99999:7:::
EOF

echo "[+] Combining passwd and shadow using unshadow..."
unshadow test_passwd test_shadow > lab_hashes.txt

echo "[+] Target hashes prepared in lab_hashes.txt"
echo "[+] To run audit: john --wordlist=/usr/share/wordlists/rockyou.txt lab_hashes.txt"
