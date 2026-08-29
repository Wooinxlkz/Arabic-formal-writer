# Changelog

## [1.6.0]

### Added — robustness hardening, found via deliberate stress-testing
For the first time, the checker was stress-tested against inputs it had never been tried against: empty strings, pure English, pure numbers, emoji, null/control characters, RTL/LTR mark characters, mixed scripts, and a 5000-character single word with no spaces. No crashes on any of them — but one real usability bug was found and fixed:

- **`latin_script_leakage` flag-spam bug**: a document with heavy or entirely non-Arabic content (e.g. someone accidentally runs the checker against an English document) previously produced one flag per *occurrence* of every Latin word — a genuinely non-Arabic document could produce dozens of near-identical flags with no summary signal. Fixed: flags are now deduplicated by word and capped at 8 individual flags, with a summary flag for anything beyond the cap.
- **New check: `check_arabic_content_ratio`** — computes the ratio of Arabic to Latin alphabetic characters and raises a single clear `low_arabic_content` warning when a document is overwhelmingly non-Arabic (<30% Arabic characters, with enough total text to judge), rather than letting the rest of the report imply a meaningful Arabic-register review happened when it didn't.
- 3 new regression tests covering the dedup/cap behavior and the new ratio check, including a check that it correctly does *not* fire on normal Arabic text or on trivially short input.

### Fixed — a recurring editing mistake in the test file, caught and named honestly
While adding new tests to `tests/run_tests.py` in this session and the prior one, a `str_replace` edit accidentally deleted the `def main():` line three separate times (this changelog entry exists partly to note that pattern honestly rather than bury it — each time it broke the test file immediately and was caught by actually running the tests, not assumed fixed).

### Notes
- 32 behavioral assertions (up from 26), 11 static (unchanged). 43 total.
- This release intentionally did not add more word-list entries — after the country-level and Gulf/Levant dataset investigation in v1.4.0/v1.5.0, the highest-value remaining work was found to be robustness, not more dialect terms.

## [1.5.0]

### Added — real, sourced country-specific document conventions (not just word-list data)
- New reference file `skills/arabic-formal-writing/references/saudi-official-correspondence.md`, sourced from a single citable authority: "دليل المراسلات الكتابية" (Official Correspondence Manual, 1440H), Saudi Ministry of Finance — the first genuinely sourced (vs. general-knowledge) document-convention reference in this project.
- Real findings from that source: a precise rank-based honorific/closing-formula table (King/Crown Prince/Princes/Ministers/multiple recipients/Directors-general — 5 distinct tiers, not the previous flat "Gulf" treatment); the exact Hijri-then-Gregorian date format with "الموافق"; and a documented correction to `regional-conventions.md`'s prior assumption about Gulf numerals — this ministry's own manual specifies **Western** digits, not Arabic-Indic, contradicting the general note. `regional-conventions.md` now flags this as institution-dependent rather than asserting one convention.
- One new `HAMZA_ERRORS` entry (`شيئ ` → `شيء `, space-bounded) sourced from the same manual's own error-correction table — caught and avoided a real false-positive risk before adding it: a naive (non-space-bounded) version would have incorrectly flagged the unrelated, completely legitimate word `مشيئة` (as in `بمشيئة الله`). Regression test `test_sheya_hamza_not_flagged_inside_mashiya` added.

### Investigated and explicitly declined
- Attempted to find open, per-country dialect datasets for Gulf/Levantine countries (comparable to Morocco's DODa) to push more `DIALECT_TERMS` entries to country-level. None found — only general Wikipedia dialect descriptions and small, unverified user-contributed dictionary apps, no structured downloadable data. Documented here rather than fabricating country-level precision without a real source. Most Gulf/Levantine entries remain family-level only (`countries=()`), honestly.

### Notes
- 26 behavioral assertions (up from 24), 11 static (unchanged). 37 total.

## [1.4.0]

### Changed — region taxonomy restructured from 4 broad buckets to family + country
- `DIALECT_TERMS` entries changed from `(equivalent, family)` to `(equivalent, family, countries)` — a tuple of ISO-3166 codes where the term is specifically verified for that country, empty when only confirmed at the family level (honest, not guessed).
- Added `REGION_TAXONOMY` (family → its countries) and `COUNTRY_NAMES` as the reference taxonomy — this is now a real library structure, not just four flat labels.
- Added a new **Sudanese** family (previously absent entirely).
- `check_dialect_leakage` output now reports country-level attribution when available (e.g. "maghrebi: Algeria/Tunisia" instead of just "maghrebi").
- `--region` CLI choices gained `sudan`.

### Added — 16 new dialect terms, all corpus-checked before inclusion
Egyptian: `ليه`, `علطول`. Sudanese (new family): `زول`, `زولة`. Gulf: `مافي`, `وش`, `شسمه`, `طاري`, `توه`, `خوش`. Levantine: `زعلان`, `كمان`. Maghrebi: `مزيان` (ma), `ياك`, `غادي`, `فاش`. Every addition checked against CAMeL Lab DA/MSA frequency ratios using the same methodology as the v1.3.0 cleanup — see `NOTICE.md` "Region/country taxonomy and list expansion (v1.4.0)" for the full list of candidates that were *rejected* by this check (e.g. `قوي`, `بقى`, `غير` — each a legitimate-MSA homograph, same failure pattern as the v1.3.0 removals).

Total: 63 dialect terms (up from 47), 18 hamza patterns.

### Added — 2 new static validator checks
`tests/validate_wordlists.py` now also verifies every country tag actually belongs to its declared family, and every country code used is a recognized one (11 static checks total, up from 9).

### Notes
- An initial attempt to expand the list by algorithmically mining the highest-frequency DA/MSA-ratio words with no manual filtering was tried and largely failed — the top results were dominated by proper nouns, religious phrases, and social-media jargon rather than usable dialect vocabulary. Documented honestly in `NOTICE.md` rather than hidden; the working method was a curated candidate list checked against the same ratio data, not a fully automated pipeline.
- Regional *conventions* (`regional-conventions.md`: numerals, dates, honorifics) remain at the broader family level — country-level precision there would require a data source this project doesn't currently have verified access to, unlike the dialect word list.

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
