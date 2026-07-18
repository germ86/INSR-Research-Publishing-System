import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_html_colors(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    return dict(re.findall(r"\\definecolor\{(INSR[A-Za-z]+)\}\{HTML\}\{([0-9A-Fa-f]{6})\}", text))


def relative_luminance(hex_color: str) -> float:
    channels = [int(hex_color[index : index + 2], 16) / 255 for index in (0, 2, 4)]

    def linear(channel: float) -> float:
        return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4

    red, green, blue = (linear(channel) for channel in channels)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(first: str, second: str) -> float:
    high, low = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


class ColorContrastStaticTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_active_midnight_palette_uses_dark_mode(self):
        project = self.read("config/project-config.tex")
        self.assertIn("design/palette = midnight", project)
        self.assertIn("design/mode = dark", project)

    def test_midnight_text_contrast_meets_wcag_aa(self):
        colors = parse_html_colors(ROOT / "palettes/midnight.tex")
        self.assertGreaterEqual(
            contrast_ratio(colors["INSRText"], colors["INSRBackground"]),
            4.5,
        )
        self.assertGreaterEqual(
            contrast_ratio(colors["INSRTextMuted"], colors["INSRBackground"]),
            4.5,
        )


    def test_additional_palette_pack_text_contrast_meets_wcag_aa(self):
        for palette in (
            "cortex-blue",
            "autonomic-teal",
            "somatic-sage",
            "translational-plum",
            "nordic-neuro",
            "clinical-burgundy",
            "synapse-amber",
            "nocturne-neural",
        ):
            with self.subTest(palette=palette):
                colors = parse_html_colors(ROOT / f"palettes/{palette}.tex")
                self.assertGreaterEqual(
                    contrast_ratio(colors["INSRText"], colors["INSRBackground"]),
                    4.5,
                )
                self.assertGreaterEqual(
                    contrast_ratio(colors["INSRTextMuted"], colors["INSRBackground"]),
                    4.5,
                )

    def test_dark_text_roles_do_not_use_dark_identity_color(self):
        colors = self.read("tex/latex/insr/insr-colors.sty")
        dark_block = colors.split("\\cs_new_protected:Npn \\__insr_apply_dark_semantic_roles:", 1)[1]
        dark_block = dark_block.split("\\cs_new_protected:Npn \\__insr_apply_semantic_color_roles:", 1)[0]
        for role in ("INSRHeading", "INSRHeaderText", "INSRTOCHeading", "INSRTOCSection"):
            self.assertIn(f"\\colorlet{{{role}}}{{INSRText}}", dark_block)
            self.assertNotIn(f"\\colorlet{{{role}}}{{INSRPrimary}}", dark_block)

    def test_high_contrast_override_precedes_semantic_alias_application(self):
        colors = self.read("tex/latex/insr/insr-colors.sty")
        self.assertLess(
            colors.index("palettes/high-contrast.tex"),
            colors.rindex("\\__insr_apply_semantic_color_roles:"),
        )

    def test_toc_uses_localized_title_and_explicit_roles(self):
        content = self.read("tex/latex/insr/insr-content.sty")
        self.assertIn("\\begin{frame}{\\contentsname}", content)
        self.assertIn("\\pdfbookmark[section]{\\contentsname}", content)
        self.assertIn("\\color{INSRTOCSection}", content)
        self.assertIn("\\color{INSRTOCHeading}", content)
        self.assertIn("\\INSRPageStyleTOC", content)

    def test_beamer_has_explicit_normal_text_contrast(self):
        page_style = self.read("tex/latex/insr/insr-page-style.sty")
        self.assertIn(
            "\\setbeamercolor{normal text}{fg=INSRText,bg=INSRBackground}",
            page_style,
        )
        self.assertIn("\\setkomafont{disposition}{\\color{INSRHeading}", page_style)


if __name__ == "__main__":
    unittest.main()
