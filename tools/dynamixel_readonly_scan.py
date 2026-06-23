#!/usr/bin/env python3
"""Read-only DYNAMIXEL AX bus inventory scanner, independent from ROS.

Safety contract:
- the only servo operations are ping, read1ByteTxRx and read2ByteTxRx;
- setBaudRate configures the PC serial port only;
- no existing project YAML is ever updated by this program;
- the historical PhantomX profile is comparison data, never a real mapping.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROTECTED_OUTPUT_PATHS = {
    (PROJECT_ROOT / "config" / "dynamixel_ids.yaml").resolve(),
    (PROJECT_ROOT / "config" / "joint_mapping.yaml").resolve(),
}

# AX-12A / AX-18A Protocol 1.0 control table: read access only.
ADDR_MODEL_NUMBER = 0
ADDR_FIRMWARE_VERSION = 2
ADDR_ID = 3
ADDR_CW_ANGLE_LIMIT = 6
ADDR_CCW_ANGLE_LIMIT = 8
ADDR_TORQUE_ENABLE = 24
ADDR_PRESENT_POSITION = 36
ADDR_PRESENT_VOLTAGE = 42
ADDR_PRESENT_TEMPERATURE = 43

AX_MODEL_NUMBERS = {12, 18}

# Exactly 18 joint expectations. Left-front coxa deliberately has two
# accepted historical alternatives; neither value is a measured robot ID.
PHANTOMX_V2_KURTE_PROFILE = {
    "name": "phantomx_v2_kurte",
    "status": "historical_hypothesis_only",
    "joint_ids": {
        "right_front_coxa": (2,),
        "right_front_femur": (4,),
        "right_front_tibia": (6,),
        "right_middle_coxa": (14,),
        "right_middle_femur": (16,),
        "right_middle_tibia": (18,),
        "right_rear_coxa": (8,),
        "right_rear_femur": (10,),
        "right_rear_tibia": (12,),
        "left_front_coxa": (1, 19),
        "left_front_femur": (3,),
        "left_front_tibia": (5,),
        "left_middle_coxa": (13,),
        "left_middle_femur": (15,),
        "left_middle_tibia": (17,),
        "left_rear_coxa": (7,),
        "left_rear_femur": (9,),
        "left_rear_tibia": (11,),
    },
}

FORBIDDEN_SDK_CALL_NAMES = {
    "write",
    "syncwrite",
    "regwrite",
    "factoryreset",
    "reboot",
    "setgoal",
    "torqueenable",
    "setid",
    "write1bytetxrx",
    "write2bytetxrx",
    "write4bytetxrx",
    "groupbulkwrite",
    "groupsyncwrite",
}


def bounded_id(value: str) -> int:
    parsed = int(value)
    if not 0 <= parsed <= 253:
        raise argparse.ArgumentTypeError("ID must be between 0 and 253")
    return parsed


def positive_integer(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be a positive integer")
    return parsed


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0.0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only scanner for DYNAMIXEL AX Protocol 1.0 servos"
    )
    parser.add_argument("--port", required=True)
    parser.add_argument("--baudrate", required=True, type=positive_integer)
    parser.add_argument("--protocol-version", required=True, type=float)
    parser.add_argument("--start-id", type=bounded_id, default=0)
    parser.add_argument("--end-id", type=bounded_id, default=253)
    parser.add_argument("--repetitions", type=positive_integer, default=3)
    parser.add_argument(
        "--timeout-ms",
        type=positive_float,
        default=None,
        help=(
            "requested timeout recorded in the report; DYNAMIXEL SDK high-level "
            "transactions retain their internally calculated packet timeout"
        ),
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--format", choices=("text", "yaml", "json"), default="text"
    )
    parser.add_argument(
        "--compare-profile", choices=("phantomx_v2_kurte",), default=None
    )
    parser.add_argument("--strict-readonly-check", action="store_true")
    return parser.parse_args(argv)


def validate_arguments(args: argparse.Namespace) -> None:
    if args.start_id > args.end_id:
        raise ValueError("--start-id must be less than or equal to --end-id")
    if args.protocol_version != 1.0:
        raise ValueError(
            "this AX scanner refuses protocols other than 1.0; no port was opened"
        )
    validate_output_path(args.output)


def validate_output_path(output: Path | None) -> None:
    if output is None:
        return
    resolved = output.expanduser().resolve()
    if resolved in PROTECTED_OUTPUT_PATHS:
        raise ValueError(f"refusing to modify protected project YAML: {resolved}")
    if resolved.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {resolved}")
    if not resolved.parent.exists():
        raise FileNotFoundError(f"output directory does not exist: {resolved.parent}")


def assert_source_is_read_only(source_path: Path | None = None) -> None:
    path = source_path or Path(__file__)
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    forbidden_found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            name = node.func.attr.lower()
        elif isinstance(node.func, ast.Name):
            name = node.func.id.lower()
        else:
            continue
        if name in FORBIDDEN_SDK_CALL_NAMES or name.startswith("write"):
            forbidden_found.append(name)
    if forbidden_found:
        raise RuntimeError(
            f"forbidden call(s) detected in scanner source: {sorted(set(forbidden_found))}"
        )


def packet_error(
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
    servo_id: int,
    address: int,
) -> tuple[int | None, str | None]:
    value, comm_result, servo_error = packet_handler.read1ByteTxRx(
        port_handler, servo_id, address
    )
    error = packet_error(
        packet_handler, comm_success, comm_result, servo_error
    )
    return (None, error) if error else (value, None)


def read_two_bytes(
    packet_handler: Any,
    port_handler: Any,
    comm_success: int,
    servo_id: int,
    address: int,
) -> tuple[int | None, str | None]:
    value, comm_result, servo_error = packet_handler.read2ByteTxRx(
        port_handler, servo_id, address
    )
    error = packet_error(
        packet_handler, comm_success, comm_result, servo_error
    )
    return (None, error) if error else (value, None)


def empty_servo_result(servo_id: int) -> dict[str, Any]:
    return {
        "id": servo_id,
        "stable": False,
        "responses_ok": 0,
        "model_number": None,
        "firmware_version": None,
        "reported_id": None,
        "present_position_raw": None,
        "present_voltage_raw": None,
        "present_temperature_c": None,
        "torque_enabled": None,
        "cw_angle_limit_raw": None,
        "ccw_angle_limit_raw": None,
        "read_errors": [],
    }


def record_read(
    servo: dict[str, Any],
    field: str,
    value: int | None,
    error: str | None,
    repetition: int,
) -> None:
    if error is None:
        servo[field] = value
    else:
        message = f"repetition {repetition}: {field}: {error}"
        if message not in servo["read_errors"]:
            servo["read_errors"].append(message)


def read_ax_registers(
    packet_handler: Any,
    port_handler: Any,
    comm_success: int,
    servo: dict[str, Any],
    repetition: int,
    ping_model: int,
) -> None:
    servo_id = servo["id"]
    model, model_error = read_two_bytes(
        packet_handler,
        port_handler,
        comm_success,
        servo_id,
        ADDR_MODEL_NUMBER,
    )
    record_read(servo, "model_number", model, model_error, repetition)
    detected_model = model if model is not None else ping_model

    if model is not None and model != ping_model:
        servo["read_errors"].append(
            f"repetition {repetition}: ping/read model mismatch "
            f"({ping_model} != {model})"
        )
    if detected_model not in AX_MODEL_NUMBERS:
        servo["read_errors"].append(
            f"repetition {repetition}: model {detected_model} is not AX-12/AX-18; "
            "AX-specific register reads skipped"
        )
        return

    one_byte_fields = (
        ("firmware_version", ADDR_FIRMWARE_VERSION),
        ("reported_id", ADDR_ID),
        ("present_voltage_raw", ADDR_PRESENT_VOLTAGE),
        ("present_temperature_c", ADDR_PRESENT_TEMPERATURE),
        ("torque_enabled", ADDR_TORQUE_ENABLE),
    )
    two_byte_fields = (
        ("present_position_raw", ADDR_PRESENT_POSITION),
        ("cw_angle_limit_raw", ADDR_CW_ANGLE_LIMIT),
        ("ccw_angle_limit_raw", ADDR_CCW_ANGLE_LIMIT),
    )

    for field, address in one_byte_fields:
        value, error = read_one_byte(
            packet_handler, port_handler, comm_success, servo_id, address
        )
        if field == "torque_enabled" and value is not None:
            value = bool(value)
        record_read(servo, field, value, error, repetition)

    for field, address in two_byte_fields:
        value, error = read_two_bytes(
            packet_handler, port_handler, comm_success, servo_id, address
        )
        record_read(servo, field, value, error, repetition)


def scan_bus(
    args: argparse.Namespace,
    port_handler: Any,
    packet_handler: Any,
    comm_success: int,
) -> list[dict[str, Any]]:
    detected: dict[int, dict[str, Any]] = {}
    for repetition in range(1, args.repetitions + 1):
        for servo_id in range(args.start_id, args.end_id + 1):
            ping_model, comm_result, servo_error = packet_handler.ping(
                port_handler, servo_id
            )
            error = packet_error(
                packet_handler, comm_success, comm_result, servo_error
            )
            if error is not None:
                continue

            servo = detected.setdefault(servo_id, empty_servo_result(servo_id))
            servo["responses_ok"] += 1
            read_ax_registers(
                packet_handler,
                port_handler,
                comm_success,
                servo,
                repetition,
                ping_model,
            )

    servos = [detected[servo_id] for servo_id in sorted(detected)]
    for servo in servos:
        servo["stable"] = servo["responses_ok"] == args.repetitions
    return servos


def profile_allowed_ids(profile: dict[str, Any]) -> set[int]:
    return {
        servo_id
        for alternatives in profile["joint_ids"].values()
        for servo_id in alternatives
    }


def compare_with_phantomx_profile(detected_ids: Sequence[int]) -> dict[str, Any]:
    profile = PHANTOMX_V2_KURTE_PROFILE
    detected = set(detected_ids)
    joint_ids = profile["joint_ids"]
    fixed_ids = {
        alternatives[0]
        for alternatives in joint_ids.values()
        if len(alternatives) == 1
    }
    allowed_ids = profile_allowed_ids(profile)
    alternative_ids = set(joint_ids["left_front_coxa"])
    alternatives_present = sorted(detected & alternative_ids)
    missing_fixed = sorted(fixed_ids - detected)
    unexpected = sorted(detected - allowed_ids)

    if alternatives_present == [1]:
        lf_status = "id_1_present"
    elif alternatives_present == [19]:
        lf_status = "id_19_present"
    elif alternatives_present == [1, 19]:
        lf_status = "both_present_ambiguous"
    else:
        lf_status = "neither_present"

    if not missing_fixed and len(alternatives_present) == 1 and not unexpected:
        compatibility = "compatible_with_hypothesis"
    elif detected & allowed_ids:
        compatibility = "partially_compatible_with_hypothesis"
    else:
        compatibility = "incompatible_with_hypothesis"

    expected_missing: list[int | str] = list(missing_fixed)
    if not alternatives_present:
        expected_missing.append("left_front_coxa: 1_or_19")

    return {
        "profile": profile["name"],
        "disclaimer": "historical hypothesis only; real mapping is not validated",
        "expected_joint_count": len(joint_ids),
        "expected_fixed_ids": sorted(fixed_ids),
        "left_front_coxa_alternatives": sorted(alternative_ids),
        "detected_ids": sorted(detected),
        "expected_present": sorted(detected & allowed_ids),
        "expected_missing": expected_missing,
        "expected_fixed_missing": missing_fixed,
        "unexpected_ids": unexpected,
        "left_front_coxa_status": lf_status,
        "compatibility": compatibility,
    }


def build_report(
    args: argparse.Namespace, servos: list[dict[str, Any]]
) -> dict[str, Any]:
    stable_ids = [servo["id"] for servo in servos if servo["stable"]]
    unstable_ids = [servo["id"] for servo in servos if not servo["stable"]]
    report: dict[str, Any] = {
        "scan": {
            "timestamp_utc": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "port": args.port,
            "baudrate": args.baudrate,
            "protocol_version": args.protocol_version,
            "read_only": True,
            "start_id": args.start_id,
            "end_id": args.end_id,
            "repetitions": args.repetitions,
            "timeout_ms_requested": args.timeout_ms,
            "timeout_policy": "SDK high-level packet timeout",
        },
        "summary": {
            "detected_count": len(servos),
            "stable_count": len(stable_ids),
            "unstable_count": len(unstable_ids),
            "stable_ids": stable_ids,
            "unstable_ids": unstable_ids,
        },
        "servos": servos,
    }
    if args.compare_profile == "phantomx_v2_kurte":
        report["comparison"] = compare_with_phantomx_profile(
            [servo["id"] for servo in servos]
        )
    return report


def render_text(report: dict[str, Any]) -> str:
    scan = report["scan"]
    summary = report["summary"]
    lines = [
        "DYNAMIXEL AX read-only scan",
        "Safety      : PING + READ only; no real mapping is modified",
        f"Port        : {scan['port']}",
        f"Baudrate    : {scan['baudrate']}",
        f"Protocol    : {scan['protocol_version']}",
        f"ID range    : {scan['start_id']}..{scan['end_id']}",
        f"Repetitions : {scan['repetitions']}",
        f"Detected    : {summary['detected_count']}",
        f"Stable IDs  : {summary['stable_ids']}",
        f"Unstable IDs: {summary['unstable_ids']}",
    ]
    if scan["timeout_ms_requested"] is not None:
        lines.append(
            "Timeout     : requested value recorded; SDK packet timeout remains managed internally"
        )

    for servo in report["servos"]:
        status = "stable" if servo["stable"] else "unstable"
        lines.extend(
            [
                "",
                f"ID {servo['id']} ({status}, {servo['responses_ok']}/{scan['repetitions']} responses)",
                f"  model number       : {servo['model_number']}",
                f"  firmware           : {servo['firmware_version']}",
                f"  reported ID        : {servo['reported_id']}",
                f"  position raw       : {servo['present_position_raw']}",
                f"  voltage raw        : {servo['present_voltage_raw']}",
                f"  temperature C      : {servo['present_temperature_c']}",
                f"  torque enabled     : {servo['torque_enabled']}",
                f"  CW/CCW limits raw  : {servo['cw_angle_limit_raw']} / {servo['ccw_angle_limit_raw']}",
            ]
        )
        for error in servo["read_errors"]:
            lines.append(f"  warning            : {error}")

    comparison = report.get("comparison")
    if comparison:
        lines.extend(
            [
                "",
                "PhantomX historical profile comparison",
                f"  profile             : {comparison['profile']}",
                f"  expected fixed IDs  : {comparison['expected_fixed_ids']}",
                f"  LF coxa alternative : {comparison['left_front_coxa_alternatives']}",
                f"  detected IDs        : {comparison['detected_ids']}",
                f"  expected present    : {comparison['expected_present']}",
                f"  expected missing    : {comparison['expected_missing']}",
                f"  unexpected IDs      : {comparison['unexpected_ids']}",
                f"  LF coxa status      : {comparison['left_front_coxa_status']}",
                f"  conclusion          : {comparison['compatibility']}",
                "  IMPORTANT           : inventory comparison only; mapping not validated",
            ]
        )
    return "\n".join(lines) + "\n"


def render_report(report: dict[str, Any], output_format: str) -> str:
    if output_format == "text":
        return render_text(report)
    if output_format == "json":
        return json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    try:
        import yaml
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "PyYAML is required for --format yaml: python3 -m pip install PyYAML"
        ) from exc
    return yaml.safe_dump(report, sort_keys=False, allow_unicode=True)


def emit_report(rendered: str, output: Path | None) -> None:
    if output is None:
        print(rendered, end="")
        return
    with output.expanduser().open("x", encoding="utf-8", newline="\n") as stream:
        print(rendered, end="", file=stream)
    print(f"Inventory saved to new file: {output}", file=sys.stderr)


def run(args: argparse.Namespace) -> int:
    try:
        validate_arguments(args)
        if args.strict_readonly_check:
            assert_source_is_read_only()
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.timeout_ms is not None:
        print(
            "WARNING: --timeout-ms is recorded but not forced; SDK high-level "
            "packet methods calculate their own timeout.",
            file=sys.stderr,
        )

    try:
        from dynamixel_sdk import COMM_SUCCESS, PacketHandler, PortHandler
    except ModuleNotFoundError:
        print(
            "ERROR: install the non-ROS dependency with: "
            "python3 -m pip install dynamixel-sdk",
            file=sys.stderr,
        )
        return 3

    port_handler = PortHandler(args.port)
    packet_handler = PacketHandler(args.protocol_version)
    port_open = False
    try:
        if not port_handler.openPort():
            print(f"ERROR: cannot open serial port {args.port}", file=sys.stderr)
            return 4
        port_open = True
        if not port_handler.setBaudRate(args.baudrate):
            print(
                f"ERROR: cannot configure PC serial port at {args.baudrate} baud",
                file=sys.stderr,
            )
            return 5

        servos = scan_bus(args, port_handler, packet_handler, COMM_SUCCESS)
        report = build_report(args, servos)
        rendered = render_report(report, args.format)
        emit_report(rendered, args.output)
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 6
    finally:
        if port_open:
            port_handler.closePort()


def main(argv: Sequence[str] | None = None) -> int:
    return run(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
