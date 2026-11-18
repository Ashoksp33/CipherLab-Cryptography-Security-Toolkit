# 🔐 CipherLab: Information & Network Security Cryptography Toolkit

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![pytest](https://img.shields.io/badge/tests-pytest-green.svg)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CipherLab is an interactive, modular cryptography toolkit and educational lab designed for an **Information and Network Security (INS)** mini project. It provides both historical classical ciphers and modern production-grade primitives (AES-256-GCM, RSA-2048, SHA-256/512, HMAC) with visual demonstrations, cryptanalysis tools, and robust integrity verification.

---

## 📖 Table of Contents
1. [Purpose & Problem Statement](#-purpose--problem-statement)
2. [Project Objectives](#-project-objectives)
3. [Features](#-features)
4. [Tech Stack](#-tech-stack)
5. [Folder Structure](#-folder-structure)
6. [Installation & Setup](#-installation--setup)
7. [Running the Application](#-running-the-application)
8. [Running Tests](#-running-tests)
9. [Mapping to the CIA Triad](#-mapping-to-the-cia-triad)
10. [Screenshots](#-screenshots)
11. [Security Notes](#-security-notes)
12. [Documented Limitations](#-documented-limitations)
13. [Future Scope](#-future-scope)

---

## 🎯 Purpose & Problem Statement
Understanding cryptographic concepts is often hindered by the disconnect between abstract mathematical theory (modular arithmetic, Galois fields, prime factor hardness) and practical, hands-on implementation. Students frequently face:
- Difficulty visualizing how classical substitution and transposition ciphers manipulate text and leak statistical patterns.
- Confusion regarding the differences between symmetric authenticated encryption (AEAD) and raw cipher block modes.
- Lack of clarity on digital signatures versus public-key encryption in asymmetric systems.
- Inefficient memory handling when hashing large files.

**CipherLab** bridges this gap by offering a clean, user-friendly, and interactive environment where students, educators, and security practitioners can encrypt, decrypt, sign, verify, and perform cryptanalysis with real-time feedback and zero tracebacks.

---

## 🚀 Project Objectives
- **Demonstrate Classical Cryptography**: Implement Caesar, Vigenère, Playfair, Rail Fence, Affine, and Atbash ciphers with visual grids, matrices, and brute-force cracking.
- **Implement Industry-Standard Modern Cryptography**: Provide robust implementations of **AES-256-GCM** with PBKDF2HMAC key derivation and **2048-bit RSA** with OAEP padding and PSS digital signatures.
- **Provide Cryptographic Integrity Tools**: Enable one-way cryptographic hashing (SHA-256, SHA-512, MD5, SHA-1) using 8 KB chunked streaming, automatic checksum matching, and keyed HMACs.
- **Educate on Cryptanalysis & Defenses**: Include password strength evaluation (Shannon entropy calculation) and letter frequency analysis to demonstrate why monoalphabetic ciphers are insecure.

---

## ✨ Features

### 1. Classical Ciphers
- **Caesar Cipher**: Modulo 26 shift, preserving case, digits, and punctuation. Features a full 25-shift brute-force cracking table.
- **Vigenère Cipher**: Polyalphabetic substitution using alphabetic keywords. The key advances only on letters.
- **Playfair Cipher**: 5x5 digraph key matrix (combining I and J). Normalizes text, handles repeating letter pairs with filler characters, and provides interactive 5x5 grid visualization.
- **Rail Fence Cipher**: Zig-zag transposition cipher across $k$ rails ($2 \le k < \text{len(text)}$) with full ASCII grid visualization.
- **Affine Cipher**: Modular arithmetic cipher $E(x) = (ax + b) \pmod{26}$, enforcing $\gcd(a, 26) = 1$.
- **Atbash Cipher**: Self-inverting mirror cipher (A ↔ Z, B ↔ Y).

### 2. Modern Symmetric Cryptography
- **AES-256-GCM**:
  - Key derivation using PBKDF2HMAC (SHA-256, 600,000 iterations, 16-byte cryptographically random salt).
  - 12-byte random nonce and 16-byte GCM authentication tag.
  - Text encryption/decryption and streaming file encryption/decryption (`.enc` format).
  - Clean `ValueError` handling for wrong passwords, corrupted data, or tampering.

### 3. Modern Asymmetric Cryptography
- **2048-bit RSA**:
  - Key pair generation with PEM serialization (unencrypted for academic demo).
  - RSA-OAEP encryption/decryption with SHA-256 and strict message size enforcement ($\le 190$ bytes).
  - RSA-PSS digital signature generation and verification.

### 4. Hashing & Message Authentication
- **Multi-Algorithm Hashing**: MD5, SHA-1, SHA-256, SHA-512 for strings and files.
- **Memory-Efficient File Hashing**: 8 KB buffer streaming prevents memory spikes when hashing large files.
- **Automated Integrity Checker**: Compares computed checksum against expected checksum, auto-detecting the algorithm by hash length (32, 40, 64, or 128 hex chars) while ignoring whitespace and case.
- **HMAC-SHA256**: Keyed-hash generation and constant-time timing-safe verification.

### 5. Password & Cryptanalysis Tools
- **Password Strength Analyzer**: Calculates Shannon entropy (bits), evaluates character diversity, checks against common password dictionaries, and provides actionable improvement tips.
- **CSPRNG Password Generator**: Generates cryptographically secure passwords using Python's `secrets` module (length 8–64) with customizable character sets.
- **Frequency Analysis**: Computes letter counts and percentage distributions, comparing ciphertext against standard English letter frequencies to showcase classical cipher vulnerabilities.

---

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **Frontend / UI**: [Streamlit](https://streamlit.io/) (modern dark theme, responsive components)
- **Cryptography Engine**: [Python Cryptography Library (`cryptography`)](https://cryptography.io/)
- **Data & Visualizations**: [Pandas](https://pandas.pydata.org/)
- **Testing**: [pytest](https://pytest.org/)
- **Code Quality**: [pyflakes](https://pypi.org/project/pyflakes/)

---

## 📂 Folder Structure
```text
cipherlab/
├── app.py                     # Streamlit multi-page interactive application
├── ciphers/                   # Core cryptographic implementations
│   ├── __init__.py
│   ├── caesar.py              # Caesar cipher & brute force engine
│   ├── vigenere.py            # Vigenère polyalphabetic cipher
│   ├── playfair.py            # Playfair 5x5 digraph cipher & matrix generator
│   ├── railfence.py           # Rail Fence zig-zag cipher & grid generator
│   ├── affine.py              # Affine modular arithmetic cipher
│   ├── atbash.py              # Atbash self-inverting cipher
│   ├── aes_tool.py            # AES-256-GCM + PBKDF2HMAC (text & file)
│   ├── rsa_tool.py            # 2048-bit RSA (OAEP + PSS digital signatures)
│   ├── hashing.py             # MD5, SHA-1, SHA-256, SHA-512, HMAC, file streaming
│   ├── password_tools.py      # Entropy analyzer & CSPRNG generator
│   └── analysis.py            # Letter frequency cryptanalysis engine
├── tests/                     # Automated unit test suite
│   ├── __init__.py
│   └── test_ciphers.py        # 33 comprehensive unit tests
├── requirements.txt           # Pinned dependencies
├── .gitignore                 # Git ignore rules
├── .streamlit/
│   └── config.toml            # Streamlit server and dark UI theme config
└── README.md                  # Project documentation & manual
```

---

## 📦 Installation & Setup

1. **Clone or navigate to the repository:**
   ```bash
   cd cipherlab
   ```

2. **Create a virtual environment (`.venv`):**
   - **Windows:**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install pinned dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Running the Application

Launch the Streamlit dashboard:
```bash
streamlit run app.py
```
Open your browser and navigate to:
👉 **`http://localhost:8501`**

---

## 🧪 Running Tests

Execute the complete pytest suite:
```bash
pytest -v
```

Run code quality / linter check:
```bash
python -m pyflakes app.py ciphers tests
```

---

## 🛡️ Mapping to the CIA Triad

| CIA Triad Pillar | Core Objective | CipherLab Module |
| :--- | :--- | :--- |
| **Confidentiality** | Protect data from unauthorized viewing | Caesar, Vigenère, Playfair, Rail Fence, Affine, Atbash, AES-256-GCM, RSA-OAEP |
| **Integrity** | Ensure data is not altered or tampered with | SHA-256, SHA-512, MD5, SHA-1, Chunked File Integrity Verification, HMAC-SHA256 |
| **Authenticity & Non-Repudiation** | Verify identity of sender and prevent denial of message | RSA-PSS Digital Signatures, HMAC-SHA256 |

---

## 📸 Screenshots

*(Placeholders for lab report and presentation figures)*

| Feature | Screenshot Preview |
| :--- | :--- |
| **Home & CIA Triad** | `[Screenshot: Home Page with CIA Triad & Architecture]` |
| **Classical Ciphers & Matrices** | `[Screenshot: Playfair 5x5 Matrix & Rail Fence Grid]` |
| **AES-256-GCM File Encryption** | `[Screenshot: AES File Encryption (.enc download)]` |
| **RSA Keygen & Signatures** | `[Screenshot: 2048-bit RSA Keypair & Signature Verification]` |
| **File Integrity Verification** | `[Screenshot: Hash Matching Green / Red Alert]` |
| **Frequency Analysis Bar Chart** | `[Screenshot: Ciphertext Frequency vs. Standard English]` |

---

## ⚠️ Security Notes

1. **Educational Use Only**: This software is designed for academic study, classroom demonstration, and Information & Network Security coursework.
2. **Broken Algorithms**: **MD5** and **SHA-1** are cryptographically broken due to documented collision attacks (e.g., Flame malware, SHAttered). They are provided solely for historical study and legacy checksum comparisons.
3. **Classical Ciphers Insecurity**: All classical substitution and transposition ciphers are easily broken using frequency analysis or small keyspace brute forcing. Never use them to protect real-world secrets.
4. **Demo RSA Keys**: RSA private keys in the UI are exported unencrypted for demonstration and inspection. In production systems, private keys should always be encrypted with strong passphrases and stored in secure Key Management Systems (KMS) or Hardware Security Modules (HSMs).

---

## 📌 Documented Limitations

- **Playfair Cipher Normalization**: The Playfair cipher operates on uppercase alphabetic characters only, replaces 'J' with 'I', merges identical letters in a pair with filler characters ('X' or 'Q'), and pads odd-length messages. As an inherent algorithm characteristic, decryption recovers this **normalized plaintext**, not the original raw punctuation or casing.
- **RSA OAEP Message Size**: RSA-OAEP with SHA-256 and a 2048-bit modulus can encrypt messages up to 190 bytes ($256 - 2 \times 32 - 2 = 190$). Larger payloads must use hybrid encryption (AES key encrypted with RSA).

---

## 🔮 Future Scope
- **Steganography Tool**: LSB image steganography to conceal encrypted payloads within PNG/BMP images.
- **Diffie-Hellman Key Exchange Simulator**: Interactive visualization of ephemeral key exchange over an insecure channel with man-in-the-middle (MITM) attack demonstrations.
- **Secure End-to-End Chat Simulator**: Simulated dual-client encrypted messaging with forward secrecy.
- **Containerization**: Dockerfile and multi-stage container deployment for instant cloud deployment.
