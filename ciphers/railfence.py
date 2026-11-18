"""Rail Fence (Zig-Zag) Cipher implementation.

The Rail Fence cipher is a transposition cipher that writes plaintext in a zig-zag
pattern across a specified number of lines (rails) and then reads them off line by line.
"""

from typing import List


def _validate_rails(text: str, rails: int) -> None:
    """Validate text and number of rails."""
    if not text:
        raise ValueError("Input text cannot be empty.")
    if not isinstance(rails, int):
        raise ValueError("Number of rails must be an integer.")
    if rails < 2 or rails >= len(text):
        raise ValueError(
            f"Number of rails must be >= 2 and < text length ({len(text)}). Got {rails}."
        )


def get_grid(text: str, rails: int) -> List[List[str]]:
    """Generate the 2D zig-zag grid of characters for visualization.

    Args:
        text: Input string.
        rails: Number of rails.

    Returns:
        2D list where grid[r][c] is the character at rail r, column c,
        or a space ' ' if no character is at that position.

    Raises:
        ValueError: If text or rails is invalid.
    """
    _validate_rails(text, rails)

    grid = [[" " for _ in range(len(text))] for _ in range(rails)]
    rail = 0
    direction_down = False

    for col, char in enumerate(text):
        grid[rail][col] = char
        # Reverse direction when hitting top or bottom rail
        if rail == 0 or rail == rails - 1:
            direction_down = not direction_down
        rail += 1 if direction_down else -1

    return grid


def encrypt(text: str, key: int) -> str:
    """Encrypt plaintext using Rail Fence transposition cipher.

    Args:
        text: Plaintext string to encrypt.
        key: Number of rails (integer >= 2 and < len(text)).

    Returns:
        Ciphertext string.

    Raises:
        ValueError: If text or key is invalid.
    """
    _validate_rails(text, key)

    rails: List[List[str]] = [[] for _ in range(key)]
    rail = 0
    direction_down = False

    for char in text:
        rails[rail].append(char)
        if rail == 0 or rail == key - 1:
            direction_down = not direction_down
        rail += 1 if direction_down else -1

    # Concatenate rows
    return "".join("".join(row) for row in rails)


def decrypt(text: str, key: int) -> str:
    """Decrypt ciphertext using Rail Fence transposition cipher.

    Args:
        text: Ciphertext string to decrypt.
        key: Number of rails used during encryption.

    Returns:
        Decrypted plaintext string.

    Raises:
        ValueError: If text or key is invalid.
    """
    _validate_rails(text, key)

    n = len(text)
    # Step 1: Mark the zig-zag positions with a placeholder '*'
    grid = [["" for _ in range(n)] for _ in range(key)]
    rail = 0
    direction_down = False

    for col in range(n):
        grid[rail][col] = "*"
        if rail == 0 or rail == key - 1:
            direction_down = not direction_down
        rail += 1 if direction_down else -1

    # Step 2: Fill the marked positions row by row with ciphertext characters
    text_idx = 0
    for r in range(key):
        for c in range(n):
            if grid[r][c] == "*" and text_idx < n:
                grid[r][c] = text[text_idx]
                text_idx += 1

    # Step 3: Read characters following the zig-zag path
    result = []
    rail = 0
    direction_down = False

    for col in range(n):
        result.append(grid[rail][col])
        if rail == 0 or rail == key - 1:
            direction_down = not direction_down
        rail += 1 if direction_down else -1

    return "".join(result)
