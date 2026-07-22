import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "overleaf_doctor.py"

class OverleafDoctorTests(unittest.TestCase):
    def run_cmd(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_list_entrypoints(self):
        result = self.run_cmd("list-entrypoints")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("main.tex", result.stdout)
        self.assertIn("examples/minimal-paper/main.tex", result.stdout)

    def test_root_entrypoint(self):
        result = self.run_cmd("check-entrypoint", "main.tex")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("documentclass: insr", result.stdout)

    def test_plain_entrypoints_are_paths_only(self):
        result = subprocess.run(
            [sys.executable, "tools/overleaf_doctor.py", "list-entrypoints", "--plain"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        self.assertIn("main.tex", lines)
        self.assertNotIn("[root]", result.stdout)
        self.assertEqual(lines, list(dict.fromkeys(lines)))
        self.assertTrue(all(line and not line.startswith("[") for line in lines))

    def test_grouped_entrypoints_have_headings(self):
        result = self.run_cmd("list-entrypoints")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[root]", result.stdout)
        self.assertIn("[paper]", result.stdout)


if __name__ == "__main__":
    unittest.main()
