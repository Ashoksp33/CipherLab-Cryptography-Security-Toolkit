"""Atbash Cipher implementation.

The Atbash cipher is a monoalphabetic substitution cipher originally used for the
Hebrew alphabet. It maps each letter to its opposite counterpart in the alphabet
(A <-> Z, B <-> Y, etc.).
"""

from typing import Any


def encrypt(text: str, key: Any = None) -> str:
    """Encrypt plaintext using the Atbash cipher.

    Reverses the alphabet mapping (A->Z, B->Y, etc.). Preserves case and
    non-alphabetic characters.

    Args:
        text: Plaintext string to encrypt.
        key: Unused argument (accepted for API consistency across ciphers).

    Returns:
        Ciphertext string.

    Raises:
        ValueError: If text is empty.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")

    result = []
    for char in text:
        if char.isupper():
            # Mirror character around alphabet midpoint: ord('A') + ord('Z') - ord(char)
            result.append(chr(ord('Z') - (ord(char) - ord('A'))))
        elif char.islower():
            # Mirror lowercase: ord('a') + ord('z') - ord(char)
            result.append(chr(ord('z') - (ord(char) - ord('a'))))
        else:
            result.append(char)

    return "".join(result)


def decrypt(text: str, key: Any = None) -> str:
    """Decrypt ciphertext using the Atbash cipher.

    Atbash is self-reciprocal (symmetric involution), meaning encrypt and decrypt
    perform the exact same transformation.

    Args:
        text: Ciphertext string to decrypt.
        key: Unused argument.

    Returns:
        Decrypted plaintext string.

    Raises:
        ValueError: If text is empty.
    """
    return encrypt(text, key)
