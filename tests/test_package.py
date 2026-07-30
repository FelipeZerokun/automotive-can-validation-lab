"""Smoke tests for the project package."""

import automotive_can_validation_lab


def test_package_exposes_version() -> None:
    """The installed package exposes its initial version."""
    assert automotive_can_validation_lab.__version__ == "0.1.0"