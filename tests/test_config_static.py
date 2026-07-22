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
        self.assertIn("document/type = position-paper", config)
        self.assertIn("design/theme = editorial", config)
        self.assertIn("design/palette = neuroclinical", config)
        resolver = self.read("tex/latex/insr/insr-config.sty")
        self.assertRegex(resolver, r"\{ position-paper \}.*\{ scrartcl \}.*\{ paper \}")

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
        self.assertRegex(resolver, r"unknown-document-type.*paper.*scrartcl.*paper")

    def test_build_profiles_are_normalized_and_set_placeholder_policy(self):
        config = self.read("tex/latex/insr/insr-config.sty")
        self.assertIn(r"document/build-profile .code:n = { \insr_build_profile_set:n {#1} }", config)
        self.assertIn(r"{ dev } { \__insr_set_development_profile: }", config)
        self.assertIn(r"{ release } { \__insr_set_production_profile: }", config)
        self.assertIn(r"\tl_gset:Nn \g_insr_content_placeholders_tl { compact }", config)
        self.assertIn(r"\tl_gset:Nn \g_insr_content_placeholders_tl { show }", config)
        self.assertIn(r"\tl_gset:Nn \g_insr_content_placeholders_tl { error }", config)

if __name__ == "__main__":
    unittest.main()
