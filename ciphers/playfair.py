"""Playfair Cipher implementation.

The Playfair cipher is a manual symmetric encryption technique that encrypts
digraphs (pairs of letters) instead of single letters, using a 5x5 matrix
of letters constructed from a secret keyword.
"""

from typing import Dict, List, Tuple


def generate_matrix(key: str) -> List[List[str]]:
    """Generate a 5x5 Playfair key matrix from a given keyword.

    'J' is replaced with 'I'. Duplicate letters are discarded while preserving order.
    The remaining alphabet letters (excluding 'J') fill the rest of the matrix.

    Args:
        key: Secret keyword string.

    Returns:
        5x5 list of lists containing uppercase alphabet letters.

    Raises:
        ValueError: If key is empty or has no alphabetic characters.
    """
    if not key or not isinstance(key, str):
        raise ValueError("Key must be a non-empty string.")

    cleaned_key = "".join([c.upper() for c in key if c.isalpha()]).replace('J', 'I')
    if not cleaned_key:
        raise ValueError("Playfair key must contain at least one alphabetic character.")

    seen = set()
    matrix_letters: List[str] = []

    # Insert unique characters from keyword
    for char in cleaned_key:
        if char not in seen:
            seen.add(char)
            matrix_letters.append(char)

    # Fill remainder with alphabet (A-Z, skipping J)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in seen:
            seen.add(char)
            matrix_letters.append(char)

    # Reshape into 5x5 grid
    matrix = [matrix_letters[i * 5:(i + 1) * 5] for i in range(5)]
    return matrix


def _build_char_positions(matrix: List[List[str]]) -> Dict[str, Tuple[int, int]]:
    """Create a mapping from letter to its (row, column) position in the matrix."""
    pos = {}
    for r in range(5):
        for c in range(5):
            pos[matrix[r][c]] = (r, c)
    return pos


def normalize_text(text: str) -> str:
    """Normalize input text for Playfair encryption.

    Converts to uppercase, replaces 'J' with 'I', removes non-letters,
    inserts 'X' between repeated letters in a pair, and pads odd length with 'X'.

    Args:
        text: Raw plaintext string.

    Returns:
        Normalized string grouped into pairs.

    Raises:
        ValueError: If text contains no letters.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text cannot be empty.")

    filtered = [c.upper() for c in text if c.isalpha()]
    if not filtered:
        raise ValueError("Input text must contain at least one alphabetic letter.")

    # Replace 'J' with 'I'
    filtered = ['I' if c == 'J' else c for c in filtered]

    # Form digraphs, inserting 'X' (or 'Q' if char is 'X') between identical letters in a pair
    pairs: List[str] = []
    i = 0
    n = len(filtered)
    while i < n:
        c1 = filtered[i]
        if i + 1 < n:
            c2 = filtered[i + 1]
            if c1 == c2:
                # Repeated letter in a pair: insert filler
                filler = 'Q' if c1 == 'X' else 'X'
                pairs.append(c1 + filler)
                i += 1
            else:
                pairs.append(c1 + c2)
                i += 2
        else:
            # Odd trailing character: pad with 'X' (or 'Q' if c1 is 'X')
            filler = 'Q' if c1 == 'X' else 'X'
            pairs.append(c1 + filler)
            i += 1

    return "".join(pairs)


def encrypt(text: str, key: str) -> str:
    """Encrypt plaintext using Playfair cipher.

    Args:
        text: Plaintext string to encrypt.
        key: Keyword to build the 5x5 key matrix.

    Returns:
        Ciphertext string (uppercase digraphs).

    Raises:
        ValueError: If text or key is invalid.
    """
    matrix = generate_matrix(key)
    pos = _build_char_positions(matrix)
    normalized = normalize_text(text)

    ciphertext_chars: List[str] = []
    for i in range(0, len(normalized), 2):
        c1, c2 = normalized[i], normalized[i + 1]
        r1, col1 = pos[c1]
        r2, col2 = pos[c2]

        if r1 == r2:
            # Same row: shift right circularly
            ciphertext_chars.append(matrix[r1][(col1 + 1) % 5])
            ciphertext_chars.append(matrix[r2][(col2 + 1) % 5])
        elif col1 == col2:
            # Same column: shift down circularly
            ciphertext_chars.append(matrix[(r1 + 1) % 5][col1])
            ciphertext_chars.append(matrix[(r2 + 1) % 5][col2])
        else:
            # Rectangle: swap columns
            ciphertext_chars.append(matrix[r1][col2])
            ciphertext_chars.append(matrix[r2][col1])

    return "".join(ciphertext_chars)


def decrypt(text: str, key: str) -> str:
    """Decrypt ciphertext using Playfair cipher.

    NOTE (Documented Limitation):
    Decryption returns the NORMALIZED plaintext (uppercase, 'J' replaced with 'I',
    non-alphabetic characters removed, and with padding/separation 'X' or 'Q' characters).
    This is an inherent property of the classical Playfair algorithm.

    Args:
        text: Ciphertext string (must have an even length of alphabetic characters).
        key: Keyword used for encryption.

    Returns:
        Normalized plaintext string.

    Raises:
        ValueError: If text or key is invalid.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input ciphertext cannot be empty.")

    filtered = "".join([c.upper() for c in text if c.isalpha()])
    if not filtered:
        raise ValueError("Ciphertext must contain alphabetic characters.")
    if len(filtered) % 2 != 0:
        raise ValueError("Playfair ciphertext must have an even number of characters.")

    matrix = generate_matrix(key)
    pos = _build_char_positions(matrix)

    plaintext_chars: List[str] = []
    for i in range(0, len(filtered), 2):
        c1, c2 = filtered[i], filtered[i + 1]
        if c1 not in pos or c2 not in pos:
            # Should not happen since all A-Z except J are in pos, and J can be replaced with I
            c1 = 'I' if c1 == 'J' else c1
            c2 = 'I' if c2 == 'J' else c2

        r1, col1 = pos[c1]
        r2, col2 = pos[c2]

        if r1 == r2:
            # Same row: shift left circularly
            plaintext_chars.append(matrix[r1][(col1 - 1) % 5])
            plaintext_chars.append(matrix[r2][(col2 - 1) % 5])
        elif col1 == col2:
            # Same column: shift up circularly
            plaintext_chars.append(matrix[(r1 - 1) % 5][col1])
            plaintext_chars.append(matrix[(r2 - 1) % 5][col2])
        else:
            # Rectangle: swap columns
            plaintext_chars.append(matrix[r1][col2])
            plaintext_chars.append(matrix[r2][col1])

    return "".join(plaintext_chars)
