# Template Developer Guide

Templates render content through semantic commands and adapters. They must not use raw `frame` in non-Beamer outputs or raw `chapter` in Beamer. Use `\INSRChapter`, `\INSRSection`, semantic statements and semantic block environments.
