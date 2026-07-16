
## Implemented target system

INSR now separates `document/type`, `output/target`, and `content/source`. Use `\INSRBootstrap{document/type=rct-protocol, output/target=slides}` to choose the semantic document type independently from the rendering format. `content/source = auto` resolves the default source from the document type, while output targets select the base class and adapter.

Content units retain `\INSRFullText`, `\INSRSummary`, `\INSRKeyMessage`, and `\INSRSpeakerNotes`, and add author-controlled representations: `\INSRHandoutText`, `\INSRPosterText`, `\INSRExecutiveSummary`, `\INSRClinicalApplication`, `\INSRSafetyNote`, `\INSRMethodsSummary`, and `\INSRLimitationsSummary`. The LaTeX build never invents or automatically summarizes scientific content.


## Golden reference outputs

The reference publication project provides paper, slides, handout and poster entry points generated from neutral, author-controlled content. Use these entry points for release smoke tests and visual review.

## Shared TOC and placeholder lifecycle

All targets use the same public `\INSRTableOfContents` entry point. Paper, report, manual, book, and thesis outputs receive one localized contents heading from the base class; slides receive one Agenda frame. Content-unit placeholders are resolved centrally and work across paper, slides, handout, poster, manual, and executive brief renderers without automatic AI summarization.
