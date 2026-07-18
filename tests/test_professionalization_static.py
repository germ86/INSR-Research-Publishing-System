from pathlib import Path
import json, subprocess, tempfile, unittest

ROOT = Path(__file__).resolve().parents[1]

class ProfessionalizationStaticTests(unittest.TestCase):
    def read(self, rel):
        return (ROOT / rel).read_text(encoding='utf-8')

    def test_public_plugin_theme_api_registered(self):
        core = self.read('tex/latex/insr/insr-core.sty')
        self.assertIn('\\insr_plugin_register:nn', core)
        self.assertIn('\\INSRUsePlugin', core)
        self.assertIn('\\insr_theme_register:nn', core)
        self.assertIn('\\INSRUseTheme', core)

    def test_json_schema_is_strict(self):
        schema = json.loads(self.read('schema/insr-project.schema.json'))
        self.assertFalse(schema['additionalProperties'])
        self.assertEqual(schema['properties']['schema_version']['const'], '1.0')

    def test_cli_generates_deterministic_safe_tex(self):
        cfg = {
            'schema_version':'1.0',
            'project': {'title': 'A&B_Study', 'language': 'english'},
            'build': {'preset': 'position-paper'},
            'design': {'theme': 'medical'},
            'typography': {'fontset': 'inter'},
            'metadata': {'authors': [{'name':'Example #1','orcid':'0000-0002-1825-0097'}]},
        }
        with tempfile.TemporaryDirectory() as td:
            inp=Path(td)/'project.json'; out1=Path(td)/'a.tex'; out2=Path(td)/'b.tex'
            inp.write_text(json.dumps(cfg, sort_keys=True), encoding='utf-8')
            for out in (out1,out2):
                subprocess.run(['python3', str(ROOT/'tools/insr_cli.py'), 'configure', str(inp), '-o', str(out)], check=True, cwd=ROOT)
            self.assertEqual(out1.read_text(), out2.read_text())
            self.assertIn(r'A\&B\_Study', out1.read_text())

    def test_cli_rejects_bad_orcid(self):
        cfg={'schema_version':'1.0','metadata':{'authors':[{'name':'Bad','orcid':'bad'}]}}
        with tempfile.TemporaryDirectory() as td:
            inp=Path(td)/'project.json'; inp.write_text(json.dumps(cfg), encoding='utf-8')
            run=subprocess.run(['python3', str(ROOT/'tools/insr_cli.py'), 'configure', str(inp)], cwd=ROOT, text=True, capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn('orcid', run.stderr)
