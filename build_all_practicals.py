# -*- coding: utf-8 -*-
"""
Production-grade builder for all 16 experiments of Cryptography (CSL0509) Lab Activity.
Aligned with ABCA Activity Document guidelines.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def save_file(rel_path, content):
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[+] Written: {rel_path}")

print("Preparing practical assets generation...")
