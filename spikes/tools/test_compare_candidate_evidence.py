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


class CompareCandidateEvidenceTests(unittest.TestCase):
    def write_platform(self, root: Path, platform_name: str) -> None:
        generated = root / f"desktop-spike-{platform_name}" / "evidence" / "generated"
        generated.mkdir(parents=True)
        manifests = {}
        for index, candidate in enumerate(("electron", "tauri"), start=1):
            manifests[candidate] = {
                "candidate": candidate,
                "archive_path": f"evidence/generated/archives/{candidate}-{platform_name}.tar.gz",
                "archive_sha256": str(index) * 64,
                "archive_size_bytes": index * 1_000_000,
                "package_root": f"evidence/generated/{candidate}-{platform_name}",
                "unpacked_tree_sha256": str(index + 2) * 64,
                "unpacked_size_bytes": index * 10_000_000,
                "unpacked_file_count": index * 10,
                "artifact_layout_round_trip_verified": True,
            }
            scenario = {
                "candidate": candidate,
                "status": "ok",
                "checks": {"canonical_read": True, "generated_vsdx_package_read": True},
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
            "npm_lock_sha256": NPM_LOCK,
            "cargo_lock_sha256": CARGO_LOCK,
        }
        (generated / f"measurements-{platform_name}.json").write_text(
            json.dumps(measurements), encoding="utf-8"
        )

    def test_builds_one_cross_platform_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_platform(root, "windows")
            self.write_platform(root, "linux")
            result = build_snapshot(root, HEAD, RUN)
            self.assertEqual(result["exact_head"], HEAD)
            self.assertEqual(result["workflow_run_id"], RUN)
            self.assertEqual(result["platforms"]["linux"]["candidates"]["electron"]["scenario_status"], "ok")
            rendered = markdown(result)
            self.assertIn("OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED", json.dumps(result))
            self.assertIn("| linux | electron |", rendered)
            self.assertIn("not universal benchmarks", rendered)

    def test_rejects_mixed_exact_heads(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_platform(root, "windows")
            self.write_platform(root, "linux")
            path = next(root.rglob("measurements-linux.json"))
            data = json.loads(path.read_text(encoding="utf-8"))
            data["exact_head"] = "d" * 40
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "one exact head"):
                build_snapshot(root)


if __name__ == "__main__":
    unittest.main()
