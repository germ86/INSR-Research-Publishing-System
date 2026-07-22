import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import insr_build
import insr_integrity


class RuntimeBuildHardeningTests(unittest.TestCase):
    def setUp(self):
        self.combo = "position-paper"
        self.build_root = insr_build.compile_root(self.combo)
        shutil.rmtree(self.build_root, ignore_errors=True)
        self.before = insr_build.versioned_config_hashes()

    def tearDown(self):
        shutil.rmtree(self.build_root, ignore_errors=True)
        self.assertEqual(self.before, insr_build.versioned_config_hashes())

    def test_public_config_commands_do_not_toggle_explsyntax_at_runtime(self):
        config = (ROOT / "tex/latex/insr/insr-config.sty").read_text(encoding="utf-8")
        for command in ("INSRConfigure", "INSRBootstrap", "INSRProfileDefaults"):
            marker = f"\\NewDocumentCommand \\{command}"
            start = config.index(marker)
            body = config[start : config.index("\n", start)]
            self.assertNotIn("\\ExplSyntaxOn", body)
            self.assertNotIn("\\ExplSyntaxOff", body)
            self.assertIn("\\keys_set:nn", body)

    def test_profile_defaults_no_longer_requires_profile_workaround(self):
        profile = (ROOT / "profiles/documents/rct-protocol.profile.tex").read_text(encoding="utf-8")
        self.assertIn("\\INSRProfileDefaults", profile)
        self.assertNotIn("% Preserve expl3 syntax", profile)

    def test_build_driver_uses_canonical_preset_without_source_mutation(self):
        driver = insr_build.write_driver(self.combo)
        text = driver.read_text(encoding="utf-8")
        self.assertIn("build/preset=position-paper", text)
        self.assertIn("config/load-project=false", text)
        self.assertIn("\\INSRRenderDocument", text)
        self.assertEqual(self.before, insr_build.versioned_config_hashes())

    def test_successful_build_path_does_not_write_active_target(self):
        with mock.patch("insr_build.shutil.which", return_value="latexmk"), mock.patch("insr_build.subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess(args=["latexmk"], returncode=0, stdout="ok")
            self.assertEqual(insr_build.build(self.combo), 0)
        self.assertEqual(self.before, insr_build.versioned_config_hashes())
        self.assertTrue(insr_build.driver_path_for(self.combo).is_file())
        latexmk_calls = [call.args[0] for call in run.call_args_list if call.args and call.args[0] and call.args[0][0] == "latexmk"]
        self.assertEqual(len(latexmk_calls), 1)
        self.assertIn("driver.tex", " ".join(latexmk_calls[0]))

    def test_failed_or_interrupted_build_path_preserves_versioned_config(self):
        for exc in (subprocess.TimeoutExpired(cmd="latexmk", timeout=1), KeyboardInterrupt()):
            with self.subTest(exc=type(exc).__name__):
                shutil.rmtree(self.build_root, ignore_errors=True)
                with mock.patch("insr_build.shutil.which", return_value="latexmk"), mock.patch("insr_build.subprocess.run", side_effect=exc):
                    with self.assertRaises(type(exc)):
                        insr_build.build(self.combo)
                self.assertEqual(self.before, insr_build.versioned_config_hashes())

    def test_integrity_compile_reuses_mutation_free_build_runner(self):
        report = {"combinations": {self.combo: {}}}
        with mock.patch("insr_build.build", return_value=0) as build, mock.patch("check_latex_log.check", return_value=[]) as check:
            self.assertEqual(insr_integrity.compile_combinations(report, [self.combo]), 0)
        build.assert_called_once_with(self.combo)
        check.assert_called_once_with(insr_build.log_path_for(self.combo))

    def test_adapter_field_detection_is_adapter_specific(self):
        paper = set(insr_integrity.adapter_fields("paper", "paper"))
        slides = set(insr_integrity.adapter_fields("slides", "slides"))
        poster = set(insr_integrity.adapter_fields("poster", "poster"))
        self.assertIn("full", paper)
        self.assertNotIn("clinical", paper)
        self.assertIn("notes", slides)
        self.assertIn("handout", slides)
        self.assertIn("poster", poster)
        self.assertNotEqual(paper, slides)


if __name__ == "__main__":
    unittest.main()
