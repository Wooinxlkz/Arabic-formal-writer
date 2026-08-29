# Changelog

## [1.2.0]

### Added
- `tests/validate_wordlists.py` — 9 static consistency checks on `DIALECT_TERMS` and `HAMZA_ERRORS` themselves (not behavior): no wrong==correct no-ops, no empty keys, no invalid region labels, no duplicate keys (scanned from source since Python dict literals silently drop true dupes), every term compiles as a valid regex, no unexpected hamza-entry prefix collisions, closing-patterns/whitelist sanity. Wired into CI.
- `NOTICE.md` now documents recommended real validation sources for expanding the word lists (MADAR Lexicon, NADI, QADI, IADD — peer-reviewed Arabic dialect corpora) instead of leaving "these lists aren't authoritative" as an unresolved concern with no path forward. `CONTRIBUTING.md` updated to point contributors at the same sources.

### Notes
- Ran a real gap-check against these academic dialect resources this cycle. They're gated/license-required datasets, so no data was bulk-imported — this release documents the correct sourcing path rather than fabricating an import that didn't happen.

## [1.1.0]

### Added
- `.claude-plugin/marketplace.json` — enables direct `/plugin install` distribution
- GitHub Actions CI (`.github/workflows/tests.yml`) — runs the full test suite plus CLI/exit-code/stdin smoke tests on every push and PR, across Python 3.9/3.11/3.12
- Expanded dialect term list: ~48 terms across Egyptian, Gulf, Levantine, Maghrebi/Darija, and informal-chat registers (up from ~30)
- Expanded hamza-error list: 17 curated high-confidence patterns (up from 9)
- Region-specific CV variant guidance (Gulf personal-info-field norms, Maghreb francophone-influenced conventions) in `document-templates.md`
- `CONTRIBUTING.md`, `.gitignore`

### Fixed
- Removed an incorrectly-flagged hamza pattern (`اعتبار`) that was actually correct Arabic and would have produced a false positive — caught during review before release, not after.

## [1.0.0]

Initial release:
- `arabic-formal-writing` skill covering 8 document types
- `arabic-document-reviewer` agent
- `register_check.py` deterministic checker (numerals, dialect leakage, hamza errors, letter-structure checks, sentence rhythm, Latin-script leakage)
- 5 reference docs (templates, regional conventions, tone tiers, calques, review checklist)
- 22-assertion test suite, 2 slash commands, README, LICENSE (MIT), NOTICE.md
