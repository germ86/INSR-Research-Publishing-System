
## Implemented target system

INSR now separates `content/source` from `output/target`. A single source tree can render as paper-like output, slides, handouts, posters, manuals, reports, briefs, books, or theses according to the authoritative registry used by both `insr-config.sty` and the Python validators.

Content units retain `\INSRFullText`, `\INSRSummary`, `\INSRKeyMessage`, and `\INSRSpeakerNotes`, and add author-controlled representations: `\INSRHandoutText`, `\INSRPosterText`, `\INSRExecutiveSummary`, `\INSRClinicalApplication`, `\INSRSafetyNote`, `\INSRMethodsSummary`, and `\INSRLimitationsSummary`. The LaTeX build never invents or automatically summarizes scientific content.


## Golden reference outputs

The reference publication project provides paper, slides, handout and poster entry points generated from neutral, author-controlled content. Use these entry points for release smoke tests and visual review.
