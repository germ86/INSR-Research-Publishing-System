import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class PublicationLayerStaticTests(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_frontmatter_module_and_semantic_renderers(self):
        src = self.read("tex/latex/insr/insr-frontmatter.sty")
        for name in ["paper", "report", "book", "manual", "thesis"]:
            self.assertIn(f"__insr_frontmatter_render_{name}:", src)
        self.assertIn("DOI:~", src)
        self.assertIn("Anonymous~manuscript", src)

    def test_paper_adapters_delegate_title_rendering(self):
        for path in ["framework/adapters/paper.tex", "framework/adapters/article.tex", "framework/adapters/report.tex", "framework/adapters/manual.tex", "framework/adapters/book.tex"]:
            src = self.read(path)
            self.assertIn("__insr_frontmatter_render_", src)
            self.assertNotIn("\\maketitle", src)

    def test_metadata_and_layout_keys_exist(self):
        src = self.read("tex/latex/insr/insr-config.sty")
        for key in ["publication/doi", "publication/repository", "publication/license", "publication/review", "layout/header-left", "layout/footer-right", "metadata/short-title"]:
            self.assertIn(key, src)

    def test_header_footer_and_pdf_metadata(self):
        self.assertIn("scrlayer-scrpage", self.read("tex/latex/insr/insr-layout.sty"))
        meta = self.read("tex/latex/insr/insr-metadata.sty")
        for field in ["pdfsubject", "pdfkeywords", "pdflang", "doi", "License", "Repository", "PublicationStatus"]:
            self.assertIn(field, meta)

if __name__ == "__main__":
    unittest.main()
