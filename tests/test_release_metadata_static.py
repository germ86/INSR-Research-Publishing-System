import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReleaseMetadataStaticTests(unittest.TestCase):
    def test_reference_publication_entrypoints_exist_and_are_neutral(self):
        base = ROOT / "examples/reference-publication"
        for name in [
            "paper.tex",
            "slides.tex",
            "handout.tex",
            "poster.tex",
            "content/reference-body.tex",
            "references.bib",
        ]:
            self.assertTrue((base / name).is_file(), name)
        text = (base / "content/reference-body.tex").read_text(encoding="utf-8")
        self.assertIn("does not make clinical efficacy claims", text)
        self.assertNotIn("proves", text.lower())

    def test_metadata_exports_are_generated_without_pending_doi(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                ["python3", "tools/insr_metadata.py", "export-all", "--outdir", tmp],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            cff = Path(tmp, "CITATION.cff").read_text(encoding="utf-8")
            datacite = json.loads(Path(tmp, "datacite.json").read_text(encoding="utf-8"))
            codemeta = json.loads(Path(tmp, "codemeta.json").read_text(encoding="utf-8"))
            self.assertIn("Fabio Schmeil", cff)
            self.assertNotIn("doi: pending", cff.lower())
            self.assertNotIn("\\today", cff)
            self.assertNotIn("\\number\\year", cff)
            self.assertRegex(cff, r"date-released: \d{4}-\d{2}-\d{2}")
            self.assertIn("titles", datacite)
            self.assertRegex(str(datacite["publicationYear"]), r"^\d{4}$")
            self.assertEqual(codemeta["@type"], "SoftwareSourceCode")
            self.assertRegex(str(codemeta["datePublished"]), r"^\d{4}-\d{2}-\d{2}$")

    def test_release_prepare_creates_manifest(self):
        proc = subprocess.run(
            ["python3", "tools/insr_release.py", "prepare", "--version", "test-alpha"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        manifest = ROOT / "dist/insr-test-alpha/release-manifest.json"
        self.assertTrue(manifest.is_file())
        data = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(data["version"], "test-alpha")
        self.assertTrue(any(item["path"] == "metadata/CITATION.cff" for item in data["files"]))


if __name__ == "__main__":
    unittest.main()
