"""Frequency Analysis Module for Cryptanalysis.

Used in Information and Network Security to demonstrate how monoalphabetic
and classical ciphers leak statistical patterns, rendering them vulnerable
to frequency analysis attacks.
"""

import string
from typing import Any, Dict, List

# Standard English letter frequencies (approximate percentages) for comparative cryptanalysis
ENGLISH_STANDARD_FREQ = {
    "E": 12.70, "T": 9.06, "A": 8.17, "O": 7.51, "I": 6.97, "N": 6.75,
    "S": 6.33, "H": 6.09, "R": 5.99, "D": 4.25, "L": 4.03, "C": 2.78,
    "U": 2.76, "M": 2.41, "W": 2.36, "F": 2.23, "G": 2.02, "Y": 1.97,
    "P": 1.93, "B": 1.49, "V": 0.98, "K": 0.77, "X": 0.15, "J": 0.15,
    "Q": 0.10, "Z": 0.07,
}


def analyze_frequency(text: str) -> Dict[str, Any]:
    """Calculate counts and percentages of letters (A-Z) in the given text.

    Args:
        text: Input text string (plaintext or ciphertext).

    Returns:
        Dictionary containing:
            - total_letters: Total count of alphabetic characters
            - letter_counts: Dict mapping uppercase letters A-Z to integer counts
            - letter_percentages: Dict mapping letters A-Z to rounded percentages
            - data_rows: List of dicts suitable for creating a pandas DataFrame
    """
    if not text:
        empty_counts = {c: 0 for c in string.ascii_uppercase}
        empty_pct = {c: 0.0 for c in string.ascii_uppercase}
        return {
            "total_letters": 0,
            "letter_counts": empty_counts,
            "letter_percentages": empty_pct,
            "data_rows": [
                {"Letter": c, "Count": 0, "Percentage": 0.0, "English Standard (%)": ENGLISH_STANDARD_FREQ.get(c, 0.0)}
                for c in string.ascii_uppercase
            ],
        }

    counts = {c: 0 for c in string.ascii_uppercase}
    total_letters = 0

    for char in text.upper():
        if char in counts:
            counts[char] += 1
            total_letters += 1

    percentages = {}
    data_rows: List[Dict[str, Any]] = []

    for char in string.ascii_uppercase:
        cnt = counts[char]
        pct = round((cnt / total_letters * 100), 2) if total_letters > 0 else 0.0
        percentages[char] = pct
        data_rows.append({
            "Letter": char,
            "Count": cnt,
            "Percentage": pct,
            "English Standard (%)": ENGLISH_STANDARD_FREQ.get(char, 0.0),
        })

    return {
        "total_letters": total_letters,
        "letter_counts": counts,
        "letter_percentages": percentages,
        "data_rows": data_rows,
    }
