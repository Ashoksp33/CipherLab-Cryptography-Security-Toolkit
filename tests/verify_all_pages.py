"""Automated Verification of All CipherLab Functions and Edge Cases.

Simulates all user interactions across all 8 pages:
- Valid and invalid inputs
- Empty fields
- Wrong AES passwords & corrupted tokens
- Invalid keys across all classical ciphers
- Bad hashes and mismatched sizes
- RSA keygen, encryption, decryption, signatures, and size boundaries
"""

import hashlib
import io
import os
import sys

# Ensure root directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from ciphers import (
    aes_tool,
    affine,
    analysis,
    atbash,
    caesar,
    hashing,
    password_tools,
    playfair,
    railfence,
    rsa_tool,
    vigenere,
)


def test_all_pages_edge_cases():
    print("[1/8] Verifying Classical Ciphers Edge Cases...")
    # Caesar
    assert caesar.encrypt("INS 2026!", 3) == "LQV 2026!"
    assert caesar.decrypt("LQV 2026!", 3) == "INS 2026!"
    with pytest.raises(ValueError):
        caesar.encrypt("", 3)

    # Vigenere
    assert vigenere.encrypt("INS TEST", "KEY") == "SRQ DIQD"
    assert vigenere.decrypt("SRQ DIQD", "KEY") == "INS TEST"
    with pytest.raises(ValueError):
        vigenere.encrypt("Valid", "BAD KEY 123")
    with pytest.raises(ValueError):
        vigenere.encrypt("Valid", "")

    # Playfair
    enc_pf = playfair.encrypt("SECRET", "MONARCHY")
    dec_pf = playfair.decrypt(enc_pf, "MONARCHY")
    assert dec_pf == playfair.normalize_text("SECRET")
    with pytest.raises(ValueError):
        playfair.encrypt("", "KEY")
    with pytest.raises(ValueError):
        playfair.decrypt("ODD", "KEY")

    # Rail Fence
    assert railfence.decrypt(railfence.encrypt("RAILFENCETEST", 3), 3) == "RAILFENCETEST"
    with pytest.raises(ValueError):
        railfence.encrypt("HELLO", 1)
    with pytest.raises(ValueError):
        railfence.encrypt("HELLO", 5)

    # Affine
    assert affine.decrypt(affine.encrypt("AFFINE", (5, 8)), (5, 8)) == "AFFINE"
    with pytest.raises(ValueError):
        affine.encrypt("TEST", (2, 5))

    # Atbash
    assert atbash.decrypt(atbash.encrypt("ATBASH")) == "ATBASH"
    with pytest.raises(ValueError):
        atbash.encrypt("")

    print("[2/8] Verifying AES-256-GCM Edge Cases...")
    token = aes_tool.encrypt_text("Confidential message", "P@ssw0rd99")
    assert aes_tool.decrypt_text(token, "P@ssw0rd99") == "Confidential message"
    # Wrong password
    with pytest.raises(ValueError, match="Decryption failed"):
        aes_tool.decrypt_text(token, "WrongPass")
    # Tampered token
    with pytest.raises(ValueError, match="Decryption failed"):
        aes_tool.decrypt_text("tampered_corrupted_base64_data_here", "P@ssw0rd99")
    # Empty fields
    with pytest.raises(ValueError):
        aes_tool.encrypt_text("", "P@ss")
    with pytest.raises(ValueError):
        aes_tool.encrypt_text("Valid", "")

    # File bytes test
    raw_file = b"Sample byte content for testing"
    enc_file = aes_tool.encrypt_bytes(raw_file, "FilePass123")
    assert aes_tool.decrypt_bytes(enc_file, "FilePass123") == raw_file

    print("[3/8] Verifying RSA-2048 & Signatures Edge Cases...")
    priv, pub = rsa_tool.generate_key_pair()
    msg = "Short message for RSA"
    rsa_ct = rsa_tool.encrypt(msg, pub)
    assert rsa_tool.decrypt(rsa_ct, priv) == msg
    # Exceeding 190 bytes limit
    with pytest.raises(ValueError, match="exceeds the maximum limit"):
        rsa_tool.encrypt("X" * 195, pub)
    # Digital signature
    sig = rsa_tool.sign("Official Contract", priv)
    assert rsa_tool.verify("Official Contract", sig, pub) is True
    assert rsa_tool.verify("Forged Contract", sig, pub) is False
    assert rsa_tool.verify("Official Contract", "invalid_sig", pub) is False

    print("[4/8] Verifying Hashing & HMAC Edge Cases...")
    assert len(hashing.hash_text("test", "SHA-256")) == 64
    assert len(hashing.hash_text("test", "MD5")) == 32
    assert len(hashing.hash_text("test", "SHA-1")) == 40
    assert len(hashing.hash_text("test", "SHA-512")) == 128
    with pytest.raises(ValueError):
        hashing.hash_text("test", "INVALID_ALGO")

    hmac_val = hashing.generate_hmac("msg", "key")
    assert hashing.verify_hmac("msg", "key", hmac_val) is True
    assert hashing.verify_hmac("msg", "wrong", hmac_val) is False

    print("[5/8] Verifying File Integrity Checker Edge Cases...")
    file_bytes = io.BytesIO(b"Integrity verification test stream")
    expected_sha256 = hashlib.sha256(b"Integrity verification test stream").hexdigest()
    match, actual, algo = hashing.compare_hash(file_bytes, expected_sha256.upper())
    assert match is True
    assert algo == "SHA-256"

    # Bad hash length
    with pytest.raises(ValueError, match="Invalid hash length"):
        hashing.compare_hash(file_bytes, "12345")

    print("[6/8] Verifying Password Tools Edge Cases...")
    w_check = password_tools.check_password_strength("password")
    assert w_check["label"] == "Weak"
    assert w_check["common_match"] is True

    s_pwd = password_tools.generate_password(16)
    s_check = password_tools.check_password_strength(s_pwd)
    assert s_check["label"] in ["Strong", "Very Strong"]
    with pytest.raises(ValueError):
        password_tools.generate_password(4)  # < 8

    print("[7/8] Verifying Frequency Analysis Edge Cases...")
    freq = analysis.analyze_frequency("AAA BBB CC D")
    assert freq["total_letters"] == 9
    assert freq["letter_counts"]["A"] == 3
    assert len(freq["data_rows"]) == 26

    # Empty text
    empty_freq = analysis.analyze_frequency("")
    assert empty_freq["total_letters"] == 0

    print("[8/8] ALL MODULES AND EDGE CASES VERIFIED SUCCESSFULLY!")


if __name__ == "__main__":
    test_all_pages_edge_cases()
