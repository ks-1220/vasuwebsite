import re

def is_valid_name(name: str) -> bool:
    """
    Name must:
    - be at least 2 characters
    - contain only letters and spaces
    """
    if not name or len(name.strip()) < 2:
        return False
    return all(char.isalpha() or char.isspace() for char in name)


def is_valid_phone(phone: str) -> bool:
    """
    Indian phone number validation
    Starts with 6-9 and total 10 digits
    """
    return bool(re.fullmatch(r"[6-9]\d{9}", phone))


def is_valid_email(email: str) -> bool:
    """
    Basic email validation
    """
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))


def is_valid_message(message: str) -> bool:
    """
    Message must be at least 5 characters
    """
    return message and len(message.strip()) >= 5
