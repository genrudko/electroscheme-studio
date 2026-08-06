import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "visio_spike_tool.py"
GENERATOR = ROOT / "tools" / "generate_controlled_visio_fixtures.py"
FIXTURES = ROOT / "shared" / "fixtures" / "visio"


class VisioFixtureTests(unittest.TestCase):
    def inspect(self, kind: str, name: str) -> dict:
        result = subprocess.run(
            [sys.executable, str(TOOL), "inspect", kind, str(FIXTURES / name)],
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_vsdx(self) -> None:
        result = self.inspect("vsdx", "controlled-minimal.vsdx")
        self.assertEqual(result["status"], "ok")
        self.assertIn("visio/pages/page1.xml", result["parts"])
        self.assertTrue({"1", "2", "3"}.issubset(set(result["sourceIds"])))

    def test_vssx(self) -> None:
        result = self.inspect("vssx", "controlled-master.vssx")
        self.assertEqual(result["status"], "ok")
        self.assertIn("visio/masters/master1.xml", result["parts"])

    def test_generated_package_structure(self) -> None:
        with zipfile.ZipFile(FIXTURES / "controlled-minimal.vsdx") as archive:
            self.assertIn("docProps/core.xml", archive.namelist())

    def test_fixtures_are_reproducible_byte_for_byte(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            generated = pathlib.Path(temporary)
            subprocess.run([sys.executable, str(GENERATOR), str(generated)], check=True)
            for name in ("controlled-minimal.vsdx", "controlled-master.vssx"):
                expected = hashlib.sha256((FIXTURES / name).read_bytes()).hexdigest()
                actual = hashlib.sha256((generated / name).read_bytes()).hexdigest()
                self.assertEqual(actual, expected, name)


if __name__ == "__main__":
    unittest.main()
