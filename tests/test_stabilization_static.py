import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class StabilizationStaticTests(unittest.TestCase):
    def read(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_l3build_authoritative_config_and_shim(self):
        build = self.read("build.lua")
        self.assertIn("Authoritative l3build configuration", build)
        self.assertIn('ctanpkg = "insr"', build)
        self.assertIn('testfiledir = "testfiles"', build)
        self.assertIn('uploadconfig = {', build)
        self.assertIn('https://github.com/germ86/INSR-Research-Publishing-System', build)
        self.assertFalse((ROOT / "l3build.lua").exists())

    def test_version_source_controls_secondary_versions(self):
        version = json.loads(self.read("insr-version.json"))
        self.assertEqual(version["version"], "0.1.0")
        self.assertEqual(version["schema_version"], "1.0")
        self.assertIn(version["repository"], self.read("build.lua"))
        self.assertIn('SCHEMA_VERSION = load_version()["schema_version"]', self.read("tools/insr_cli.py"))
        self.assertEqual(json.loads(self.read("schema/insr-project.schema.json"))["properties"]["schema_version"]["const"], version["schema_version"])

    def test_plugin_dependency_conflict_cycle_diagnostics_exist(self):
        core = self.read("tex/latex/insr/insr-core.sty")
        for token in ["plugin-missing-dependency", "plugin-conflict", "plugin-cycle", "plugin-core-version", "dependencies .clist_set:N", "conflicts .clist_set:N"]:
            self.assertIn(token, core)
        registry = self.read("config/plugin-registry.tex")
        self.assertIn("dependencies=accessibility", registry)
        self.assertIn("conflicts=poster", registry)

    def test_theme_and_fontset_resolution_are_connected(self):
        core = self.read("tex/latex/insr/insr-core.sty")
        config = self.read("tex/latex/insr/insr-config.sty")
        self.assertIn("\\g__insr_theme_palette_prop", core)
        self.assertIn("\\g_insr_layout_header_separator_style_tl", core)
        self.assertIn("\\insr_fontset_activate:n", core)
        self.assertIn("design/theme .code:n = { \\insr_theme_activate:n", config)
        self.assertIn("typography/fontset .code:n = { \\insr_fontset_activate:n", config)
        self.assertTrue((ROOT / "config/fontset-registry.tex").is_file())

    def test_required_l3build_regression_files_exist(self):
        required = [
            "canonical-configuration", "legacy-key-aliases", "target-resolution", "unknown-target",
            "theme-registration", "theme-activation", "unknown-theme", "plugin-registration",
            "plugin-loading", "duplicate-plugin-loading", "plugin-dependency", "missing-plugin-dependency",
            "plugin-conflict", "localization-fallback", "metadata-storage", "build-preset-resolution",
        ]
        for name in required:
            self.assertTrue((ROOT / "testfiles" / f"{name}.lvt").is_file(), name)
            self.assertTrue((ROOT / "testfiles" / f"{name}.tlg").is_file(), name)

    def test_ci_runs_l3build_and_ctan_smoke(self):
        ci = self.read(".github/workflows/ci.yml")
        self.assertIn("l3build check", ci)
        self.assertIn("l3build ctan", ci)
        self.assertIn("unzip -l", ci)
        self.assertIn("upload-artifact", ci)

if __name__ == "__main__":
    unittest.main()
