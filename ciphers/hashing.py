"""Cryptographic Hashing and Integrity Verification Module.

Supports:
- MD5, SHA-1, SHA-256, SHA-512 algorithms for text and streaming files
- Memory-efficient 8 KB chunked file hashing
- Automated algorithm detection and hash comparison
- HMAC-SHA256 generation and timing-safe verification
"""

import hashlib
import hmac
from typing import BinaryIO, Dict, Tuple, Union

CHUNK_SIZE = 8192  # 8 KB chunks

SUPPORTED_ALGORITHMS = {
    "MD5": hashlib.md5,
    "SHA-1": hashlib.sha1,
    "SHA-256": hashlib.sha256,
    "SHA-512": hashlib.sha512,
}

HASH_LENGTHS: Dict[int, str] = {
    32: "MD5",
    40: "SHA-1",
    64: "SHA-256",
    128: "SHA-512",
}


def _get_hasher(algorithm: str):
    """Normalize algorithm name and return the corresponding hashlib constructor."""
    algo_key = algorithm.upper().strip()
    # Normalize common variations (e.g. SHA1 -> SHA-1, SHA256 -> SHA-256)
    if algo_key == "SHA1":
        algo_key = "SHA-1"
    elif algo_key == "SHA256":
        algo_key = "SHA-256"
    elif algo_key == "SHA512":
        algo_key = "SHA-512"

    if algo_key not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported algorithm '{algorithm}'. Supported: {list(SUPPORTED_ALGORITHMS.keys())}"
        )
    return SUPPORTED_ALGORITHMS[algo_key]()


def hash_text(text: str, algorithm: str = "SHA-256") -> str:
    """Calculate the cryptographic hash of a text string.

    Args:
        text: Plaintext string to hash.
        algorithm: One of 'MD5', 'SHA-1', 'SHA-256', 'SHA-512'.

    Returns:
        Hexadecimal hash digest string.

    Raises:
        ValueError: If algorithm is unsupported.
    """
    if text is None:
        raise ValueError("Input text cannot be None.")

    hasher = _get_hasher(algorithm)
    hasher.update(text.encode("utf-8"))
    return hasher.hexdigest().lower()


def hash_file(file_source: Union[str, BinaryIO], algorithm: str = "SHA-256") -> str:
    """Calculate hash of a file reading in 8 KB chunks to prevent memory exhaustion.

    Args:
        file_source: File path (str) or binary file-like object (e.g. UploadedFile).
        algorithm: One of 'MD5', 'SHA-1', 'SHA-256', 'SHA-512'.

    Returns:
        Hexadecimal hash digest string.

    Raises:
        ValueError: If file cannot be read or algorithm is unsupported.
    """
    hasher = _get_hasher(algorithm)

    if isinstance(file_source, str):
        # Open and stream from local file path
        with open(file_source, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)
    else:
        # File-like object (e.g., Streamlit UploadedFile or BytesIO)
        if hasattr(file_source, "seek"):
            file_source.seek(0)
        while chunk := file_source.read(CHUNK_SIZE):
            hasher.update(chunk)
        if hasattr(file_source, "seek"):
            file_source.seek(0)

    return hasher.hexdigest().lower()


def compare_hash(
    file_source: Union[str, BinaryIO],
    expected_hash: str,
) -> Tuple[bool, str, str]:
    """Compare a file's hash against an expected hash with automated algorithm detection.

    Trims whitespace and ignores case in expected_hash. Auto-detects algorithm based on length:
    32 hex chars -> MD5, 40 -> SHA-1, 64 -> SHA-256, 128 -> SHA-512.

    Args:
        file_source: File path or file-like object.
        expected_hash: Hexadecimal expected hash string.

    Returns:
        Tuple of (is_match: bool, actual_computed_hash: str, detected_algorithm: str).

    Raises:
        ValueError: If expected_hash length does not match any supported algorithm.
    """
    if not expected_hash:
        raise ValueError("Expected hash cannot be empty.")

    cleaned_expected = expected_hash.strip().lower()
    hash_len = len(cleaned_expected)

    if hash_len not in HASH_LENGTHS:
        raise ValueError(
            f"Invalid hash length ({hash_len} characters). "
            "Expected 32 (MD5), 40 (SHA-1), 64 (SHA-256), or 128 (SHA-512) hexadecimal characters."
        )

    detected_algo = HASH_LENGTHS[hash_len]
    actual_hash = hash_file(file_source, detected_algo)
    is_match = hmac.compare_digest(actual_hash, cleaned_expected)

    return is_match, actual_hash, detected_algo


def generate_hmac(message: Union[str, bytes], key: Union[str, bytes]) -> str:
    """Generate an HMAC-SHA256 authentication code.

    Args:
        message: Message text or bytes.
        key: Secret authentication key.

    Returns:
        Hexadecimal HMAC digest string.

    Raises:
        ValueError: If message or key is empty.
    """
    if not message:
        raise ValueError("Message cannot be empty.")
    if not key:
        raise ValueError("HMAC key cannot be empty.")

    msg_bytes = message.encode("utf-8") if isinstance(message, str) else message
    key_bytes = key.encode("utf-8") if isinstance(key, str) else key

    return hmac.new(key_bytes, msg_bytes, hashlib.sha256).hexdigest()


def verify_hmac(
    message: Union[str, bytes],
    key: Union[str, bytes],
    expected_hmac: str,
) -> bool:
    """Verify an HMAC-SHA256 authentication code using constant-time comparison.

    Args:
        message: Message text or bytes.
        key: Secret authentication key.
        expected_hmac: Provided HMAC hex string to verify against.

    Returns:
        True if HMAC matches; False otherwise.
    """
    if not message or not key or not expected_hmac:
        return False

    computed = generate_hmac(message, key)
    return hmac.compare_digest(computed.lower(), expected_hmac.strip().lower())
