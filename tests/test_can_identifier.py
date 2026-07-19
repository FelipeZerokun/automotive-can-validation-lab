"""Tests for standard and extended CAN identifier validation."""

from automotive_can_validation.can_identifier import (
    is_valid_extended_identifier,
    is_valid_standard_identifier,
)


# CAN-FND-REQ-001


def test_lowest_standard_identifier_is_valid() -> None:
    assert is_valid_standard_identifier(0x000) is True


def test_highest_standard_identifier_is_valid() -> None:
    assert is_valid_standard_identifier(0x7FF) is True


def test_negative_standard_identifier_is_invalid() -> None:
    assert is_valid_standard_identifier(-1) is False


def test_identifier_above_standard_range_is_invalid() -> None:
    assert is_valid_standard_identifier(0x800) is False


# CAN-FND-REQ-002


def test_lowest_extended_identifier_is_valid() -> None:
    assert is_valid_extended_identifier(0x00000000) is True


def test_highest_extended_identifier_is_valid() -> None:
    assert is_valid_extended_identifier(0x1FFFFFFF) is True


def test_negative_extended_identifier_is_invalid() -> None:
    assert is_valid_extended_identifier(-1) is False


def test_identifier_above_extended_range_is_invalid() -> None:
    assert is_valid_extended_identifier(0x20000000) is False
