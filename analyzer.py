"""Local password-strength analysis.

This module never stores, logs, or transmits passwords. Its scoring is a
transparent heuristic, not a guarantee against cracking or a substitute for
a vetted password-strength estimator.
"""

from dataclasses import dataclass
import re
import string
from typing import List, Tuple


COMMON_PASSWORDS = {
    "password", "password1", "123456", "123456789", "12345678",
    "qwerty", "qwerty123", "admin", "letmein", "welcome",
    "iloveyou", "abc123", "111111", "000000", "india123",
}

SEQUENTIAL_PATTERNS = (
    "abcdefghijklmnopqrstuvwxyz",
    "0123456789",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
)


@dataclass(frozen=True)
class PasswordReport:
    """Result of a password analysis without retaining the password."""

    score: int
    rating: str
    feedback: Tuple[str, ...]
    checks: Tuple[Tuple[str, bool], ...]


def _contains_sequence(value: str, minimum: int = 4) -> bool:
    """Return True for ascending/reversed alphabet, digit, or keyboard runs."""
    lowered = value.lower()
    for pattern in SEQUENTIAL_PATTERNS:
        for candidate in (pattern, pattern[::-1]):
            for start in range(0, len(candidate) - minimum + 1):
                if candidate[start:start + minimum] in lowered:
                    return True
    return False


def analyze_password(password: str) -> PasswordReport:
    """Assess a password using length, character diversity, and pattern checks.

    The password is used only during this function call. The returned report
    contains no password or password-derived substring.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")

    checks = [
        ("At least 12 characters", len(password) >= 12),
        ("Uppercase letter", any(ch.isupper() for ch in password)),
        ("Lowercase letter", any(ch.islower() for ch in password)),
        ("Number", any(ch.isdigit() for ch in password)),
        ("Special character", any(not ch.isalnum() and not ch.isspace()
                                  for ch in password)),
        ("No leading or trailing whitespace", password == password.strip()),
    ]

    score = 0
    feedback: List[str] = []

    # Length is weighted because longer unique passwords are generally harder
    # to guess than short passwords with many character classes.
    if len(password) >= 16:
        score += 3
    elif len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 12 characters; 16 or more is preferable.")

    diversity = sum((
        any(ch.islower() for ch in password),
        any(ch.isupper() for ch in password),
        any(ch.isdigit() for ch in password),
        any(not ch.isalnum() and not ch.isspace() for ch in password),
    ))
    score += diversity

    if not any(ch.islower() for ch in password):
        feedback.append("Include lowercase letters.")
    if not any(ch.isupper() for ch in password):
        feedback.append("Include uppercase letters.")
    if not any(ch.isdigit() for ch in password):
        feedback.append("Include numbers.")
    if not any(not ch.isalnum() and not ch.isspace() for ch in password):
        feedback.append("Consider including a symbol.")

    normalized = password.lower()
    if normalized in COMMON_PASSWORDS:
        score = 0
        feedback.append("This is a commonly used password. Choose a unique one.")
    else:
        if len(password) > 0 and len(set(password)) == 1:
            score = max(0, score - 3)
            feedback.append("Avoid repeating the same character.")
        if re.search(r"(.)\1{2,}", password):
            score = max(0, score - 2)
            feedback.append("Avoid long repeated-character patterns.")
        if _contains_sequence(password):
            score = max(0, score - 2)
            feedback.append("Avoid predictable sequences such as abcd, 1234, or qwer.")
        if password != password.strip():
            score = max(0, score - 1)
            feedback.append("Remove leading or trailing spaces to avoid input mistakes.")

    # Maximum unpenalized score is 7 (length + four character classes).
    score = min(7, max(0, score))

    if score <= 2:
        rating = "WEAK"
    elif score <= 5:
        rating = "MODERATE"
    elif score == 6:
        rating = "STRONG"
    else:
        rating = "VERY STRONG"

    if not feedback:
        feedback.append("Good result. Use a unique password and never reuse it.")

    return PasswordReport(
        score=score,
        rating=rating,
        feedback=tuple(feedback),
        checks=tuple(checks),
    )
