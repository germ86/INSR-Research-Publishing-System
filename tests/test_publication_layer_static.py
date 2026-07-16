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
        self.assertIn("scrlayer-scrpage", self.read("tex/latex/insr/insr-page-style.sty"))
        self.assertNotIn("scrlayer-scrpage", self.read("tex/latex/insr/insr-layout.sty"))
        meta = self.read("tex/latex/insr/insr-metadata.sty")
        for field in ["pdfsubject", "pdfkeywords", "pdflang", "doi", "License", "Repository", "PublicationStatus"]:
            self.assertIn(field, meta)

    def test_project_config_split_and_semantic_colors(self):
        project = self.read("config/project-config.tex")
        for cfg in ["metadata-config.tex", "publication-config.tex", "layout-config.tex", "authors-config.tex"]:
            self.assertIn(cfg, project)
        colors = self.read("tex/latex/insr/insr-colors.sty")
        for color in ["INSRHeaderText", "INSRFooterText", "INSRTOCSection", "INSRTOCLink"]:
            self.assertIn(color, colors)

if __name__ == "__main__":
    unittest.main()
