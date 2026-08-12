from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("archive_candidate.py")


class ArchiveCandidateTests(unittest.TestCase):
    def create_package(self, root: Path) -> Path:
        package = root / "candidate-package"
        nested = package / "nested"
        nested.mkdir(parents=True)
        executable = package / ("candidate.exe" if os.name == "nt" else "candidate")
        executable.write_bytes(b"candidate-binary\n")
        if os.name != "nt":
            executable.chmod(0o755)
        (nested / "fixture.json").write_text('{"fixture":true}\n', encoding="utf-8")
        return package

    def archive(self, root: Path, package: Path, suffix: str) -> tuple[Path, dict[str, object]]:
        archive = root / f"candidate-{suffix}.tar.gz"
        manifest = root / f"candidate-{suffix}.json"
        subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "test-candidate",
                str(package),
                str(archive),
                str(manifest),
                "--base-root",
                str(root),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return archive, json.loads(manifest.read_text(encoding="utf-8"))

    def test_archive_is_deterministic_and_restores_package_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = self.create_package(root)
            archive_one, manifest_one = self.archive(root, package, "one")
            archive_two, manifest_two = self.archive(root, package, "two")

            self.assertEqual(archive_one.read_bytes(), archive_two.read_bytes())
            self.assertEqual(
                hashlib.sha256(archive_one.read_bytes()).hexdigest(),
                manifest_one["archive_sha256"],
            )
            self.assertEqual(manifest_one["archive_sha256"], manifest_two["archive_sha256"])
            self.assertEqual(manifest_one["unpacked_tree_sha256"], manifest_two["unpacked_tree_sha256"])
            self.assertTrue(manifest_one["artifact_layout_round_trip_verified"])
            self.assertEqual(manifest_one["package_root"], "candidate-package")
            self.assertTrue((package / "nested" / "fixture.json").is_file())
            if os.name != "nt":
                mode = stat.S_IMODE((package / "candidate").stat().st_mode)
                self.assertEqual(mode, 0o755)


if __name__ == "__main__":
    unittest.main()
