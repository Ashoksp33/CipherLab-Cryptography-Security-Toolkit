"""Caesar Cipher implementation.

The Caesar cipher is a substitution cipher where each letter in the plaintext
is shifted a fixed number of positions down the alphabet.
"""

from typing import List, Tuple


def encrypt(text: str, key: int) -> str:
    """Encrypt plaintext using Caesar cipher with given shift key.

    Args:
        text: Plaintext string to encrypt.
        key: Shift value (integer of any size).

    Returns:
        Encrypted ciphertext string.

    Raises:
        ValueError: If text is empty or key is not an integer.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")
    if not isinstance(key, int):
        raise ValueError("Caesar key must be an integer.")

    # Normalize shift key within 0 to 25
    shift = key % 26
    result = []

    for char in text:
        if char.isupper():
            # Shift uppercase characters (A-Z: ASCII 65-90)
            shifted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result.append(shifted)
        elif char.islower():
            # Shift lowercase characters (a-z: ASCII 97-122)
            shifted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            result.append(shifted)
        else:
            # Leave punctuation, digits, spaces unchanged
            result.append(char)

    return "".join(result)


def decrypt(text: str, key: int) -> str:
    """Decrypt ciphertext using Caesar cipher with given shift key.

    Decryption is equivalent to encryption with negative shift (-key).

    Args:
        text: Ciphertext string to decrypt.
        key: Shift value used during encryption.

    Returns:
        Decrypted plaintext string.

    Raises:
        ValueError: If text is empty or key is not an integer.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")
    if not isinstance(key, int):
        raise ValueError("Caesar key must be an integer.")

    return encrypt(text, -key)


def brute_force(ciphertext: str) -> List[Tuple[int, str]]:
    """Generate all 25 possible shifts to crack Caesar ciphertext.

    Args:
        ciphertext: Ciphertext string to analyze.

    Returns:
        List of tuples: (shift_value, decrypted_candidate_text).

    Raises:
        ValueError: If ciphertext is empty.
    """
    if not ciphertext:
        raise ValueError("Input ciphertext cannot be empty.")

    candidates: List[Tuple[int, str]] = []
    # Test every shift from 1 to 25
    for shift in range(1, 26):
        candidate = decrypt(ciphertext, shift)
        candidates.append((shift, candidate))

    return candidates
