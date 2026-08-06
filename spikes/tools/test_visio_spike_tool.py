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


def expected_hashes() -> dict[str, str]:
    result: dict[str, str] = {}
    for line in (FIXTURES / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, name = line.split(maxsplit=1)
        result[name.strip()] = digest
    return result


class VisioFixtureTests(unittest.TestCase):
    def run_tool(self, *args: str) -> dict:
        result = subprocess.run(
            [sys.executable, str(TOOL), *args],
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)

    def generate(self, directory: pathlib.Path) -> None:
        subprocess.run(
            [sys.executable, str(GENERATOR), str(directory), "--canonical", str(CANONICAL)],
            check=True,
        )

    def test_vsdx(self) -> None:
        result = self.run_tool("inspect", "vsdx", str(FIXTURES / "controlled-minimal.vsdx"))
        self.assertEqual(result["status"], "ok")
        self.assertIn("visio/pages/page1.xml", result["parts"])
        self.assertTrue({"1", "2", "3"}.issubset(set(result["sourceIds"])))

    def test_generated_vssx(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            generated = pathlib.Path(temporary)
            self.generate(generated)
            stencil = generated / "controlled-master.vssx"
            result = self.run_tool("inspect", "vssx", str(stencil))
            self.assertEqual(result["status"], "ok")
            self.assertIn("visio/masters/master1.xml", result["parts"])
            self.assertIn("10", result["sourceIds"])

    def test_generated_package_structure(self) -> None:
        with zipfile.ZipFile(FIXTURES / "controlled-minimal.vsdx") as archive:
            self.assertIn("docProps/core.xml", archive.namelist())
            self.assertIn(b"Q-SPK-1", archive.read("visio/pages/page1.xml"))

    def test_fixtures_are_reproducible_byte_for_byte(self) -> None:
        expected = expected_hashes()
        with tempfile.TemporaryDirectory() as temporary:
            generated = pathlib.Path(temporary)
            self.generate(generated)
            self.assertEqual(
                (generated / "controlled-minimal.vsdx").read_bytes(),
                (FIXTURES / "controlled-minimal.vsdx").read_bytes(),
            )
            for name in ("controlled-minimal.vsdx", "controlled-master.vssx"):
                actual = hashlib.sha256((generated / name).read_bytes()).hexdigest()
                self.assertEqual(actual, expected[name], name)

    def test_generate_vsdx_from_canonical_document(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = pathlib.Path(temporary) / "generated.vsdx"
            result = self.run_tool("generate-vsdx", str(CANONICAL), str(output))
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["canonicalProjectId"], "project-spike-0001")
            self.assertEqual(output.read_bytes(), (FIXTURES / "controlled-minimal.vsdx").read_bytes())


if __name__ == "__main__":
    unittest.main()
