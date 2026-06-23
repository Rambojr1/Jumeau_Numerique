#!/usr/bin/env python3
"""Pure conversion helpers with no ROS or hardware dependency."""

from __future__ import annotations

import math
from numbers import Real


def _finite_number(name: str, value: Real | None) -> float:
    if value is None or isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a real number, not {value!r}")
    converted = float(value)
    if not math.isfinite(converted):
        raise ValueError(f"{name} must be finite")
    return converted


def raw_to_radians(
    raw: Real | None,
    *,
    raw_zero: Real | None,
    scale_rad_per_tick: Real | None,
    sign: int | None,
    offset_rad: Real = 0.0,
) -> float:
    """Convert a raw tick value using an explicit calibration.

    Formula:
        q = sign * (raw - raw_zero) * scale_rad_per_tick + offset_rad

    Missing calibration values are rejected so that an incomplete real mapping
    cannot silently produce an angle.
    """

    if sign not in (-1, 1):
        raise ValueError("sign must be exactly -1 or 1")

    raw_value = _finite_number("raw", raw)
    zero_value = _finite_number("raw_zero", raw_zero)
    scale_value = _finite_number("scale_rad_per_tick", scale_rad_per_tick)
    offset_value = _finite_number("offset_rad", offset_rad)

    if scale_value <= 0.0:
        raise ValueError("scale_rad_per_tick must be strictly positive")

    return sign * (raw_value - zero_value) * scale_value + offset_value
