import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_latex_log.py"


class LatexLogCheckerTests(unittest.TestCase):
    def run_checker(self, text: str):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "main.log"
            log.write_text(text, encoding="utf-8")
            return subprocess.run(
                ["python3", str(SCRIPT), str(log)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

    def test_clean_log_passes(self):
        result = self.run_checker("Output written on main.pdf.\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_repository_path_package_warning_fails(self):
        result = self.run_checker(
            "LaTeX Warning: You have requested package `tex/latex/insr/insr-core',\n"
            "but the package provides `insr-core'.\n"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("repository path", result.stdout)

    def test_known_regression_warnings_fail(self):
        warnings = [
            "LaTeX Warning: Command \\showhyphens has changed.\n",
            "Package hyperref Warning: Option `pdfauthor' has already been used, setting the option has no effect.\n",
            "Package biblatex Warning: No localisation for language 'ngerman' loaded.\n",
        ]
        for warning in warnings:
            with self.subTest(warning=warning):
                result = self.run_checker(warning)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
