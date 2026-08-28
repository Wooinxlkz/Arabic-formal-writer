# Changelog

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
