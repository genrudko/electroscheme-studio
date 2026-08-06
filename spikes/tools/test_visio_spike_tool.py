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
CANONICAL = ROOT / "shared" / "fixtures" / "canonical-project.json"


class VisioFixtureTests(unittest.TestCase):
    def run_tool(self, *args: str) -> dict:
        result = subprocess.run(
            [sys.executable, str(TOOL), *args],
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_vsdx(self) -> None:
        result = self.run_tool("inspect", "vsdx", str(FIXTURES / "controlled-minimal.vsdx"))
        self.assertEqual(result["status"], "ok")
        self.assertIn("visio/pages/page1.xml", result["parts"])
        self.assertTrue({"1", "2", "3"}.issubset(set(result["sourceIds"])))

    def test_vssx(self) -> None:
        result = self.run_tool("inspect", "vssx", str(FIXTURES / "controlled-master.vssx"))
        self.assertEqual(result["status"], "ok")
        self.assertIn("visio/masters/master1.xml", result["parts"])
        self.assertIn("10", result["sourceIds"])

    def test_generated_package_structure(self) -> None:
        with zipfile.ZipFile(FIXTURES / "controlled-minimal.vsdx") as archive:
            self.assertIn("docProps/core.xml", archive.namelist())
            self.assertIn(b"Q-SPK-1", archive.read("visio/pages/page1.xml"))

    def test_fixtures_are_reproducible_byte_for_byte(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            generated = pathlib.Path(temporary)
            subprocess.run(
                [sys.executable, str(GENERATOR), str(generated), "--canonical", str(CANONICAL)],
                check=True,
            )
            for name in ("controlled-minimal.vsdx", "controlled-master.vssx"):
                expected = hashlib.sha256((FIXTURES / name).read_bytes()).hexdigest()
                actual = hashlib.sha256((generated / name).read_bytes()).hexdigest()
                self.assertEqual(actual, expected, name)

    def test_generate_vsdx_from_canonical_document(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = pathlib.Path(temporary) / "generated.vsdx"
            result = self.run_tool("generate-vsdx", str(CANONICAL), str(output))
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["canonicalProjectId"], "project-spike-0001")
            self.assertEqual(output.read_bytes(), (FIXTURES / "controlled-minimal.vsdx").read_bytes())


if __name__ == "__main__":
    unittest.main()
