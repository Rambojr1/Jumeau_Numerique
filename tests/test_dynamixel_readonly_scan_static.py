from __future__ import annotations

import ast
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SCANNER_PATH = ROOT / "tools" / "dynamixel_readonly_scan.py"


def load_scanner_module():
    spec = importlib.util.spec_from_file_location("readonly_scanner", SCANNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scanner module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DynamixelReadonlyScanStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SCANNER_PATH.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)
        cls.scanner = load_scanner_module()

    def test_scanner_file_exists(self) -> None:
        self.assertTrue(SCANNER_PATH.is_file())

    def test_no_forbidden_sdk_call_exists(self) -> None:
        forbidden = {
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
        calls: list[str] = []
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Attribute):
                name = node.func.attr.lower()
            elif isinstance(node.func, ast.Name):
                name = node.func.id.lower()
            else:
                continue
            if name in forbidden or name.startswith("write"):
                calls.append(name)
        self.assertEqual([], calls)

    def test_expected_read_only_addresses_exist(self) -> None:
        expected = {
            "ADDR_MODEL_NUMBER": 0,
            "ADDR_FIRMWARE_VERSION": 2,
            "ADDR_ID": 3,
            "ADDR_CW_ANGLE_LIMIT": 6,
            "ADDR_CCW_ANGLE_LIMIT": 8,
            "ADDR_TORQUE_ENABLE": 24,
            "ADDR_PRESENT_POSITION": 36,
            "ADDR_PRESENT_VOLTAGE": 42,
            "ADDR_PRESENT_TEMPERATURE": 43,
        }
        for name, value in expected.items():
            self.assertEqual(value, getattr(self.scanner, name))

    def test_hypothetical_profile_has_18_joint_entries_and_lf_alternative(self) -> None:
        profile = self.scanner.PHANTOMX_V2_KURTE_PROFILE
        self.assertEqual("historical_hypothesis_only", profile["status"])
        self.assertEqual(18, len(profile["joint_ids"]))
        self.assertEqual((1, 19), profile["joint_ids"]["left_front_coxa"])
        comparison = self.scanner.compare_with_phantomx_profile(
            [2, 4, 6, 14, 16, 18, 8, 10, 12, 19, 3, 5, 13, 15, 17, 7, 9, 11]
        )
        self.assertEqual("id_19_present", comparison["left_front_coxa_status"])
        self.assertEqual("compatible_with_hypothesis", comparison["compatibility"])
        missing_alternative = self.scanner.compare_with_phantomx_profile(
            [2, 4, 6]
        )
        self.assertIn(
            "left_front_coxa: 1_or_19", missing_alternative["expected_missing"]
        )

    def test_existing_id_inventory_is_protected(self) -> None:
        protected = ROOT / "config" / "dynamixel_ids.yaml"
        with self.assertRaises(ValueError):
            self.scanner.validate_output_path(protected)

    def test_existing_joint_mapping_is_protected(self) -> None:
        protected = ROOT / "config" / "joint_mapping.yaml"
        with self.assertRaises(ValueError):
            self.scanner.validate_output_path(protected)

    def test_existing_arbitrary_output_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            existing = Path(directory) / "scan.json"
            existing.touch()
            with self.assertRaises(FileExistsError):
                self.scanner.validate_output_path(existing)

    def test_port_is_closed_from_finally_block(self) -> None:
        finally_calls: list[str] = []
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Try) or not node.finalbody:
                continue
            for child in ast.walk(ast.Module(body=node.finalbody, type_ignores=[])):
                if (
                    isinstance(child, ast.Call)
                    and isinstance(child.func, ast.Attribute)
                ):
                    finally_calls.append(child.func.attr)
        self.assertIn("closePort", finally_calls)

    def test_strict_self_check_passes(self) -> None:
        self.scanner.assert_source_is_read_only(SCANNER_PATH)

    def test_protocol_other_than_one_is_rejected_before_scan(self) -> None:
        args = self.scanner.parse_args(
            [
                "--port",
                "/dev/null",
                "--baudrate",
                "1000000",
                "--protocol-version",
                "2.0",
            ]
        )
        with self.assertRaises(ValueError):
            self.scanner.validate_arguments(args)

    def test_inventory_report_serializes_without_hardware(self) -> None:
        args = SimpleNamespace(
            port="/dev/serial/by-id/test-only",
            baudrate=1000000,
            protocol_version=1.0,
            start_id=0,
            end_id=253,
            repetitions=3,
            timeout_ms=None,
            compare_profile="phantomx_v2_kurte",
        )
        servo = self.scanner.empty_servo_result(2)
        servo["responses_ok"] = 3
        servo["stable"] = True
        servo["model_number"] = 12
        report = self.scanner.build_report(args, [servo])
        parsed = json.loads(self.scanner.render_report(report, "json"))
        self.assertEqual(1, parsed["summary"]["detected_count"])
        self.assertEqual([2], parsed["summary"]["stable_ids"])
        self.assertIn("comparison", parsed)


if __name__ == "__main__":
    unittest.main()
