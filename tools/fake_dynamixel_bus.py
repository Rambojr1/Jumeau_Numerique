#!/usr/bin/env python3
"""Synthetic tick source for offline tests only.

This module has no serial, DYNAMIXEL SDK, servo ID, torque, or write operation.
Its constants are arbitrary test data and must never be copied into the real
mapping YAML.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


SYNTHETIC_RAW_ZERO = 500
SYNTHETIC_AMPLITUDE_TICKS = 60


class FakeDynamixelBus:
    def __init__(self, joint_names: Sequence[str]) -> None:
        self._joint_names = tuple(joint_names)
        if not self._joint_names:
            raise ValueError("at least one joint name is required")
        if len(set(self._joint_names)) != len(self._joint_names):
            raise ValueError("joint names must be unique")

    @property
    def joint_names(self) -> tuple[str, ...]:
        return self._joint_names

    def read_raw_positions(self, elapsed_seconds: float) -> list[int]:
        """Return deterministic synthetic ticks, one per URDF joint name."""

        values: list[int] = []
        count = len(self._joint_names)
        for index in range(count):
            phase = 2.0 * math.pi * index / count
            displacement = SYNTHETIC_AMPLITUDE_TICKS * math.sin(
                float(elapsed_seconds) + phase
            )
            values.append(int(round(SYNTHETIC_RAW_ZERO + displacement)))
        return values
