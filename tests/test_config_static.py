import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ConfigStaticTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_root_document_is_minimal(self):
        main = re.sub(r"%.*", "", self.read("main.tex"))
        self.assertIn("\\documentclass{insr}", main)
        self.assertIn("\\INSRMakeTitle", main)
        self.assertIn("\\INSRRenderDocument", main)
        self.assertNotIn("document/target", main)

    def test_project_uses_two_dimensional_bootstrap(self):
        active = self.read("config/active-target.tex")
        project = self.read("config/project-config.tex")
        self.assertIn("document/type = position-paper", active)
        self.assertIn("output/target = paper", active)
        self.assertIn("document/type=position-paper", project)
        self.assertIn("output/target=paper", project)
        self.assertNotIn("document/target=position-paper", project)

    def test_publication_date_and_year_are_dynamic(self):
        publication = self.read("config/publication-config.tex")
        metadata = self.read("tex/latex/insr/insr-metadata.sty")
        self.assertIn("publication/date = {\\today}", publication)
        self.assertIn("publication/year = {\\number\\year}", publication)
        self.assertNotIn("publication/date = {14 July 2026}", publication)
        self.assertNotIn("{2026}", metadata)

    def test_registry_runtime_is_loaded(self):
        resolver = self.read("tex/latex/insr/insr-config.sty")
        for token in (
            "\\INSRRegisterDocumentType",
            "\\INSRRegisterDocumentAlias",
            "\\INSRRegisterOutputTarget",
            "\\INSRRegisterCombination",
            "config/target-registry.tex",
            "unknown-output-target",
        ):
            self.assertIn(token, resolver)

    def test_no_full_path_package_requests(self):
        paths = [ROOT / "insr.cls", *sorted((ROOT / "tex/latex/insr").glob("*.sty"))]
        pattern = re.compile(r"\\(?:RequirePackage|usepackage)\s*(?:\[[^]]*\])?\{tex/latex/insr/")
        for path in paths:
            self.assertIsNone(pattern.search(path.read_text(encoding="utf-8")), str(path))

    def test_class_options_processed_after_project_config(self):
        cls = self.read("insr.cls")
        self.assertLess(cls.index("config/project-config.tex"), cls.index("\\ProcessOptions"))
        self.assertIn("config/load-project=false", cls)

    def test_language_and_microtype_configuration_are_available(self):
        project = self.read("config/project-config.tex")
        config = self.read("tex/latex/insr/insr-config.sty")
        self.assertIn("localization/language = ngerman", project)
        self.assertIn("typography/microtype", config)


if __name__ == "__main__":
    unittest.main()
