"""Comprehensive Unit Test Suite for CipherLab.

Tests all classical ciphers, modern cryptography algorithms (AES-256-GCM, RSA, SHA/MD5),
file hashing integrity, password tools, and cryptanalysis functions.
"""

import hashlib
import io
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


# =====================================================================
# 1. CLASSICAL CIPHERS: CAESAR
# =====================================================================

def test_caesar_known_vector():
    """Verify Caesar cipher known vector: HELLO with shift 3 -> KHOOR."""
    assert caesar.encrypt("HELLO", 3) == "KHOOR"
    assert caesar.decrypt("KHOOR", 3) == "HELLO"


def test_caesar_roundtrip():
    """Verify Caesar round-trip encryption/decryption with various shifts."""
    text = "Information & Network Security 2026!"
    for shift in [0, 1, 13, 25, 52, -3]:
        encrypted = caesar.encrypt(text, shift)
        decrypted = caesar.decrypt(encrypted, shift)
        assert decrypted == text


def test_caesar_preserves_case_and_symbols():
    """Verify case, spaces, digits, and punctuation are preserved."""
    sample = "Hello, World! 123"
    enc = caesar.encrypt(sample, 4)
    assert enc == "Lipps, Asvph! 123"
    assert caesar.decrypt(enc, 4) == sample


def test_caesar_brute_force():
    """Verify brute_force returns 25 shifts and contains the plaintext."""
    plaintext = "SECRET"
    ciphertext = caesar.encrypt(plaintext, 7)
    candidates = caesar.brute_force(ciphertext)
    assert len(candidates) == 25
    decrypted_texts = [text for _, text in candidates]
    assert plaintext in decrypted_texts


def test_caesar_invalid_input():
    """Empty text or non-int key raises ValueError."""
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        caesar.encrypt("", 3)
    with pytest.raises(ValueError, match="must be an integer"):
        caesar.encrypt("Hello", "invalid")  # type: ignore


# =====================================================================
# 2. CLASSICAL CIPHERS: VIGENERE
# =====================================================================

def test_vigenere_known_vector():
    """Verify known vector: ATTACKATDAWN with LEMON -> LXFOPVEFRNHR."""
    assert vigenere.encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
    assert vigenere.decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"


def test_vigenere_roundtrip_preserves_case_punctuation():
    """Verify key advances ONLY on letters and case/punctuation is preserved."""
    original = "Hello, World! Cryptography 101."
    key = "cipher"
    encrypted = vigenere.encrypt(original, key)
    assert encrypted != original
    decrypted = vigenere.decrypt(encrypted, key)
    assert decrypted == original


def test_vigenere_invalid_inputs():
    """Empty text, empty key, or non-alphabetic key must raise ValueError."""
    with pytest.raises(ValueError):
        vigenere.encrypt("", "KEY")
    with pytest.raises(ValueError, match="Key cannot be empty"):
        vigenere.encrypt("Hello", "")
    with pytest.raises(ValueError, match="alphabetic characters"):
        vigenere.encrypt("Hello", "KEY123")
    with pytest.raises(ValueError, match="alphabetic characters"):
        vigenere.encrypt("Hello", "K E Y")


# =====================================================================
# 3. CLASSICAL CIPHERS: PLAYFAIR
# =====================================================================

def test_playfair_matrix_generation():
    """Verify 5x5 matrix generation, handling of J->I and duplicates."""
    matrix = playfair.generate_matrix("MONARCHY")
    assert len(matrix) == 5
    assert all(len(row) == 5 for row in matrix)
    # First row should be M, O, N, A, R
    assert matrix[0] == ["M", "O", "N", "A", "R"]
    # Total unique letters should be 25
    flat = [c for row in matrix for c in row]
    assert len(set(flat)) == 25
    assert "J" not in flat


def test_playfair_roundtrip_normalized():
    """Verify Playfair round-trip equals the normalized plaintext."""
    raw = "INSTRUMENT"
    key = "MONARCHY"
    normalized = playfair.normalize_text(raw)
    encrypted = playfair.encrypt(raw, key)
    decrypted = playfair.decrypt(encrypted, key)
    assert decrypted == normalized


def test_playfair_repeated_letters_handling():
    """Verify repeated letter in pair gets separated by X or Q."""
    normalized = playfair.normalize_text("BALLOON")
    # 'LL' should be separated: BA, LX, LO, ON
    assert normalized == "BALXLOON"


def test_playfair_invalid_inputs():
    """Empty text or empty key raises ValueError."""
    with pytest.raises(ValueError):
        playfair.encrypt("", "KEY")
    with pytest.raises(ValueError):
        playfair.encrypt("HELLO", "")
    with pytest.raises(ValueError, match="even number"):
        playfair.decrypt("ABC", "KEY")


# =====================================================================
# 4. CLASSICAL CIPHERS: RAIL FENCE
# =====================================================================

def test_railfence_roundtrip():
    """Verify Rail Fence round-trip encryption and decryption."""
    original = "DEFEND THE EAST WALL OF THE CASTLE"
    for rails in [2, 3, 5]:
        enc = railfence.encrypt(original, rails)
        dec = railfence.decrypt(enc, rails)
        assert dec == original


def test_railfence_grid_structure():
    """Verify Rail Fence visualization grid."""
    text = "HELLO"
    grid = railfence.get_grid(text, 3)
    assert len(grid) == 3
    assert len(grid[0]) == len(text)
    assert grid[0][0] == "H"
    assert grid[1][1] == "E"
    assert grid[2][2] == "L"
    assert grid[1][3] == "L"
    assert grid[0][4] == "O"


def test_railfence_invalid_keys():
    """Key < 2 or key >= len(text) must raise ValueError."""
    with pytest.raises(ValueError, match=">= 2 and < text length"):
        railfence.encrypt("HELLO", 1)
    with pytest.raises(ValueError, match=">= 2 and < text length"):
        railfence.encrypt("HELLO", 5)
    with pytest.raises(ValueError, match=">= 2 and < text length"):
        railfence.encrypt("HELLO", 10)


# =====================================================================
# 5. CLASSICAL CIPHERS: AFFINE
# =====================================================================

def test_affine_roundtrip():
    """Verify Affine cipher encryption and decryption."""
    text = "Affine Cipher Mini Project 2026!"
    key = (5, 8)  # gcd(5, 26) == 1
    enc = affine.encrypt(text, key)
    dec = affine.decrypt(enc, key)
    assert dec == text


def test_affine_invalid_keys():
    """If gcd(a, 26) != 1 (e.g., a=2, 4, 13), raise ValueError."""
    with pytest.raises(ValueError, match="not coprime"):
        affine.encrypt("HELLO", (2, 5))
    with pytest.raises(ValueError, match="not coprime"):
        affine.encrypt("HELLO", (13, 1))
    with pytest.raises(ValueError, match="must be a tuple/pair"):
        affine.encrypt("HELLO", 5)  # type: ignore


# =====================================================================
# 6. CLASSICAL CIPHERS: ATBASH
# =====================================================================

def test_atbash_roundtrip_and_mirroring():
    """Verify Atbash mirror: A->Z, B->Y, and self-reciprocal round-trip."""
    assert atbash.encrypt("ABC") == "ZYX"
    assert atbash.encrypt("Hello, World!") == "Svool, Dliow!"
    assert atbash.decrypt(atbash.encrypt("Information Security")) == "Information Security"


# =====================================================================
# 7. MODERN CRYPTOGRAPHY: AES-256-GCM
# =====================================================================

def test_aes_text_roundtrip():
    """Verify AES-256-GCM text encrypt and decrypt."""
    text = "Super secret project payload 🔐"
    password = "MasterPassword123!"
    token = aes_tool.encrypt_text(text, password)
    assert isinstance(token, str)
    decrypted = aes_tool.decrypt_text(token, password)
    assert decrypted == text


def test_aes_bytes_roundtrip():
    """Verify AES-256-GCM bytes encrypt and decrypt for file payloads."""
    binary_data = b"\x00\x01\x02\xFF\xFE\xFD" * 100
    password = "BinaryFileKey#99"
    encrypted = aes_tool.encrypt_bytes(binary_data, password)
    decrypted = aes_tool.decrypt_bytes(encrypted, password)
    assert decrypted == binary_data


def test_aes_wrong_password_raises_clean_error():
    """Wrong password must raise ValueError('Decryption failed: wrong password or corrupted data')."""
    token = aes_tool.encrypt_text("Confidential", "CorrectPassword")
    with pytest.raises(ValueError, match="Decryption failed: wrong password or corrupted data"):
        aes_tool.decrypt_text(token, "WrongPassword")


def test_aes_tampered_ciphertext_fails():
    """Tampering with ciphertext must raise clean ValueError."""
    import base64
    token = aes_tool.encrypt_text("Confidential", "Password123")
    raw = bytearray(base64.b64decode(token))
    # Flip the last byte (auth tag)
    raw[-1] ^= 0x01
    tampered_token = base64.b64encode(raw).decode("utf-8")
    with pytest.raises(ValueError, match="Decryption failed: wrong password or corrupted data"):
        aes_tool.decrypt_text(tampered_token, "Password123")


def test_aes_empty_inputs():
    """Empty password or text must raise ValueError."""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        aes_tool.encrypt_text("Test", "")
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        aes_tool.encrypt_text("", "Password")


# =====================================================================
# 8. MODERN CRYPTOGRAPHY: RSA & DIGITAL SIGNATURES
# =====================================================================

def test_rsa_roundtrip():
    """Verify RSA keygen, OAEP encryption and decryption."""
    priv_pem, pub_pem = rsa_tool.generate_key_pair()
    assert "BEGIN PRIVATE KEY" in priv_pem
    assert "BEGIN PUBLIC KEY" in pub_pem

    message = "Secret INS RSA Key Exchange"
    ciphertext = rsa_tool.encrypt(message, pub_pem)
    decrypted = rsa_tool.decrypt(ciphertext, priv_pem)
    assert decrypted == message


def test_rsa_message_size_limit():
    """Verify messages > 190 bytes raise friendly ValueError."""
    _, pub_pem = rsa_tool.generate_key_pair()
    oversized = "A" * 191
    with pytest.raises(ValueError, match="exceeds the maximum limit"):
        rsa_tool.encrypt(oversized, pub_pem)


def test_rsa_digital_signature_verification():
    """Verify digital signature passes for original, fails for modified message."""
    priv_pem, pub_pem = rsa_tool.generate_key_pair()
    doc = "Authorized transfer: $1,000,000 to Bob"
    sig = rsa_tool.sign(doc, priv_pem)

    # Valid signature
    assert rsa_tool.verify(doc, sig, pub_pem) is True

    # Tampered message
    tampered_doc = "Authorized transfer: $1,000,000 to Eve"
    assert rsa_tool.verify(tampered_doc, sig, pub_pem) is False

    # Corrupted signature
    assert rsa_tool.verify(doc, "bad_signature_data", pub_pem) is False


# =====================================================================
# 9. HASHING & INTEGRITY CHECKING
# =====================================================================

def test_hashing_known_vectors():
    """Verify SHA-256 and MD5 known test vectors."""
    sha256_known = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    md5_known = "900150983cd24fb0d6963f7d28e17f72"

    assert hashing.hash_text("abc", "SHA-256") == sha256_known
    assert hashing.hash_text("abc", "MD5") == md5_known


def test_chunked_file_hash_equals_oneshot():
    """Verify 8 KB chunked file hash matches one-shot hashlib digest for 50 KB data."""
    test_content = b"Cryptography and Network Security" * 1500
    expected = hashlib.sha256(test_content).hexdigest()

    file_stream = io.BytesIO(test_content)
    chunked_result = hashing.hash_file(file_stream, "SHA-256")
    assert chunked_result == expected


def test_compare_hash_auto_detect_and_whitespace():
    """Verify compare_hash auto-detects algo and ignores case/whitespace."""
    content = b"File integrity verification"
    correct_sha256 = hashlib.sha256(content).hexdigest()

    file_stream = io.BytesIO(content)
    match, actual, algo = hashing.compare_hash(
        file_stream,
        f"  {correct_sha256.upper()}  ",
    )
    assert match is True
    assert actual == correct_sha256
    assert algo == "SHA-256"

    # Mismatch check
    file_stream.seek(0)
    fake_sha256 = "0" * 64
    match, actual, algo = hashing.compare_hash(file_stream, fake_sha256)
    assert match is False
    assert actual == correct_sha256


def test_hmac_sha256():
    """Verify HMAC generation and constant-time verification."""
    msg = "Transaction ID: 987654"
    secret = "TopSecretHMACKey"
    code = hashing.generate_hmac(msg, secret)
    assert hashing.verify_hmac(msg, secret, code) is True
    assert hashing.verify_hmac("Altered Message", secret, code) is False
    assert hashing.verify_hmac(msg, "WrongKey", code) is False


# =====================================================================
# 10. PASSWORD TOOLS
# =====================================================================

def test_password_strength_common_and_strong():
    """Verify common weak password gets Weak, long random gets Strong."""
    weak_res = password_tools.check_password_strength("password")
    assert weak_res["label"] == "Weak"
    assert weak_res["common_match"] is True

    strong_pwd = password_tools.generate_password(20, True, True, True, True)
    strong_res = password_tools.check_password_strength(strong_pwd)
    assert strong_res["label"] in ["Strong", "Very Strong"]
    assert strong_res["entropy_bits"] > 70


def test_password_generator_constraints():
    """Verify generated password length and character pool requirements."""
    pwd = password_tools.generate_password(24, True, True, True, True)
    assert len(pwd) == 24
    assert any(c.isupper() for c in pwd)
    assert any(c.islower() for c in pwd)
    assert any(c.isdigit() for c in pwd)
    assert any(c in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" for c in pwd)


# =====================================================================
# 11. FREQUENCY ANALYSIS
# =====================================================================

def test_frequency_analysis():
    """Verify letter counts and percentages calculation."""
    text = "AAABBC"
    result = analysis.analyze_frequency(text)
    assert result["total_letters"] == 6
    assert result["letter_counts"]["A"] == 3
    assert result["letter_counts"]["B"] == 2
    assert result["letter_counts"]["C"] == 1
    assert result["letter_percentages"]["A"] == 50.0
    assert result["letter_percentages"]["B"] == 33.33
