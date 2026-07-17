import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "tex/latex/insr/insr-metadata.sty"
CONTENT = ROOT / "content/insr-position-paper"

ROLE_LABELS = {
    "conceptualization": "Conceptualization",
    "methodology": "Methodology",
    "software": "Software",
    "writing-original-draft": "Writing -- Original Draft",
    "writing-review-editing": "Writing -- Review & Editing",
    "investigation": "Investigation",
    "validation": "Validation",
    "visualization": "Visualization",
    "formal-analysis": "Formal Analysis",
    "data-curation": "Data Curation",
    "project-administration": "Project Administration",
    "supervision": "Supervision",
    "funding-acquisition": "Funding Acquisition",
    "resources": "Resources",
}


def render_roles(raw):
    labels = []
    warnings = []
    for item in raw.split(','):
        key = item.strip().lower()
        if not key:
            continue
        label = ROLE_LABELS.get(key)
        if label is None:
            warnings.append(f"Unknown CRediT role '{key}'")
        else:
            labels.append(label)
    return ", ".join(labels), warnings


class CreditAndPlaceholderSemantics(unittest.TestCase):
    def test_credit_pipeline_renders_four_roles(self):
        rendered, warnings = render_roles(
            "conceptualization, methodology, writing-original-draft, writing-review-editing"
        )
        self.assertEqual(
            rendered,
            "Conceptualization, Methodology, Writing -- Original Draft, Writing -- Review & Editing",
        )
        self.assertEqual(warnings, [])

    def test_multiple_authors_unknown_and_empty_roles(self):
        author_a, warn_a = render_roles("software, unknown-role")
        author_b, warn_b = render_roles("")
        author_c, warn_c = render_roles("validation")
        visible = [line for line in [author_a, author_b, author_c] if line]
        self.assertEqual(visible, ["Software", "Validation"])
        self.assertEqual(warn_a, ["Unknown CRediT role 'unknown-role'"])
        self.assertEqual(warn_b + warn_c, [])

    def test_tex_credit_renderer_uses_separated_pipeline(self):
        src = METADATA.read_text(encoding="utf-8")
        for token in [
            "\\__insr_credit_role_label_set:n",
            "\\__insr_credit_role_collect:n",
            "\\seq_put_right:Nx \\l__insr_credit_role_label_seq",
            "\\seq_use:Nn \\l__insr_credit_role_label_seq {,~}",
            "\\insr_credit_has_valid:",
        ]:
            self.assertIn(token, src)
        renderer = re.search(r"\\cs_new_protected:Npn \\__insr_roles_label:n.*?\\prg_new_conditional:Npnn", src, re.S).group(0)
        self.assertNotIn("clist_map_indexed_inline", renderer)
        self.assertNotIn("##2", renderer)

    def test_official_position_paper_uses_explicit_placeholders(self):
        for path in CONTENT.glob("*.tex"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("\\INSRPlaceholder", text, path)
            self.assertNotIn("This placeholder exists only", text, path)
            self.assertNotIn("minimal syntactic placeholder", text, path)
            self.assertNotRegex(text, r"\\INSRFullText\{[^}]*placeholder", path.as_posix())


if __name__ == "__main__":
    unittest.main()
