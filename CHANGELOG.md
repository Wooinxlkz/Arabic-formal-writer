# Changelog

## [1.3.0]

### Fixed — real bug found via data cross-check
- **`خالص` self-contradiction bug**: it was flagged as informal Egyptian dialect, but it's also part of this project's own recommended formal closing `مع خالص التحية` (listed in `CLOSING_PATTERNS`). Any document using our own template's suggested closing would have been incorrectly flagged as containing dialect leakage. Removed from `DIALECT_TERMS`; added regression test `test_khales_closing_not_flagged_as_dialect`.

### Changed — word list cross-checked against real frequency data
Every `DIALECT_TERMS` entry checked against CAMeL Lab's open Dialectal-Arabic vs. MSA frequency corpora (6.7M / 11.4M unique words respectively — see `NOTICE.md` "Validation performed" for the full methodology and per-term ratios).

**Removed** (ratio ≤ 1.5, each with a plausible legitimate-MSA explanation):
`خالص`, `تمام`, `قاع`, `هلأ`, `أبغى`, `زين`

**Corrected/added** (cross-checked against DODa, the Moroccan-specific Darija corpus):
- `ماكاش` kept — confirmed real and strongly dialectal (ratio 11.5) but more Algerian/Tunisian than Moroccan
- `ماكاينش` added — the attested Moroccan form (ratio 6.6), absent from the original list

**Kept with a noted caveat**: `كاين` (ratio 1.5, no identified MSA homograph, but the weakest-confidence entry remaining in the list)

Net: 47 dialect terms (down from 52), each now backed by a checked frequency ratio rather than unverified judgment.

### Added
- `test_khales_closing_not_flagged_as_dialect` regression test (24 behavioral assertions total, up from 22)
- `NOTICE.md` "Validation performed (v1.3.0)" section — full methodology and per-term reasoning, not just a summary claim

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
