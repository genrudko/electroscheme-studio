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


def rewrite_zip(source: pathlib.Path, destination: pathlib.Path, replacements: dict[str, bytes]) -> None:
    with zipfile.ZipFile(source) as input_archive, zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as output_archive:
        for item in input_archive.infolist():
            payload = replacements.get(item.filename, input_archive.read(item.filename))
            output_archive.writestr(item, payload)


class VisioFixtureTests(unittest.TestCase):
    def run_tool_process(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def run_tool(self, *args: str) -> dict:
        result = self.run_tool_process(*args)
        if result.returncode != 0:
            self.fail(f"tool failed rc={result.returncode}: {result.stderr}\n{result.stdout}")
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
        self.assertEqual(result["diagnostics"], [])

    def test_generated_vssx(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            generated = pathlib.Path(temporary)
            self.generate(generated)
            stencil = generated / "controlled-master.vssx"
            result = self.run_tool("inspect", "vssx", str(stencil))
            self.assertEqual(result["status"], "ok")
            self.assertIn("visio/masters/master1.xml", result["parts"])
            self.assertIn("10", result["sourceIds"])
            self.assertEqual(result["diagnostics"], [])

    def test_generated_package_structure(self) -> None:
        with zipfile.ZipFile(FIXTURES / "controlled-minimal.vsdx") as archive:
            self.assertIn("docProps/app.xml", archive.namelist())
            self.assertIn(b"<AppVersion>01.0000</AppVersion>", archive.read("docProps/app.xml"))
            self.assertIn(b"<Rel r:id=\"rId1\"/>", archive.read("visio/pages/pages.xml"))
            self.assertNotIn(b"<Pages r:id=", archive.read("visio/document.xml"))
            page = archive.read("visio/pages/page1.xml")
            self.assertIn(b"Q-SPK-1", page)
            self.assertIn(b"<Cell N=\"BeginX\"", page)
            self.assertIn(b"<Cell N=\"EndX\"", page)

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

    def test_legacy_invalid_vsdx_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = pathlib.Path(temporary)
            self.generate(directory)
            source = directory / "controlled-minimal.vsdx"
            broken = directory / "legacy-invalid.vsdx"
            bad_document = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<VisioDocument xmlns="http://schemas.microsoft.com/office/visio/2012/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><DocumentProperties/><Pages r:id="rId1"/></VisioDocument>'''
            bad_pages = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Pages xmlns="http://schemas.microsoft.com/office/visio/2012/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><Page ID="0" NameU="Page-1" Name="Page-1" r:id="rId1"/></Pages>'''
            rewrite_zip(source, broken, {"visio/document.xml": bad_document, "visio/pages/pages.xml": bad_pages})
            process = self.run_tool_process("inspect", "vsdx", str(broken))
            self.assertEqual(process.returncode, 2)
            result = json.loads(process.stdout)
            self.assertEqual(result["status"], "invalid")
            codes = {item["code"] for item in result["diagnostics"]}
            self.assertIn("INLINE_PAGES_RELATION_INVALID", codes)
            self.assertIn("PAGE_REL_INVALID", codes)
            self.assertIn("PAGE_REL_ATTRIBUTE_INVALID", codes)

    def test_dangling_relationship_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = pathlib.Path(temporary)
            self.generate(directory)
            source = directory / "controlled-minimal.vsdx"
            broken = directory / "dangling.vsdx"
            bad_rels = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="missing-page.xml"/></Relationships>'''
            rewrite_zip(source, broken, {"visio/pages/_rels/pages.xml.rels": bad_rels})
            process = self.run_tool_process("inspect", "vsdx", str(broken))
            self.assertEqual(process.returncode, 2)
            result = json.loads(process.stdout)
            self.assertEqual(result["status"], "invalid")
            codes = {item["code"] for item in result["diagnostics"]}
            self.assertIn("DANGLING_RELATIONSHIP", codes)
            self.assertIn("REQUIRED_RELATIONSHIP_MISSING", codes)

    def test_nonconformant_app_version_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = pathlib.Path(temporary)
            self.generate(directory)
            source = directory / "controlled-minimal.vsdx"
            broken = directory / "bad-app-version.vsdx"
            with zipfile.ZipFile(source) as archive:
                bad_app = archive.read("docProps/app.xml").replace(
                    b"<AppVersion>01.0000</AppVersion>",
                    b"<AppVersion>0.1</AppVersion>",
                )
            rewrite_zip(source, broken, {"docProps/app.xml": bad_app})
            process = self.run_tool_process("inspect", "vsdx", str(broken))
            self.assertEqual(process.returncode, 2)
            result = json.loads(process.stdout)
            self.assertEqual(result["status"], "invalid")
            diagnostics = [item for item in result["diagnostics"] if item["code"] == "APP_VERSION_INVALID"]
            self.assertEqual(len(diagnostics), 1)
            self.assertEqual(diagnostics[0]["value"], "0.1")
            self.assertEqual(diagnostics[0]["expectedFormat"], "XX.YYYY")


if __name__ == "__main__":
    unittest.main()
