#!/usr/bin/env python3
"""Probe a single DYNAMIXEL servo without modifying any register.

READ-ONLY SAFETY CONTRACT
-------------------------
This tool only uses these PacketHandler operations:
  - ping
  - read1ByteTxRx
  - read2ByteTxRx

It contains no register-write, torque-enable, ID-change, baudrate-change,
or goal-position operation. The baudrate passed on the command line only
configures the PC serial port; it does not modify the servo baudrate.

Register addresses are used only after the pinged model is recognized as an
AX-12 family servo (model number 12) or AX-18 family servo (model number 18)
using DYNAMIXEL Protocol 1.0.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ReadOnlyProfile:
    name: str
    protocol_version: float
    model_number_address: int
    firmware_version_address: int
    present_position_address: int


AX_READ_ONLY_PROFILES = {
    12: ReadOnlyProfile(
        name="AX-12 / AX-12+ / AX-12A family",
        protocol_version=1.0,
        model_number_address=0,
        firmware_version_address=2,
        present_position_address=36,
    ),
    18: ReadOnlyProfile(
        name="AX-18F / AX-18A family",
        protocol_version=1.0,
        model_number_address=0,
        firmware_version_address=2,
        present_position_address=36,
    ),
}


def servo_id(value: str) -> int:
    parsed = int(value)
    if not 0 <= parsed <= 253:
        raise argparse.ArgumentTypeError("servo ID must be between 0 and 253")
    return parsed


def positive_baudrate(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("baudrate must be a positive integer")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only communication probe for one DYNAMIXEL AX servo. "
            "No servo register is written."
        )
    )
    parser.add_argument(
        "--port",
        required=True,
        help="serial device, preferably /dev/serial/by-id/...",
    )
    parser.add_argument(
        "--baudrate",
        required=True,
        type=positive_baudrate,
        help="PC serial baudrate to test (does not change the servo baudrate)",
    )
    parser.add_argument(
        "--protocol-version",
        required=True,
        type=float,
        choices=(1.0, 2.0),
        help="DYNAMIXEL protocol version to test",
    )
    parser.add_argument(
        "--id",
        required=True,
        type=servo_id,
        dest="servo_id",
        help="physical servo ID to test; do not use project mock IDs",
    )
    return parser.parse_args()


def result_error(
    packet_handler: Any,
    comm_success: int,
    comm_result: int,
    servo_error: int,
) -> str | None:
    if comm_result != comm_success:
        return packet_handler.getTxRxResult(comm_result)
    if servo_error != 0:
        return packet_handler.getRxPacketError(servo_error)
    return None


def read_one_byte(
    packet_handler: Any,
    port_handler: Any,
    comm_success: int,
    target_id: int,
    address: int,
) -> tuple[int | None, str | None]:
    value, comm_result, servo_error = packet_handler.read1ByteTxRx(
        port_handler, target_id, address
    )
    error = result_error(
        packet_handler, comm_success, comm_result, servo_error
    )
    return (None, error) if error else (value, None)


def read_two_bytes(
    packet_handler: Any,
    port_handler: Any,
    comm_success: int,
    target_id: int,
    address: int,
) -> tuple[int | None, str | None]:
    value, comm_result, servo_error = packet_handler.read2ByteTxRx(
        port_handler, target_id, address
    )
    error = result_error(
        packet_handler, comm_success, comm_result, servo_error
    )
    return (None, error) if error else (value, None)


def run(args: argparse.Namespace) -> int:
    try:
        from dynamixel_sdk import COMM_SUCCESS, PacketHandler, PortHandler
    except ModuleNotFoundError:
        print(
            "ERROR: Python package 'dynamixel-sdk' is not installed.\n"
            "Install it in a virtual environment with:\n"
            "  python3 -m pip install dynamixel-sdk",
            file=sys.stderr,
        )
        return 2

    print("DYNAMIXEL read-only probe")
    print("Safety mode : PING + READ operations only")
    print(f"Port        : {args.port}")
    print(f"Baudrate    : {args.baudrate}")
    print(f"Protocol    : {args.protocol_version:.1f}")
    print(f"Servo ID    : {args.servo_id}")

    port_handler = PortHandler(args.port)
    packet_handler = PacketHandler(args.protocol_version)
    port_open = False

    try:
        if not port_handler.openPort():
            print(f"ERROR: cannot open serial port {args.port}", file=sys.stderr)
            return 3
        port_open = True
        print("Port        : opened")

        if not port_handler.setBaudRate(args.baudrate):
            print(
                f"ERROR: cannot configure PC serial port at {args.baudrate} baud",
                file=sys.stderr,
            )
            return 4
        print("Baudrate    : configured on PC")

        ping_model, comm_result, servo_error = packet_handler.ping(
            port_handler, args.servo_id
        )
        error = result_error(
            packet_handler, COMM_SUCCESS, comm_result, servo_error
        )
        if error:
            print(f"ERROR: ping failed: {error}", file=sys.stderr)
            return 5

        print("Ping        : success")
        print(f"Ping model  : {ping_model}")

        profile = AX_READ_ONLY_PROFILES.get(ping_model)
        if profile is None:
            print(
                "ERROR: the model responded, but it is not a supported AX-12/AX-18 "
                "profile. Register reads are stopped to avoid assuming addresses.",
                file=sys.stderr,
            )
            return 6

        if args.protocol_version != profile.protocol_version:
            print(
                "ERROR: the detected model and requested protocol profile do not match. "
                "Register reads are stopped.",
                file=sys.stderr,
            )
            return 7

        print(f"Model family: {profile.name}")

        model_number, error = read_two_bytes(
            packet_handler,
            port_handler,
            COMM_SUCCESS,
            args.servo_id,
            profile.model_number_address,
        )
        if error:
            print(f"ERROR: Model Number read failed: {error}", file=sys.stderr)
            return 8
        if model_number != ping_model:
            print(
                "ERROR: Model Number read does not match the ping response "
                f"({model_number} != {ping_model})",
                file=sys.stderr,
            )
            return 9
        print(f"Model Number: {model_number}")

        firmware_version, firmware_error = read_one_byte(
            packet_handler,
            port_handler,
            COMM_SUCCESS,
            args.servo_id,
            profile.firmware_version_address,
        )
        if firmware_error:
            print(f"Firmware    : unavailable ({firmware_error})")
        else:
            print(f"Firmware    : {firmware_version}")

        present_position, error = read_two_bytes(
            packet_handler,
            port_handler,
            COMM_SUCCESS,
            args.servo_id,
            profile.present_position_address,
        )
        if error:
            print(f"ERROR: Present Position read failed: {error}", file=sys.stderr)
            return 10

        print(f"Position raw: {present_position}")
        print("RESULT      : PASS - read-only communication is proven")
        return 0
    finally:
        if port_open:
            port_handler.closePort()
            print("Port        : closed")


def main() -> int:
    return run(parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
