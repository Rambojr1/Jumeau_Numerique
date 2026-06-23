from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from raw_to_radians import raw_to_radians  # noqa: E402


class RawToRadiansTests(unittest.TestCase):
    def test_zero_tick_maps_to_offset(self) -> None:
        result = raw_to_radians(
            500,
            raw_zero=500,
            scale_rad_per_tick=0.01,
            sign=1,
            offset_rad=0.2,
        )
        self.assertAlmostEqual(0.2, result)

    def test_positive_sign(self) -> None:
        result = raw_to_radians(
            510, raw_zero=500, scale_rad_per_tick=0.01, sign=1
        )
        self.assertAlmostEqual(0.1, result)

    def test_negative_sign(self) -> None:
        result = raw_to_radians(
            510, raw_zero=500, scale_rad_per_tick=0.01, sign=-1
        )
        self.assertAlmostEqual(-0.1, result)

    def test_missing_real_calibration_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            raw_to_radians(
                510, raw_zero=None, scale_rad_per_tick=0.01, sign=1
            )
        with self.assertRaises(ValueError):
            raw_to_radians(
                510, raw_zero=500, scale_rad_per_tick=None, sign=1
            )
        with self.assertRaises(ValueError):
            raw_to_radians(
                510, raw_zero=500, scale_rad_per_tick=0.01, sign=None
            )

    def test_non_finite_input_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            raw_to_radians(
                math.nan, raw_zero=500, scale_rad_per_tick=0.01, sign=1
            )


if __name__ == "__main__":
    unittest.main()
