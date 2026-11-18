"""Vigenere Cipher implementation.

The Vigenere cipher is a polyalphabetic substitution cipher that uses a repeated
keyword to determine variable Caesar shifts for each letter.
"""


def _validate_inputs(text: str, key: str) -> None:
    """Validate input text and key.

    Args:
        text: Plaintext or ciphertext.
        key: Alphabetic encryption key.

    Raises:
        ValueError: If text or key is empty or key contains non-alphabetic characters.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")
    if not key:
        raise ValueError("Key cannot be empty.")
    if not key.isalpha():
        raise ValueError("Vigenere key must contain only alphabetic characters (A-Z, a-z).")


def encrypt(text: str, key: str) -> str:
    """Encrypt plaintext using Vigenere cipher with given alphabetic key.

    Non-alphabetic characters (spaces, punctuation) are preserved unchanged,
    and the key pointer advances only when an alphabetic character is encrypted.

    Args:
        text: Plaintext string to encrypt.
        key: Alphabetic keyword.

    Returns:
        Encrypted ciphertext string.

    Raises:
        ValueError: If inputs are invalid.
    """
    _validate_inputs(text, key)

    key_upper = key.upper()
    key_len = len(key_upper)
    key_index = 0
    result = []

    for char in text:
        if char.isalpha():
            # Current shift amount derived from the matching key character
            shift = ord(key_upper[key_index % key_len]) - ord('A')

            if char.isupper():
                shifted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                result.append(shifted)
            else:
                shifted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                result.append(shifted)

            # Advance key only on alphabetic characters
            key_index += 1
        else:
            # Leave non-alphabetic character unchanged without advancing key
            result.append(char)

    return "".join(result)


def decrypt(text: str, key: str) -> str:
    """Decrypt ciphertext using Vigenere cipher with given alphabetic key.

    Args:
        text: Ciphertext string to decrypt.
        key: Alphabetic keyword used during encryption.

    Returns:
        Decrypted plaintext string.

    Raises:
        ValueError: If inputs are invalid.
    """
    _validate_inputs(text, key)

    key_upper = key.upper()
    key_len = len(key_upper)
    key_index = 0
    result = []

    for char in text:
        if char.isalpha():
            shift = ord(key_upper[key_index % key_len]) - ord('A')

            if char.isupper():
                shifted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                result.append(shifted)
            else:
                shifted = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                result.append(shifted)

            # Advance key only on alphabetic characters
            key_index += 1
        else:
            result.append(char)

    return "".join(result)
