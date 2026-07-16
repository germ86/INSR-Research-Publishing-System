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

    def test_native_classes_and_separators(self):
        for cls, doc_type in {"insr-paper":"paper", "insr-book":"book", "insr-beamer":"slides", "insr-poster":"poster", "insr-handout":"handout"}.items():
            text = self.read(f"tex/latex/insr/{cls}.cls")
            self.assertIn("\\LoadClass{insr}", text)
            self.assertIn(f"document/type={doc_type}", text)
            self.assertNotIn("ClassWarning", text)
        page_style = self.read("tex/latex/insr/insr-page-style.sty")
        for token in ["KOMAoptions", "headsepline", "footsepline", "header-separator", "footer-separator", "logo", "git-revision"]:
            self.assertIn(token, page_style)

    def test_frontmatter_metadata_helpers_cover_reviewed_cases(self):
        meta = self.read("tex/latex/insr/insr-metadata.sty")
        frontmatter = self.read("tex/latex/insr/insr-frontmatter.sty")
        for token in ["\\insr_author_title_block:", "\\insr_affiliation_title_block:", "\\insr_suggested_citation:", "\\insr_credit_block:"]:
            self.assertIn(token, meta)
            self.assertIn(token, frontmatter)
        for token in ["ORCID", "orcid.org", "seq_remove_duplicates", "manual", "g_insr_publication_publisher_tl", "g_insr_author_contributions_tl"]:
            self.assertIn(token, meta)
        self.assertIn("Anonymous~manuscript", frontmatter)
        self.assertIn("pageanchor=false", frontmatter)
        self.assertIn("pageanchor=true", frontmatter)

    def test_requirepackage_bootstrap_has_local_package_path(self):
        cls = self.read("insr.cls")
        self.assertIn("\\def\\input@path", cls)
        self.assertIn("tex/latex/insr/", cls)
        self.assertIn("\\RequirePackage{insr-adapters}", cls)
        self.assertNotIn("\\input{tex/latex/insr/insr-adapters.sty}", cls)

    def test_citation_and_credit_formatters_are_publication_quality(self):
        meta = self.read("tex/latex/insr/insr-metadata.sty")
        for role in ["investigation", "validation", "formal-analysis", "data-curation", "supervision", "funding-acquisition", "resources"]:
            self.assertIn(role, meta)
        for token in ["__insr_publication_year:", "https://doi.org/", "{pending}{}", r"\__insr_credit_roles:n {##2}"]:
            self.assertIn(token, meta)
        self.assertNotIn("Roadmap.INSR", meta)
        self.assertNotIn("Consortium,", meta)
        self.assertNotIn("writing-original-draft} {#1}", meta)

    def test_toc_document_status_and_placeholder_lifecycle(self):
        content = self.read("tex/latex/insr/insr-content.sty")
        self.assertIn("g__insr_toc_rendered_bool", content)
        self.assertIn("pdfbookmark[section]{Contents}{insr-toc}", content)
        self.assertNotIn(r"\section*{Contents}", content)
        self.assertNotIn("addcontentsline{toc}{section}{Contents}", content)
        self.assertIn("{pp-status}", content)
        self.assertIn(r"\section*{Document status}", content)
        self.assertIn("__insr_render_placeholder:", content)
        self.assertIn("Substantive~content~pending", content)
        self.assertNotIn("syntactically complete", content)

if __name__ == "__main__":
    unittest.main()
