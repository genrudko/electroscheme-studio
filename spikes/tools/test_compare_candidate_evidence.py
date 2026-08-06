from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from tools.compare_candidate_evidence import build_snapshot, markdown


HEAD = "a" * 40
RUN = "123456"
NPM_LOCK = "b" * 64
CARGO_LOCK = "c" * 64
LOGICAL = {
    "canonical_json_sha256": "d" * 64,
    "clipboard_sha256": "e" * 64,
    "pdf_sha256": "f" * 64,
}
VISIO = {
    "controlled_vsdx_sha256": "1" * 64,
    "controlled_vssx_sha256": "2" * 64,
    "generated_vsdx_sha256": "3" * 64,
}


class CompareCandidateEvidenceTests(unittest.TestCase):
    def write_platform(self, root: Path, platform_name: str) -> None:
        generated = root / f"desktop-spike-{platform_name}" / "evidence" / "generated"
        generated.mkdir(parents=True)
        manifests = {}
        packages = {}
        for index, candidate in enumerate(("electron", "tauri"), start=1):
            manifests[candidate] = {
                "candidate": candidate,
                "archive_path": f"evidence/generated/archives/{candidate}-{platform_name}.tar.gz",
                "archive_sha256": str(index) * 64,
                "archive_size_bytes": index * 1_000_000,
                "package_root": f"evidence/generated/{candidate}-{platform_name}",
                "unpacked_tree_sha256": str(index + 3) * 64,
                "unpacked_size_bytes": index * 10_000_000,
                "unpacked_file_count": index * 10,
                "artifact_layout_round_trip_verified": True,
            }
            packages[candidate] = {
                key: manifests[candidate][key]
                for key in (
                    "archive_path",
                    "archive_sha256",
                    "archive_size_bytes",
                    "package_root",
                    "unpacked_tree_sha256",
                    "unpacked_size_bytes",
                    "unpacked_file_count",
                )
            }
            scenario = {
                "candidate": candidate,
                "status": "ok",
                "checks": {"canonical_read": True, "generated_vsdx_package_read": True},
                "hashes": dict(LOGICAL),
                "tool_results": {
                    "vsdx": {"status": "ok", "sha256": VISIO["controlled_vsdx_sha256"]},
                    "vssx": {"status": "ok", "sha256": VISIO["controlled_vssx_sha256"]},
                    "generated": {"status": "ok", "sha256": VISIO["generated_vsdx_sha256"]},
                    "generatedInspection": {"status": "ok", "sha256": VISIO["generated_vsdx_sha256"]},
                },
                "harness": {
                    "package_evidence": {
                        "artifact_layout_round_trip_verified": True,
                        "launched_from_verified_package_root": True,
                    }
                },
            }
            runtime = {
                "candidate": candidate,
                "startup_to_renderer_ready_ms": 100.0 * index,
                "idle_process_tree_rss_bytes": 50_000_000 * index,
                "measurement_root_pid": 1000 + index,
                "package_evidence": {
                    "artifact_layout_round_trip_verified": True,
                    "launched_from_verified_package_root": True,
                },
            }
            (generated / f"{candidate}-scenario-{platform_name}.json").write_text(
                json.dumps(scenario), encoding="utf-8"
            )
            (generated / f"{candidate}-runtime-{platform_name}.json").write_text(
                json.dumps(runtime), encoding="utf-8"
            )
        measurements = {
            "workflow_run_id": RUN,
            "exact_head": HEAD,
            "artifact_name": f"desktop-spike-{platform_name}",
            "runner_os": platform_name,
            "runner_architecture": "x86_64",
            "python": "3.13",
            "node": "v24.19.0",
            "npm": "11",
            "rustc": "1.97.1",
            "cargo": "1.97.1",
            "package_manifests": manifests,
            "package_size_json": f"evidence/generated/package-sizes-{platform_name}.json",
            "npm_lock_sha256": NPM_LOCK,
            "cargo_lock_sha256": CARGO_LOCK,
        }
        package_sizes = {
            "protocol": "electroscheme-package-sizes/1",
            "workflow_run_id": RUN,
            "exact_head": HEAD,
            "artifact_name": f"desktop-spike-{platform_name}",
            "npm_lock_sha256": NPM_LOCK,
            "cargo_lock_sha256": CARGO_LOCK,
            "packages": packages,
        }
        (generated / f"measurements-{platform_name}.json").write_text(
            json.dumps(measurements), encoding="utf-8"
        )
        (generated / f"package-sizes-{platform_name}.json").write_text(
            json.dumps(package_sizes), encoding="utf-8"
        )

    def fixture_root(self) -> tempfile.TemporaryDirectory[str]:
        return tempfile.TemporaryDirectory()

    def test_builds_one_cross_platform_snapshot(self) -> None:
        with self.fixture_root() as temporary:
            root = Path(temporary)
            self.write_platform(root, "windows")
            self.write_platform(root, "linux")
            result = build_snapshot(root, HEAD, RUN)
            self.assertEqual(result["exact_head"], HEAD)
            self.assertEqual(result["workflow_run_id"], RUN)
            self.assertEqual(result["logical_output_sha256"], LOGICAL)
            self.assertEqual(result["visio_sha256"], VISIO)
            self.assertTrue(result["cross_candidate_platform_logical_equality_verified"])
            self.assertEqual(result["platforms"]["linux"]["candidates"]["electron"]["scenario_status"], "ok")
            rendered = markdown(result)
            self.assertIn("OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED", json.dumps(result))
            self.assertIn("| linux | electron |", rendered)
            self.assertIn("not universal benchmarks", rendered)
            self.assertIn(LOGICAL["canonical_json_sha256"], rendered)

    def test_rejects_mixed_exact_heads(self) -> None:
        with self.fixture_root() as temporary:
            root = Path(temporary)
            self.write_platform(root, "windows")
            self.write_platform(root, "linux")
            path = next(root.rglob("measurements-linux.json"))
            data = json.loads(path.read_text(encoding="utf-8"))
            data["exact_head"] = "9" * 40
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "package sizes: exact_head"):
                build_snapshot(root)

    def test_rejects_divergent_logical_output(self) -> None:
        with self.fixture_root() as temporary:
            root = Path(temporary)
            self.write_platform(root, "windows")
            self.write_platform(root, "linux")
            path = next(root.rglob("electron-scenario-linux.json"))
            data = json.loads(path.read_text(encoding="utf-8"))
            data["hashes"]["pdf_sha256"] = "8" * 64
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "pdf_sha256 differs"):
                build_snapshot(root)

    def test_rejects_generated_vsdx_changed_before_inspection(self) -> None:
        with self.fixture_root() as temporary:
            root = Path(temporary)
            self.write_platform(root, "windows")
            self.write_platform(root, "linux")
            path = next(root.rglob("tauri-scenario-windows.json"))
            data = json.loads(path.read_text(encoding="utf-8"))
            data["tool_results"]["generatedInspection"]["sha256"] = "7" * 64
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "changed between generation and package inspection"):
                build_snapshot(root)


if __name__ == "__main__":
    unittest.main()
