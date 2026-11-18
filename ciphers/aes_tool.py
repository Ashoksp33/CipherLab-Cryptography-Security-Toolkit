"""AES-256-GCM Encryption and Decryption Tool.

Uses authenticated encryption (AES-256-GCM) with key derivation via PBKDF2HMAC
(SHA-256, 600,000 iterations).

Output format:
    base64(salt [16 bytes] + nonce [12 bytes] + ciphertext_with_auth_tag)
"""

import base64
import os
from typing import Union

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_SIZE = 16  # 128-bit salt
NONCE_SIZE = 12  # 96-bit standard nonce for GCM
KEY_SIZE = 32  # 256-bit AES key
PBKDF2_ITERATIONS = 600_000
MIN_PAYLOAD_SIZE = SALT_SIZE + NONCE_SIZE + 16  # Salt + Nonce + 16-byte GCM tag


def _derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit AES key from a password and salt using PBKDF2HMAC.

    Args:
        password: User-provided passphrase.
        salt: Cryptographically random 16-byte salt.

    Returns:
        32-byte derived symmetric key.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_bytes(data: bytes, password: str) -> bytes:
    """Encrypt raw bytes using AES-256-GCM with PBKDF2 key derivation.

    Args:
        data: Plaintext bytes to encrypt.
        password: Secret passphrase.

    Returns:
        Base64-encoded encrypted bytes containing salt, nonce, and ciphertext with tag.

    Raises:
        ValueError: If data or password is empty.
    """
    if not data:
        raise ValueError("Input data cannot be empty.")
    if not password:
        raise ValueError("Password cannot be empty.")

    # 1. Generate random 16-byte salt and 12-byte nonce
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)

    # 2. Derive 256-bit encryption key
    key = _derive_key(password, salt)

    # 3. Encrypt data with AES-256-GCM (automatically appends 16-byte tag)
    aesgcm = AESGCM(key)
    ciphertext_with_tag = aesgcm.encrypt(nonce, data, None)

    # 4. Concatenate salt + nonce + ciphertext_with_tag and base64-encode
    package = salt + nonce + ciphertext_with_tag
    return base64.b64encode(package)


def decrypt_bytes(token: Union[bytes, str], password: str) -> bytes:
    """Decrypt base64-encoded AES-256-GCM payload back to raw bytes.

    Args:
        token: Base64-encoded package (salt + nonce + ciphertext_with_tag).
        password: Secret passphrase used during encryption.

    Returns:
        Decrypted plaintext bytes.

    Raises:
        ValueError: If password is wrong, data is tampered, or inputs are invalid.
    """
    if not token:
        raise ValueError("Input encrypted data cannot be empty.")
    if not password:
        raise ValueError("Password cannot be empty.")

    try:
        # 1. Decode base64 package
        if isinstance(token, str):
            token_bytes = token.strip().encode("utf-8")
        else:
            token_bytes = token.strip()

        package = base64.b64decode(token_bytes, validate=True)
        if len(package) < MIN_PAYLOAD_SIZE:
            raise ValueError("Decryption failed: wrong password or corrupted data")

        # 2. Extract salt, nonce, and ciphertext with tag
        salt = package[:SALT_SIZE]
        nonce = package[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
        ciphertext_with_tag = package[SALT_SIZE + NONCE_SIZE:]

        # 3. Re-derive the key with extracted salt
        key = _derive_key(password, salt)

        # 4. Decrypt and verify tag with AES-256-GCM
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
        return plaintext

    except (InvalidTag, ValueError, Exception):
        # Never expose raw traceback to caller
        raise ValueError("Decryption failed: wrong password or corrupted data")


def encrypt_text(text: str, password: str) -> str:
    """Encrypt a plaintext string to a base64 ciphertext string.

    Args:
        text: Plaintext string.
        password: Secret passphrase.

    Returns:
        Base64-encoded ciphertext string.

    Raises:
        ValueError: If text or password is empty.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")
    if not password:
        raise ValueError("Password cannot be empty.")

    encrypted = encrypt_bytes(text.encode("utf-8"), password)
    return encrypted.decode("utf-8")


def decrypt_text(ciphertext: str, password: str) -> str:
    """Decrypt a base64 ciphertext string back to plaintext string.

    Args:
        ciphertext: Base64-encoded ciphertext string.
        password: Secret passphrase.

    Returns:
        Decrypted plaintext string.

    Raises:
        ValueError: If password is wrong or ciphertext is corrupted/tampered.
    """
    if not ciphertext:
        raise ValueError("Input ciphertext cannot be empty.")
    if not password:
        raise ValueError("Password cannot be empty.")

    decrypted_bytes = decrypt_bytes(ciphertext, password)
    try:
        return decrypted_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Decryption failed: wrong password or corrupted data")
