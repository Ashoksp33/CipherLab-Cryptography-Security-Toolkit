"""Password Strength Evaluation and Cryptographically Secure Generator.

Features:
- Password strength scoring and Shannon entropy estimation
- Dictionary check against common weak passwords
- Actionable security improvement recommendations
- Secure random password generation using the `secrets` module
"""

import math
import secrets
import string
from typing import Any, Dict, List

COMMON_WEAK_PASSWORDS = {
    "password", "123456", "12345678", "123456789", "qwerty", "admin",
    "welcome", "login", "password123", "abc123", "iloveyou", "monkey",
    "dragon", "master", "football", "secret", "p@ssword", "letmein"
}


def check_password_strength(password: str) -> Dict[str, Any]:
    """Evaluate password strength, entropy, and common dictionary vulnerabilities.

    Args:
        password: The password string to evaluate.

    Returns:
        Dictionary with:
            - score: Integer from 0 (very weak) to 4 (very strong)
            - percentage: Integer 0 to 100 for progress bar display
            - label: 'Weak', 'Fair', 'Strong', or 'Very Strong'
            - entropy_bits: Estimated entropy in bits
            - common_match: Boolean indicating if found in common passwords
            - tips: List of recommendations to improve security
            - checks: Dict of boolean criteria (has_upper, has_lower, etc.)
    """
    if not password:
        return {
            "score": 0,
            "percentage": 0,
            "label": "Weak",
            "entropy_bits": 0.0,
            "common_match": False,
            "tips": ["Enter a password to evaluate."],
            "checks": {
                "length": False,
                "upper": False,
                "lower": False,
                "digits": False,
                "symbols": False,
            },
        }

    tips: List[str] = []
    checks = {
        "length": len(password) >= 12,
        "upper": any(c.isupper() for c in password),
        "lower": any(c.islower() for c in password),
        "digits": any(c.isdigit() for c in password),
        "symbols": any(c in string.punctuation for c in password),
    }

    # Pool size calculation for Shannon entropy: H = L * log2(R)
    pool_size = 0
    if checks["upper"]:
        pool_size += 26
    if checks["lower"]:
        pool_size += 26
    if checks["digits"]:
        pool_size += 10
    if checks["symbols"]:
        pool_size += len(string.punctuation)
    # Characters not in the above categories
    other_chars = sum(1 for c in password if not (c.isalnum() or c in string.punctuation))
    if other_chars > 0:
        pool_size += 32

    entropy_bits = round(len(password) * math.log2(pool_size), 1) if pool_size > 0 else 0.0

    # Common password check
    is_common = password.lower().strip() in COMMON_WEAK_PASSWORDS

    # Tips generation
    if len(password) < 12:
        tips.append(f"Increase length to at least 12 characters (currently {len(password)}).")
    if not checks["upper"]:
        tips.append("Add uppercase letters (A-Z).")
    if not checks["lower"]:
        tips.append("Add lowercase letters (a-z).")
    if not checks["digits"]:
        tips.append("Add numeric digits (0-9).")
    if not checks["symbols"]:
        tips.append("Add special symbols (!@#$%^&*...).")
    if is_common:
        tips.append("This is an extremely common, easily crackable password. Choose a unique phrase.")

    # Scoring logic
    if is_common or len(password) < 6:
        score = 0
        label = "Weak"
        percentage = 15
    else:
        passed_rules = sum(checks.values())
        if passed_rules <= 2 or entropy_bits < 35:
            score = 1
            label = "Weak"
            percentage = 30
        elif passed_rules == 3 or entropy_bits < 55:
            score = 2
            label = "Fair"
            percentage = 60
        elif passed_rules == 4 or entropy_bits < 75:
            score = 3
            label = "Strong"
            percentage = 85
        else:
            score = 4
            label = "Very Strong"
            percentage = 100

    return {
        "score": score,
        "percentage": percentage,
        "label": label,
        "entropy_bits": entropy_bits,
        "common_match": is_common,
        "tips": tips if tips else ["Great job! Your password meets all security criteria."],
        "checks": checks,
    }


def generate_password(
    length: int = 16,
    include_upper: bool = True,
    include_lower: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
) -> str:
    """Generate a cryptographically secure random password using secrets.

    Args:
        length: Desired length (8 to 64).
        include_upper: Include uppercase letters (A-Z).
        include_lower: Include lowercase letters (a-z).
        include_digits: Include digits (0-9).
        include_symbols: Include punctuation symbols.

    Returns:
        Generated password string.

    Raises:
        ValueError: If length is outside [8, 64] or no character sets are selected.
    """
    if length < 8 or length > 64:
        raise ValueError(f"Password length must be between 8 and 64 characters (got {length}).")

    char_pools: List[str] = []
    guaranteed: List[str] = []

    if include_upper:
        char_pools.append(string.ascii_uppercase)
        guaranteed.append(secrets.choice(string.ascii_uppercase))
    if include_lower:
        char_pools.append(string.ascii_lowercase)
        guaranteed.append(secrets.choice(string.ascii_lowercase))
    if include_digits:
        char_pools.append(string.digits)
        guaranteed.append(secrets.choice(string.digits))
    if include_symbols:
        char_pools.append(string.punctuation)
        guaranteed.append(secrets.choice(string.punctuation))

    if not char_pools:
        raise ValueError("At least one character set must be selected.")

    combined_chars = "".join(char_pools)
    remaining_length = length - len(guaranteed)

    # Fill remaining characters
    random_chars = [secrets.choice(combined_chars) for _ in range(remaining_length)]
    all_chars = guaranteed + random_chars

    # Cryptographically secure in-place shuffle
    # Using Fisher-Yates shuffle with secrets.randbelow
    for i in range(len(all_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        all_chars[i], all_chars[j] = all_chars[j], all_chars[i]

    return "".join(all_chars)
