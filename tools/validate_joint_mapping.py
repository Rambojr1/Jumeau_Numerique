#!/usr/bin/env python3
"""Validate the offline placeholders or the future real-ready configuration."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_URDF = ROOT / "hexa_simulation" / "urdf" / "hexapode.urdf"
DEFAULT_MAPPING = ROOT / "config" / "joint_mapping.yaml"
DEFAULT_IDS = ROOT / "config" / "dynamixel_ids.yaml"
DEFAULT_BRIDGE = ROOT / "config" / "real_hexapod_bridge.yaml"

MOVABLE_JOINT_TYPES = {"revolute", "continuous", "prismatic"}
REQUIRED_JOINT_FIELDS = {
    "id",
    "physical_location",
    "servo_model",
    "sign",
    "raw_zero",
    "scale_rad_per_tick",
    "offset_rad",
    "min_rad",
    "max_rad",
    "calibrated",
}
PHYSICAL_FIELDS = (
    "id",
    "sign",
    "raw_zero",
    "scale_rad_per_tick",
    "min_rad",
    "max_rad",
)


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ModuleNotFoundError as exc:
        raise RuntimeError("PyYAML is required: python -m pip install PyYAML") from exc

    with path.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def extract_movable_joint_names(urdf_path: Path) -> list[str]:
    root = ET.parse(urdf_path).getroot()
    return [
        joint.attrib["name"]
        for joint in root.findall("joint")
        if joint.attrib.get("type") in MOVABLE_JOINT_TYPES
    ]


def collect_structural_errors(
    urdf_path: Path, mapping_path: Path
) -> list[str]:
    errors: list[str] = []
    urdf_names = extract_movable_joint_names(urdf_path)
    mapping = load_yaml(mapping_path)
    joints = mapping.get("joints")

    if len(urdf_names) != 18:
        errors.append(f"URDF must expose 18 movable joints, found {len(urdf_names)}")
    if len(set(urdf_names)) != len(urdf_names):
        errors.append("URDF movable joint names are not unique")
    if mapping.get("schema_version") != 1:
        errors.append("joint mapping schema_version must be 1")
    if mapping.get("source") != "urdf_extracted":
        errors.append("joint mapping source must be 'urdf_extracted'")
    if not isinstance(joints, dict):
        errors.append("joint mapping 'joints' must be a mapping")
        return errors

    mapping_names = list(joints)
    if mapping_names != urdf_names:
        errors.append("joint mapping names/order must exactly match the URDF")

    for joint_name, values in joints.items():
        if not isinstance(values, dict):
            errors.append(f"{joint_name} must contain a mapping")
            continue
        missing = REQUIRED_JOINT_FIELDS - set(values)
        if missing:
            errors.append(f"{joint_name} is missing fields: {sorted(missing)}")
    return errors


def collect_offline_errors(
    urdf_path: Path,
    mapping_path: Path,
    ids_path: Path,
    bridge_path: Path,
) -> list[str]:
    errors = collect_structural_errors(urdf_path, mapping_path)
    mapping = load_yaml(mapping_path)
    inventory = load_yaml(ids_path)
    bridge_config = load_yaml(bridge_path)

    if mapping.get("hardware_validated") is not False:
        errors.append("offline mapping must set hardware_validated: false")

    joints = mapping.get("joints", {})
    if isinstance(joints, dict):
        for joint_name, values in joints.items():
            if not isinstance(values, dict):
                continue
            for field in PHYSICAL_FIELDS:
                if values.get(field) is not None:
                    errors.append(f"{joint_name}.{field} must remain null offline")
            if values.get("physical_location") is not None:
                errors.append(f"{joint_name}.physical_location must remain null offline")
            if values.get("servo_model") is not None:
                errors.append(f"{joint_name}.servo_model must remain null offline")
            if values.get("calibrated") is not False:
                errors.append(f"{joint_name}.calibrated must be false offline")

    scan = inventory.get("scan")
    if not isinstance(scan, dict) or scan.get("read_only") is not True:
        errors.append("ID inventory must declare scan.read_only: true")
    if inventory.get("servos") != []:
        errors.append("offline ID inventory must contain servos: []")

    if bridge_config.get("hardware_validated") is not False:
        errors.append("offline bridge config must set hardware_validated: false")
    bridge = bridge_config.get("bridge")
    if not isinstance(bridge, dict):
        errors.append("bridge configuration is missing")
    else:
        if bridge.get("enabled") is not False:
            errors.append("real bridge must remain disabled offline")
        if bridge.get("read_only") is not True:
            errors.append("real bridge must remain read-only")
        for field in (
            "port",
            "baudrate",
            "protocol_version",
            "publish_rate_hz",
            "serial_timeout_ms",
        ):
            if bridge.get(field) is not None:
                errors.append(f"bridge.{field} must remain null offline")
    return errors


def collect_real_readiness_errors(
    urdf_path: Path,
    mapping_path: Path,
    ids_path: Path,
    bridge_path: Path,
) -> list[str]:
    errors = collect_structural_errors(urdf_path, mapping_path)
    mapping = load_yaml(mapping_path)
    inventory = load_yaml(ids_path)
    bridge_config = load_yaml(bridge_path)

    if mapping.get("hardware_validated") is not True:
        errors.append("mapping is not hardware-validated")

    mapped_ids: list[int] = []
    joints = mapping.get("joints", {})
    if isinstance(joints, dict):
        for joint_name, values in joints.items():
            if not isinstance(values, dict):
                continue
            for field in PHYSICAL_FIELDS:
                if values.get(field) is None:
                    errors.append(f"{joint_name}.{field} is null")
            if values.get("calibrated") is not True:
                errors.append(f"{joint_name} is not calibrated")
            if isinstance(values.get("id"), int):
                mapped_ids.append(values["id"])

    servos = inventory.get("servos")
    if not isinstance(servos, list) or not servos:
        errors.append("no real servo inventory is available")
        inventory_ids: list[int] = []
    else:
        inventory_ids = [
            servo.get("id") for servo in servos if isinstance(servo, dict)
        ]
    if len(mapped_ids) != len(set(mapped_ids)):
        errors.append("mapped servo IDs are not unique")
    if mapped_ids and sorted(mapped_ids) != sorted(inventory_ids):
        errors.append("mapped IDs do not match the scanned inventory")

    if bridge_config.get("hardware_validated") is not True:
        errors.append("bridge configuration is not hardware-validated")
    bridge = bridge_config.get("bridge")
    if not isinstance(bridge, dict):
        errors.append("bridge configuration is missing")
    else:
        if bridge.get("enabled") is not True:
            errors.append("real bridge is disabled")
        if bridge.get("read_only") is not True:
            errors.append("real bridge is not read-only")
        for field in (
            "port",
            "baudrate",
            "protocol_version",
            "publish_rate_hz",
            "serial_timeout_ms",
        ):
            if bridge.get(field) is None:
                errors.append(f"bridge.{field} is null")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--urdf", type=Path, default=DEFAULT_URDF)
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--ids", type=Path, default=DEFAULT_IDS)
    parser.add_argument("--bridge", type=Path, default=DEFAULT_BRIDGE)
    parser.add_argument("--require-real-ready", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.require_real_ready:
            errors = collect_real_readiness_errors(
                args.urdf, args.mapping, args.ids, args.bridge
            )
            mode = "real-ready"
        else:
            errors = collect_offline_errors(
                args.urdf, args.mapping, args.ids, args.bridge
            )
            mode = "offline-placeholder"
    except (OSError, ET.ParseError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if errors:
        print(f"INVALID {mode} configuration:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    joint_count = len(extract_movable_joint_names(args.urdf))
    print(f"VALID {mode} configuration: {joint_count} URDF joints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
