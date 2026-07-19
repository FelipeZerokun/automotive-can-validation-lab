"""Validation utilities for CAN identifiers."""

STANDARD_IDENTIFIER_MIN = 0x000
STANDARD_IDENTIFIER_MAX = 0x7FF

EXTENDED_IDENTIFIER_MIN = 0x00000000
EXTENDED_IDENTIFIER_MAX = 0x1FFFFFFF


def is_valid_standard_identifier(identifier: int) -> bool:
    """Return whether an integer fits the 11-bit standard CAN range."""

    return STANDARD_IDENTIFIER_MIN <= identifier <= STANDARD_IDENTIFIER_MAX


def is_valid_extended_identifier(identifier: int) -> bool:
    """Return whether an integer fits the 29-bit extended CAN range."""

    return EXTENDED_IDENTIFIER_MIN <= identifier <= EXTENDED_IDENTIFIER_MAX
