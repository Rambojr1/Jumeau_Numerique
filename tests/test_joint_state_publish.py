from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from fake_dynamixel_bus import FakeDynamixelBus  # noqa: E402
from offline_joint_state_bridge import (  # noqa: E402
    build_offline_joint_state_data,
    extract_movable_joint_names,
    validate_joint_state_lengths,
)


URDF = ROOT / "hexa_simulation" / "urdf" / "hexapode.urdf"


class JointStatePublishTests(unittest.TestCase):
    def test_synthetic_message_has_one_position_per_name(self) -> None:
        names = extract_movable_joint_names(URDF)
        bus = FakeDynamixelBus(names)
        raw_positions = bus.read_raw_positions(1.25)
        message_names, positions = build_offline_joint_state_data(
            bus.joint_names, raw_positions
        )

        self.assertEqual(18, len(message_names))
        self.assertEqual(len(message_names), len(positions))
        self.assertTrue(all(math.isfinite(value) for value in positions))

    def test_length_mismatch_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_joint_state_lengths(["joint_a"], [])
        with self.assertRaises(ValueError):
            build_offline_joint_state_data(["joint_a"], [500, 501])


if __name__ == "__main__":
    unittest.main()
