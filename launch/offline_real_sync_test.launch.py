#!/usr/bin/env python3
"""Standalone launch for synthetic /joint_states + existing URDF + RViz."""

from pathlib import Path
import sys

from launch import LaunchDescription, LaunchService
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


ROOT = Path(__file__).resolve().parents[1]
URDF = ROOT / "hexa_simulation" / "urdf" / "hexapode.urdf"
RVIZ = ROOT / "hexa_simulation" / "rviz" / "hexapode.rviz"
OFFLINE_BRIDGE = ROOT / "tools" / "offline_joint_state_bridge.py"


def generate_launch_description() -> LaunchDescription:
    robot_description = URDF.read_text(encoding="utf-8")
    return LaunchDescription(
        [
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[{"robot_description": robot_description}],
                output="screen",
            ),
            ExecuteProcess(
                cmd=[
                    sys.executable,
                    str(OFFLINE_BRIDGE),
                    "--urdf",
                    str(URDF),
                ],
                output="screen",
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                arguments=["-d", str(RVIZ)],
                output="screen",
            ),
        ]
    )


def main() -> int:
    service = LaunchService()
    service.include_launch_description(generate_launch_description())
    return service.run()


if __name__ == "__main__":
    raise SystemExit(main())
