import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ConfigLifecycleStaticTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_root_is_canonical(self):
        self.assertEqual(
            self.read("main.tex"),
            "\\documentclass{insr}\n\n\\begin{document}\n\n\\INSRMakeTitle\n\\INSRRenderDocument\n\n\\end{document}\n",
        )

    def test_project_config_position_paper_resolution_inputs(self):
        config = self.read("config/project-config.tex")
        active = self.read("config/active-target.tex")
        self.assertIn("\\INSRBootstrap", active)
        self.assertIn("document/type=position-paper", active)
        self.assertIn("output/target=paper", active)
        self.assertNotIn("document/type = position-paper", config)
        self.assertIn("design/theme =", config)
        self.assertIn("design/palette =", config)
        resolver = self.read("tex/latex/insr/insr-config.sty")
        self.assertIn("__insr_resolve_document_profile:", resolver)
        self.assertIn("__insr_resolve_output_target:", resolver)
        registry = self.read("config/target-registry.tex")
        self.assertIn("\\INSRRegisterDocumentType{position-paper}{profile=position-paper", registry)
        self.assertIn("\\INSRRegisterOutputTarget{paper}{base=scrartcl, adapter=paper}", registry)

    def test_class_options_processed_after_project_config(self):
        cls = self.read("insr.cls")
        self.assertLess(cls.index("config/project-config.tex"), cls.index("\\ProcessOptions"))
        self.assertIn("config/load-project=false", cls)

    def test_ordinary_metadata_spaces_are_documented_defaults(self):
        config_pkg = self.read("tex/latex/insr/insr-config.sty")
        self.assertIn("INSR Scientific Publishing Platform", config_pkg)
        self.assertIn("Independent translational research program", config_pkg)
        self.assertNotIn("INSR~Scientific", config_pkg)

    def test_language_alias_and_unknown_type_fallback(self):
        localization = self.read("tex/latex/insr/insr-localization.sty")
        resolver = self.read("tex/latex/insr/insr-config.sty")
        self.assertIn("localization/language=german normalized to ngerman", localization)
        self.assertIn("unknown-document-type", resolver)
        self.assertIn("unknown-document-type", resolver)

if __name__ == "__main__":
    unittest.main()
