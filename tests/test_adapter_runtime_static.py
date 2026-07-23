import importlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AdapterRuntimeStaticTests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def registered_output_adapters(self) -> dict[str, str]:
        registry = self.read("config/target-registry.tex")
        adapters = {}
        pattern = re.compile(r"\\INSRRegisterOutputTarget\{([^}]+)\}\{([^}]*)\}")
        for target, body in pattern.findall(registry):
            values = dict(part.strip().split("=", 1) for part in body.split(",") if "=" in part)
            adapters[target] = values["adapter"].strip()
        return adapters

    def test_every_registered_output_target_has_adapter_file(self):
        for target, adapter in self.registered_output_adapters().items():
            with self.subTest(target=target, adapter=adapter):
                self.assertTrue((ROOT / "framework" / "adapters" / f"{adapter}.tex").is_file())

    def test_specialized_targets_do_not_reuse_generic_paper_or_slides_adapters(self):
        adapters = self.registered_output_adapters()
        self.assertEqual(adapters["handout"], "handout")
        self.assertEqual(adapters["executive-brief"], "executive-brief")
        self.assertEqual(adapters["submission-package"], "submission-package")
        self.assertEqual(adapters["web"], "web")

        registry = self.read("config/target-registry.tex")
        self.assertIn(r"\INSRRegisterOutputTarget{handout}{base=beamer, adapter=handout, class-options=handout}", registry)
        self.assertIn(r"\INSRRegisterOutputTarget{executive-brief}{base=scrartcl, adapter=executive-brief}", registry)
        self.assertIn(r"\INSRRegisterOutputTarget{submission-package}{base=scrartcl, adapter=submission-package}", registry)
        self.assertIn(r"\INSRRegisterOutputTarget{web}{base=scrartcl, adapter=web}", registry)

    def test_integrity_reports_specialized_target_fallbacks_without_inherited_noise(self):
        import sys
        tools = ROOT / "tools"
        sys.path.insert(0, str(tools))
        import insr_integrity
        insr_integrity = importlib.reload(insr_integrity)

        integrity_source = self.read("tools/insr_integrity.py")
        self.assertIn('"handout": ["handout", "summary", "full", "key"]', integrity_source)
        self.assertIn('"executive-brief": ["executive", "summary", "full", "key"]', integrity_source)

        self.assertEqual(insr_integrity.adapter_fields("handout", "handout"), ["full", "handout", "key", "summary"])
        self.assertNotIn("notes", insr_integrity.adapter_fields("handout", "handout"))
        self.assertEqual(insr_integrity.adapter_fields("executive-brief", "executive-brief"), ["executive", "full", "key", "summary"])

    def test_specialized_adapters_expose_target_specific_fallbacks(self):
        expectations = {
            "handout": "handout,summary,full,key",
            "executive-brief": "executive,summary,full,key",
            "submission-package": "full,summary,key",
            "web": "summary,full,key",
            "poster": "poster,summary,key,full",
        }
        for adapter, fallback in expectations.items():
            with self.subTest(adapter=adapter):
                text = self.read(f"framework/adapters/{adapter}.tex")
                self.assertIn(fallback, text)
                self.assertIn("__insr_adapter_render_content_unit", text)


if __name__ == "__main__":
    unittest.main()
