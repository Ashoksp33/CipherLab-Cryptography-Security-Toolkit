"""Affine Cipher implementation.

The Affine cipher is a type of monoalphabetic substitution cipher, wherein each letter
in an alphabet is mapped to its numeric equivalent, encrypted using a simple
mathematical function: E(x) = (a*x + b) mod m, and decrypted using:
D(x) = a^(-1) * (x - b) mod m, where m is the alphabet size (26).
"""

import math
from typing import Tuple


def _validate_inputs(text: str, key: Tuple[int, int]) -> Tuple[int, int]:
    """Validate text and affine cipher key pair (a, b)."""
    if not text:
        raise ValueError("Input text cannot be empty.")
    if not isinstance(key, (tuple, list)) or len(key) != 2:
        raise ValueError("Affine cipher key must be a tuple/pair of two integers: (a, b).")

    a, b = key
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Keys 'a' and 'b' must both be integers.")

    # 'a' and 26 must be coprime (gcd(a, 26) == 1) for modular inverse to exist
    if math.gcd(a % 26, 26) != 1:
        raise ValueError(
            f"Key 'a' ({a}) is not coprime with 26 (gcd={math.gcd(a % 26, 26)}). "
            "Valid values for 'a' include 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25."
        )

    return a % 26, b % 26


def encrypt(text: str, key: Tuple[int, int]) -> str:
    """Encrypt plaintext using Affine cipher: E(x) = (a*x + b) mod 26.

    Preserves case and non-alphabetic characters.

    Args:
        text: Plaintext string.
        key: Tuple of integers (a, b) where gcd(a, 26) == 1.

    Returns:
        Ciphertext string.

    Raises:
        ValueError: If text is empty or key is invalid.
    """
    a, b = _validate_inputs(text, key)
    result = []

    for char in text:
        if char.isupper():
            x = ord(char) - ord('A')
            enc_x = (a * x + b) % 26
            result.append(chr(enc_x + ord('A')))
        elif char.islower():
            x = ord(char) - ord('a')
            enc_x = (a * x + b) % 26
            result.append(chr(enc_x + ord('a')))
        else:
            result.append(char)

    return "".join(result)


def decrypt(text: str, key: Tuple[int, int]) -> str:
    """Decrypt ciphertext using Affine cipher: D(x) = a^(-1) * (x - b) mod 26.

    Preserves case and non-alphabetic characters.

    Args:
        text: Ciphertext string.
        key: Tuple of integers (a, b) where gcd(a, 26) == 1.

    Returns:
        Decrypted plaintext string.

    Raises:
        ValueError: If text is empty or key is invalid.
    """
    a, b = _validate_inputs(text, key)
    # Modular multiplicative inverse of 'a' modulo 26
    a_inv = pow(a, -1, 26)
    result = []

    for char in text:
        if char.isupper():
            y = ord(char) - ord('A')
            dec_y = (a_inv * (y - b)) % 26
            result.append(chr(dec_y + ord('A')))
        elif char.islower():
            y = ord(char) - ord('a')
            dec_y = (a_inv * (y - b)) % 26
            result.append(chr(dec_y + ord('a')))
        else:
            result.append(char)

    return "".join(result)
