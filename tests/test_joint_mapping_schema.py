from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from validate_joint_mapping import (  # noqa: E402
    collect_offline_errors,
    collect_real_readiness_errors,
    extract_movable_joint_names,
    load_yaml,
)


URDF = ROOT / "hexa_simulation" / "urdf" / "hexapode.urdf"
MAPPING = ROOT / "config" / "joint_mapping.yaml"
IDS = ROOT / "config" / "dynamixel_ids.yaml"
BRIDGE = ROOT / "config" / "real_hexapod_bridge.yaml"


class JointMappingSchemaTests(unittest.TestCase):
    def test_urdf_contains_six_legs_with_three_joints_each(self) -> None:
        names = extract_movable_joint_names(URDF)
        self.assertEqual(18, len(names))
        for leg in range(1, 7):
            expected = {
                f"leg_{leg}_coxa_joint",
                f"leg_{leg}_femur_joint",
                f"leg_{leg}_tibia_joint",
            }
            self.assertTrue(expected.issubset(names))

    def test_mapping_names_exactly_match_urdf(self) -> None:
        names = extract_movable_joint_names(URDF)
        mapping = load_yaml(MAPPING)
        self.assertEqual(names, list(mapping["joints"]))

    def test_offline_placeholders_are_valid(self) -> None:
        self.assertEqual(
            [], collect_offline_errors(URDF, MAPPING, IDS, BRIDGE)
        )

    def test_no_servo_id_is_invented(self) -> None:
        inventory = load_yaml(IDS)
        mapping = load_yaml(MAPPING)
        self.assertEqual([], inventory["servos"])
        self.assertTrue(
            all(values["id"] is None for values in mapping["joints"].values())
        )

    def test_real_mode_is_blocked_by_null_values(self) -> None:
        errors = collect_real_readiness_errors(URDF, MAPPING, IDS, BRIDGE)
        self.assertTrue(errors)
        self.assertTrue(any("is null" in error for error in errors))
        self.assertTrue(any("no real servo inventory" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
