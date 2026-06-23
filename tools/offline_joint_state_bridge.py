#!/usr/bin/env python3
"""Publish synthetic JointState messages for offline RViz testing only.

This program reads joint names from the URDF but never reads the real mapping
values. It has no serial or DYNAMIXEL SDK dependency and cannot command motors.
"""

from __future__ import annotations

import argparse
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Sequence

from fake_dynamixel_bus import FakeDynamixelBus, SYNTHETIC_RAW_ZERO
from raw_to_radians import raw_to_radians


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_URDF = ROOT / "hexa_simulation" / "urdf" / "hexapode.urdf"
MOVABLE_JOINT_TYPES = {"revolute", "continuous", "prismatic"}

# Arbitrary offline-only conversion values. They are intentionally absent from
# config/joint_mapping.yaml and must never be treated as hardware calibration.
SYNTHETIC_SCALE_RAD_PER_TICK = 0.004
SYNTHETIC_SIGN = 1


def extract_movable_joint_names(urdf_path: Path) -> list[str]:
    root = ET.parse(urdf_path).getroot()
    return [
        joint.attrib["name"]
        for joint in root.findall("joint")
        if joint.attrib.get("type") in MOVABLE_JOINT_TYPES
    ]


def validate_joint_state_lengths(
    names: Sequence[str], positions: Sequence[float]
) -> None:
    if len(names) != len(positions):
        raise ValueError(
            f"JointState length mismatch: {len(names)} names, "
            f"{len(positions)} positions"
        )


def build_offline_joint_state_data(
    joint_names: Sequence[str], raw_positions: Sequence[int]
) -> tuple[list[str], list[float]]:
    names = list(joint_names)
    if len(names) != len(raw_positions):
        raise ValueError("synthetic raw position count does not match joint names")

    positions = [
        raw_to_radians(
            raw,
            raw_zero=SYNTHETIC_RAW_ZERO,
            scale_rad_per_tick=SYNTHETIC_SCALE_RAD_PER_TICK,
            sign=SYNTHETIC_SIGN,
            offset_rad=0.0,
        )
        for raw in raw_positions
    ]
    validate_joint_state_lengths(names, positions)
    if not all(math.isfinite(position) for position in positions):
        raise ValueError("all synthetic positions must be finite")
    return names, positions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--urdf", type=Path, default=DEFAULT_URDF)
    parser.add_argument("--rate-hz", type=float, default=20.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.rate_hz <= 0.0:
        print("ERROR: --rate-hz must be positive", file=sys.stderr)
        return 2

    joint_names = extract_movable_joint_names(args.urdf)
    if len(joint_names) != 18:
        print(
            f"ERROR: expected 18 movable URDF joints, found {len(joint_names)}",
            file=sys.stderr,
        )
        return 3

    try:
        import rclpy
        from rclpy.node import Node
        from sensor_msgs.msg import JointState
    except ModuleNotFoundError as exc:
        print(f"ERROR: ROS 2 Python dependency unavailable: {exc}", file=sys.stderr)
        return 4

    class OfflineJointStateBridge(Node):
        def __init__(self) -> None:
            super().__init__("offline_joint_state_bridge")
            self.publisher = self.create_publisher(JointState, "/joint_states", 10)
            self.bus = FakeDynamixelBus(joint_names)
            self.start_time = self.get_clock().now()
            self.timer = self.create_timer(1.0 / args.rate_hz, self.publish_state)
            self.get_logger().warning(
                "OFFLINE SYNTHETIC DATA: no robot hardware or real calibration"
            )

        def publish_state(self) -> None:
            now = self.get_clock().now()
            elapsed = (now - self.start_time).nanoseconds * 1e-9
            raw_positions = self.bus.read_raw_positions(elapsed)
            names, positions = build_offline_joint_state_data(
                self.bus.joint_names, raw_positions
            )

            message = JointState()
            message.header.stamp = now.to_msg()
            message.name = names
            message.position = positions
            self.publisher.publish(message)

    rclpy.init(args=[])
    node = OfflineJointStateBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
