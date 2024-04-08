# Author: Mohamed Elafifi
"""Module with validation logic for discounts."""

NAME_MIN_LEN = 4  # INCLUSIVE
NAME_MAX_LEN = 50  # INCLUSIVE

DESCRIPTION_MIN_LEN = 5  # INCLUSIVE
DESCRIPTION_MAX_LEN = 200  # INCLUSIVE

def validate_name(name: str):
    """Validate discount name."""
    ABOVE_MIN = len(name) >= NAME_MIN_LEN
    BELOW_MAX = len(name) <= NAME_MAX_LEN

    return ABOVE_MIN and BELOW_MAX

def validate_description(description: str):
    """Validate discount description."""
    ABOVE_MIN = len(description) >= DESCRIPTION_MIN_LEN
    BELOW_MAX = len(description) <= DESCRIPTION_MAX_LEN

    return ABOVE_MIN and BELOW_MAX
