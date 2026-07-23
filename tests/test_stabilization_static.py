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
        self.assertIn('"insr.cls"', build)
        self.assertIn('"templates/*.tex"', build)
        self.assertIn('["config"] = "tex/latex/insr/config"', build)
        self.assertIn('["templates"] = "tex/latex/insr/templates"', build)
        self.assertIn('testfiledir = "testfiles"', build)
        self.assertIn('uploadconfig = {', build)
        self.assertIn('https://github.com/germ86/INSR-Research-Publishing-System', build)
        self.assertFalse((ROOT / "l3build.lua").exists())

    def test_installed_package_harness_exists(self):
        script = self.read("scripts/test-installed-package.sh")
        self.assertIn("TEXMFHOME", script)
        self.assertIn('kpsewhich "$f"', script)
        self.assertIn("insr.cls", script)
        self.assertIn("config/target-registry.tex", script)
        self.assertIn("unset TEXINPUTS BIBINPUTS", script)
        self.assertIn("latexmk -lualatex", script)

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
        self.assertIn("design/theme .code:n", config)
        self.assertIn("\\insr_theme_activate:n", config)
        self.assertIn("typography/fontset .code:n", config)
        self.assertIn("\\insr_fontset_activate:n", config)
        self.assertTrue((ROOT / "config/fontset-registry.tex").is_file())


    def test_each_typography_preset_is_registered(self):
        registry = self.read("config/fontset-registry.tex")
        registered = set(re.findall(r"\\insr_fontset_register:nn \{ ([^}]+) \}", registry))
        presets = {path.stem for path in (ROOT / "typography").glob("*.tex")}
        self.assertTrue(presets)
        self.assertTrue(presets.issubset(registered), presets - registered)

    def test_public_configuration_commands_preserve_explsyntax_state(self):
        config = self.read("tex/latex/insr/insr-config.sty")
        for command in ("INSRConfigure", "INSRBootstrap", "INSRProfileDefaults"):
            match = re.search(rf"\\NewDocumentCommand \\{command} [^\n]+", config)
            self.assertIsNotNone(match, command)
            body = match.group(0)
            self.assertIn("\\keys_set:nn", body)
            self.assertNotIn("\\ExplSyntaxOn", body)
            self.assertNotIn("\\ExplSyntaxOff", body)


    def test_registered_themes_have_runtime_files(self):
        registry = self.read("config/theme-registry.tex")
        registered = re.findall(r"\\insr_theme_register:nn \{ ([^}]+) \}", registry)
        self.assertTrue(registered)
        for theme in registered:
            self.assertTrue((ROOT / f"themes/{theme}.tex").is_file(), theme)

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
        self.assertIn("bash scripts/test-installed-package.sh", ci)
        self.assertIn("unzip -l", ci)
        self.assertIn("upload-artifact", ci)

    def test_legacy_latex_workflow_status_is_preserved(self):
        workflow = self.read(".github/workflows/latex.yml")
        self.assertIn("name: Build LaTeX", workflow)
        self.assertIn("xu-cheng/latex-action@v3", workflow)
        self.assertIn("examples/paper-demo.tex", workflow)
        self.assertIn("latexmk_use_lualatex: true", workflow)

    def test_multi_output_content_fields_have_runtime_fallbacks(self):
        content = self.read("tex/latex/insr/insr-content.sty")
        for token in ("handout,summary,full,key", "poster,summary,key,full", "executive,summary,full,key", "clinical,safety,full,summary,key", "methods,limitations,full,summary,key"):
            self.assertIn(token, content)
        self.assertIn("__insr_render_first_available:n", content)
        slides = self.read("framework/adapters/slides.tex")
        poster = self.read("framework/adapters/poster.tex")
        self.assertIn("handout,summary,full,key", slides)
        self.assertIn(r"\note", slides)
        self.assertIn("poster,summary,key,full", poster)

    def test_typography_font_helpers_exist(self):
        typography = self.read("tex/latex/insr/insr-typography.sty")
        for helper in (
            "__insr_typography_set_main_font:nn",
            "__insr_typography_set_sans_font:nn",
            "__insr_typography_set_mono_font:nn",
        ):
            self.assertIn(helper, typography)
        self.assertIn(r"\setmainfont", typography)
        self.assertIn(r"\setsansfont", typography)
        self.assertIn(r"\setmonofont", typography)

    def test_test_runner_uses_isolated_compile_output_dirs_and_log_checks(self):
        runner = self.read("tests/run-tests.sh")
        self.assertIn('output_dir="build/compile/${document%.*}"', runner)
        self.assertIn('-outdir="$output_dir"', runner)
        self.assertIn("tools/check_latex_log.py", runner)
        self.assertIn("python3 -m unittest discover -s tests", runner)

    def test_validator_ignores_generated_build_trees(self):
        validator = self.read("tools/validate_project.py")
        self.assertIn('IGNORED_GENERATED_DIRS = {".git", "build", "dist", "tmp", "release", "test-output", ".l3build", "__pycache__"}', validator)
        self.assertIn("is_generated_path", validator)

    def test_l3build_uses_portable_line_width(self):
        build = self.read("build.lua")
        self.assertIn("maxprintline = 10000", build)

    def test_integrity_tool_exists_and_reports_runtime_status(self):
        tool = self.read("tools/insr_integrity.py")
        self.assertIn("Registry-to-runtime integrity audit", tool)
        self.assertIn("supported", tool)
        self.assertIn("incomplete", tool)
        self.assertIn("broken", tool)
        self.assertIn("framework", tool)
        self.assertIn("templates", tool)
        self.assertIn("content_fields_by_adapter", tool)

    def test_canonical_active_target_uses_build_preset(self):
        active = self.read("config/active-target.tex")
        self.assertIn("build/preset = position-paper", active)
        self.assertNotIn("document/type", active)
        self.assertNotIn("output/target", active)

if __name__ == "__main__":
    unittest.main()
