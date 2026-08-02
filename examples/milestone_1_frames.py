"""Demonstrate valid standard and extended Classical CAN frames."""

from automotive_can_validation_lab.protocol.frame import CanFrame


def main() -> None:
    """Create and log example Classical CAN frames."""
    standard_frame = CanFrame(
        identifier=0x123,
        is_extended=False,
        data=b"\xAA\x55",
        timestamp=1.25,
    )
    extended_frame = CanFrame(
        identifier=0x1ABCDE,
        is_extended=True,
        data=b"",
        timestamp=2.0,
    )

    print(standard_frame)
    print(extended_frame)


if __name__ == "__main__":
    main()