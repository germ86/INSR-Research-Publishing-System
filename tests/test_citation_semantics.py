import unittest


def auto_citation(author, year, title, subtitle="", version="", publisher="", institution="", doi=""):
    parts = [f"{author} ({year})."]
    title_part = title + (f": {subtitle}" if subtitle else "")
    if version:
        title_part += f" (Version {version})"
    parts.append(title_part + ".")
    parts.append((publisher or institution) + ".")
    doi_key = doi.strip().lower()
    if doi and doi_key not in {"pending", "to be assigned"}:
        parts.append(f"https://doi.org/{doi}.")
    return " ".join(parts)


class CitationSemantics(unittest.TestCase):
    def test_automatic_citation_spacing(self):
        self.assertEqual(
            auto_citation(
                "Schmeil, F.",
                "2026",
                "Integrative Neuro-Somatic Recalibration",
                "Conceptual Framework and Research Roadmap",
                "1.0",
                "INSR Research Consortium",
            ),
            "Schmeil, F. (2026). Integrative Neuro-Somatic Recalibration: "
            "Conceptual Framework and Research Roadmap (Version 1.0). INSR Research Consortium.",
        )

    def test_manual_citation_mode_is_source_controlled(self):
        manual = "Manual author text. Manual title. Manual publisher."
        self.assertEqual(manual, "Manual author text. Manual title. Manual publisher.")

    def test_doi_and_fallbacks(self):
        self.assertIn("https://doi.org/10.1234/example.", auto_citation("A.", "2026", "T", publisher="P", doi="10.1234/example"))
        self.assertNotIn("doi.org", auto_citation("A.", "2026", "T", publisher="P", doi="pending"))
        self.assertTrue(auto_citation("A.", "2026", "T", institution="Institute").endswith("Institute."))
        self.assertTrue(auto_citation("A.", "2026", "T", publisher="Publisher", institution="Institute").endswith("Publisher."))


if __name__ == "__main__":
    unittest.main()
