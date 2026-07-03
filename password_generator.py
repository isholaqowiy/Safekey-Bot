import secrets
import string

def generate_secure_password(length: int = 16, uppercase: bool = True, lowercase: bool = True, numbers: bool = True, symbols: bool = True) -> str:
    """Generates a cryptographically secure password based on user constraints."""
    character_pool = ""
    guaranteed_chars = []

    if uppercase:
        character_pool += string.ascii_uppercase
        guaranteed_chars.append(secrets.choice(string.ascii_uppercase))
    if lowercase:
        character_pool += string.ascii_lowercase
        guaranteed_chars.append(secrets.choice(string.ascii_lowercase))
    if numbers:
        character_pool += string.digits
        guaranteed_chars.append(secrets.choice(string.digits))
    if symbols:
        special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        character_pool += special_chars
        guaranteed_chars.append(secrets.choice(special_chars))

    # Fallback if everything is deselected
    if not character_pool:
        character_pool = string.ascii_lowercase + string.digits
        guaranteed_chars.append(secrets.choice(string.ascii_lowercase))

    # Fill remaining length
    remaining_length = length - len(guaranteed_chars)
    if remaining_length > 0:
        guaranteed_chars.extend(secrets.choice(character_pool) for _ in range(remaining_length))

    # Shuffle the list securely
    secrets.SystemRandom().shuffle(guaranteed_chars)
    return "".join(guaranteed_chars)

def evaluate_strength(password: str) -> str:
    """Evaluates and returns password strength with a colored indicator."""
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    score = sum([has_upper, has_lower, has_digit, has_special])

    if length >= 14 and score >= 4:
        return "🟢 Strong"
    elif length >= 10 and score >= 3:
        return "🟡 Medium"
    else:
        return "🔴 Weak"

