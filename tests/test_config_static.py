import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAMES = [
    "insr-core",
    "insr-config",
    "insr-metadata",
    "insr-utils",
    "insr-localization",
    "insr-bibliography",
    "insr-typography",
    "insr-colors",
    "insr-layout",
    "insr-frontmatter",
    "insr-page-style",
    "insr-boxes",
    "insr-accessibility",
    "insr-neuro",
    "insr-content",
    "insr-adapters",
]


class ConfigStaticTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_root_document_is_minimal(self):
        main = re.sub(r"%.*", "", self.read("main.tex"))
        self.assertIn("\\documentclass{insr}", main)
        self.assertIn("\\INSRMakeTitle", main)
        self.assertIn("\\INSRRenderDocument", main)
        self.assertNotIn("\\INSRBootstrap", main)
        self.assertNotIn("document/target", main)
        self.assertNotIn("output/target", main)
        self.assertNotIn("build/preset", main)

    def test_active_build_uses_one_pre_class_selector(self):
        active = self.read("config/active-target.tex")
        project = self.read("config/project-config.tex")
        self.assertIn("document/target = rct-protocol", active)
        self.assertNotIn("document/type", active)
        self.assertNotIn("output/target", active)
        self.assertNotIn("build/preset", active)
        self.assertIn("document/target=position-paper", project)
        self.assertNotIn("document/type=position-paper", project)
        self.assertNotIn("output/target=paper", project)
        self.assertNotIn("build/preset", project)

    def test_rct_combination_is_canonicalized_when_used_as_output_target(self):
        registry = self.read("config/target-registry.tex")
        compatibility = self.read("config/target-compatibility.tex")
        fixture = self.read("tests/fixtures/rct-combination-as-output-target.tex")
        profile = self.read("profiles/documents/rct-protocol.profile.tex")
        self.assertIn("config/target-compatibility.tex", registry)
        self.assertIn("\\__insr_set_output_target_compat:n", compatibility)
        self.assertIn("\\g__insr_combination_target_prop", compatibility)
        self.assertIn("\\tl_gset_eq:NN \\g_insr_output_target_tl \\l_tmpa_tl", compatibility)
        self.assertNotIn("\\INSRRegisterOutputTarget{rct-protocol}", registry)
        self.assertIn("document/type=rct-protocol", fixture)
        self.assertIn("output/target=rct-protocol", fixture)
        self.assertIn("outputs = {paper}", fixture)
        self.assertIn("Randomized~controlled~trial~protocol", profile)

    def test_build_preset_and_slide_shorthand_are_resolved(self):
        resolver = self.read("tex/latex/insr/insr-config.sty")
        for token in (
            "build/preset",
            "\\__insr_set_build_preset:n",
            "\\__insr_apply_document_type_preset_shorthand:",
            "\\__insr_resolve_output_target:",
        ):
            self.assertIn(token, resolver)
        self.assertLess(
            resolver.index("\\__insr_apply_document_type_preset_shorthand:"),
            resolver.rindex("\\__insr_resolve_output_target:"),
        )

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

    def test_root_shims_are_canonical(self):
        for package in PACKAGE_NAMES:
            shim = self.read(f"{package}.sty")
            expected = (
                "% INSR source-tree compatibility shim for Overleaf and local builds.\n"
                f"\\input{{tex/latex/insr/{package}.sty}}\n"
                "\\endinput\n"
            )
            self.assertEqual(shim, expected, package)
            implementation = self.read(f"tex/latex/insr/{package}.sty")
            self.assertIn(f"\\ProvidesPackage{{{package}}}", implementation)

    def test_class_does_not_mutate_input_path(self):
        cls = self.read("insr.cls")
        self.assertNotIn("\\input@path", cls)
        self.assertNotIn("local package path:", cls)
        for package in PACKAGE_NAMES:
            self.assertIn(f"\\RequirePackage{{{package}}}", cls)

    def test_texinputs_prefers_root_shims(self):
        latexmkrc = self.read("latexmkrc")
        workflow = self.read(".github/workflows/latex.yml")
        runner = self.read("tests/run-tests.sh")
        self.assertIn("$ENV{'TEXINPUTS'} = '.:./examples//:'", latexmkrc)
        self.assertNotIn("./tex/latex/insr//", latexmkrc)
        self.assertIn("TEXINPUTS: .:./examples//:", workflow)
        self.assertNotIn("TEXINPUTS: .//:./tex/latex/insr//", workflow)
        self.assertIn('export TEXINPUTS=".:./examples//:', runner)
        self.assertNotIn("./tex/latex/insr//", runner)

    def test_class_options_processed_after_project_config(self):
        cls = self.read("insr.cls")
        self.assertLess(cls.index("config/project-config.tex"), cls.index("\\ProcessOptions"))
        self.assertIn("config/load-project=false", cls)

    def test_language_and_microtype_configuration_are_available(self):
        project = self.read("config/project-config.tex")
        config = self.read("tex/latex/insr/insr-config.sty")
        localization = self.read("tex/latex/insr/insr-localization.sty")
        self.assertIn("localization/language = english", project)
        self.assertIn("babelprovide[import,main]{ngerman}", localization)
        self.assertIn("typography/microtype", config)


if __name__ == "__main__":
    unittest.main()
