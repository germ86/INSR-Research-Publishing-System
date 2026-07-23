import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TargetDimensionStaticTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_bootstrap_uses_canonical_build_preset(self):
        active = self.read("config/active-target.tex")
        self.assertIn("build/preset = position-paper", active)
        self.assertNotIn("document/type", active)
        self.assertNotIn("output/target", active)
        self.assertNotIn("document/target=position-paper", active)

    def test_resolver_is_registry_driven(self):
        config = self.read("tex/latex/insr/insr-config.sty")
        self.assertIn("config/target-registry.tex", config)
        self.assertIn("\\INSRRegisterDocumentType", config)
        self.assertIn("\\INSRRegisterOutputTarget", config)
        self.assertIn("\\INSRRegisterCombination", config)
        self.assertIn("__insr_resolve_document_profile", config)
        self.assertIn("__insr_resolve_output_target", config)
        self.assertIn("unknown-output-target", config)
        self.assertNotIn("tl_gset_eq:NN \\g_insr_document_type_tl \\g_insr_output_target_tl", config)

    def test_auto_content_source_and_protocol_profiles_exist(self):
        config = self.read("config/project-config.tex")
        self.assertIn("content/source = auto", config)
        self.assertTrue((ROOT / "profiles/documents/rct-protocol.profile.tex").is_file())
        self.assertTrue((ROOT / "profiles/documents/clinical-protocol.profile.tex").is_file())
        self.assertTrue((ROOT / "content/rct-protocol/manifest.tex").is_file())
        self.assertTrue((ROOT / "content/clinical-protocol/manifest.tex").is_file())

    def test_registry_contains_cross_output_protocol_combinations(self):
        registry = self.read("config/target-registry.tex")
        for combination in (
            "rct-protocol-slides",
            "rct-protocol-handout",
            "clinical-protocol-slides",
            "clinical-protocol-handout",
        ):
            self.assertIn(f"\\INSRRegisterCombination{{{combination}}}", registry)

    def test_document_types_have_registered_default_output_combinations(self):
        registry = self.read("config/target-registry.tex")
        expected = {
            "manual": "target=manual",
            "report": "target=report",
            "book": "target=book",
            "monograph": "target=book",
            "thesis": "target=thesis",
            "letter": "target=letter",
            "technical-documentation": "target=report",
            "developer-documentation": "target=report",
            "systematic-review": "target=report",
            "narrative-review": "target=report",
            "grant-proposal": "target=report",
            "protocol": "target=report",
        }
        for name, target in expected.items():
            self.assertIn(f"\\INSRRegisterCombination{{{name}}}", registry)
            self.assertIn(target, registry)


if __name__ == "__main__":
    unittest.main()
