import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class TargetDimensionStaticTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_bootstrap_uses_separate_document_type_and_output_target(self):
        active = self.read("config/active-target.tex")
        self.assertIn("document/type=position-paper", active)
        self.assertIn("output/target=paper", active)
        self.assertNotIn("document/target=position-paper", active)

    def test_resolver_no_longer_copies_output_target_to_document_type(self):
        config = self.read("tex/latex/insr/insr-config.sty")
        self.assertNotIn("tl_gset_eq:NN \\g_insr_document_type_tl \\g_insr_output_target_tl", config)
        self.assertIn("__insr_resolve_document_profile", config)
        self.assertIn("__insr_resolve_output_target", config)
        self.assertRegex(config, r"\{ rct-protocol \}.*\{ rct-protocol \}")
        self.assertRegex(config, r"\{ slides \}.*\{ beamer \}.*\{ slides \}")

    def test_auto_content_source_and_protocol_profiles_exist(self):
        config = self.read("config/project-config.tex")
        self.assertIn("content/source = auto", config)
        self.assertTrue((ROOT / "profiles/documents/rct-protocol.profile.tex").is_file())
        self.assertTrue((ROOT / "profiles/documents/clinical-protocol.profile.tex").is_file())
        self.assertTrue((ROOT / "content/rct-protocol/manifest.tex").is_file())
        self.assertTrue((ROOT / "content/clinical-protocol/manifest.tex").is_file())

if __name__ == "__main__":
    unittest.main()
