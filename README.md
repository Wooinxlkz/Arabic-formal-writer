# Arabic Formal Writer

A Claude plugin (skill + reviewer agent + deterministic checker) for writing and reviewing formal Modern Standard Arabic (MSA) documents — official letters, administrative correspondence, CVs, cover letters, reports, memos, meeting minutes, and simple contracts.

## Why

Most Arabic AI-writing help today has three recurring problems:

1. **It defaults to one region's conventions** (usually Gulf or Egyptian) even when you're writing from or to the Maghreb, the Levant, or want neutral Pan-Arab MSA.
2. **It reads as translated** — English/French sentence structure wearing Arabic words.
3. **It mixes registers** — a dialect word or an inconsistent numeral system slipping into an otherwise formal document.

This plugin exists to catch and prevent exactly those three failure modes — with real reference material and a deterministic script, not just a "write formally" instruction.

## What's included

```
arabic-formal-writer/
├── .claude-plugin/
│   ├── plugin.json                      # plugin manifest
│   └── marketplace.json                 # enables direct /plugin install
├── .github/workflows/
│   └── tests.yml                        # CI: runs full test suite on push/PR
├── skills/
│   └── arabic-formal-writing/
│       ├── SKILL.md                     # main skill definition
│       ├── references/
│       │   ├── document-templates.md    # structure for every supported doc type
│       │   ├── regional-conventions.md  # Gulf/Egypt/Levant/Maghreb: numerals, dates, honorifics
│       │   ├── tone-tiers.md            # 3 MSA formality tiers
│       │   ├── common-calques.md        # English/French → bad-Arabic calques, with fixes
│       │   └── review-checklist.md      # manual checklist used by the reviewer agent
│       └── scripts/
│           └── register_check.py        # deterministic linter (see below)
├── agents/
│   └── arabic-document-reviewer.md      # subagent for deep document review
├── commands/
│   ├── arabic-letter.md                 # /arabic-letter <request>
│   └── arabic-review.md                 # /arabic-review <text>
├── tests/
│   ├── fixtures/
│   │   ├── good_letter.txt
│   │   └── flawed_letter.txt
│   └── run_tests.py                     # behavioral test suite — see Testing section for current count
├── LICENSE
├── NOTICE.md
├── CONTRIBUTING.md
└── CHANGELOG.md
```

## Document types covered

Official/business letters · administrative correspondence · CVs/resumes · cover letters · reports · internal memos · meeting minutes · simple contracts & agreements (with a mandatory legal-review disclaimer — see `NOTICE.md`).

## Regional conventions covered

Neutral/Pan-Arab (default) · Gulf · Egyptian · Sudanese · Levantine · Maghrebi/Algerian — numerals, date formats, honorifics, and closing formulas for each. Core grammar is always standard MSA; only these surface conventions change by region.

The dialect-leakage checker goes further than the document conventions: it tags terms at the country level where verified (e.g. Algeria/Tunisia vs. Morocco within Maghrebi — see `NOTICE.md`), via an explicit `REGION_TAXONOMY` rather than four flat regional buckets. One country — Saudi Arabia — also has a dedicated, source-cited convention file (`references/saudi-official-correspondence.md`) drawn from an actual government correspondence manual, rather than general knowledge.

## The checker: `register_check.py`

A dependency-free Python 3 script (standard library only) that checks a draft for:

- **Mixed numeral systems** — Western (0-9) vs Arabic-Indic (٠-٩) used inconsistently in one document
- **Dialect/informal word leakage** — a curated, labeled list covering Egyptian, Sudanese, Gulf, Levantine, and Maghrebi/Darija terms (63 terms, some tagged to specific countries), each with its MSA equivalent
- **Common hamza errors** — a curated high-confidence list (kept short deliberately to limit false positives)
- **Missing subject line / closing formula** for letter-type documents
- **Sentence-rhythm outliers** — both "too choppy" (translated-feeling) and true run-ons
- **Untransliterated Latin-script leakage** without technical justification, deduplicated and capped so heavily non-Arabic text produces a clear signal instead of dozens of repetitive flags
- **Overall Arabic-content ratio** — warns clearly when a document is overwhelmingly non-Arabic, so the rest of the report isn't misread as a meaningful review of text the tool wasn't designed for

It's a heuristic linter, not a grammar engine — false positives are expected and fine (they're meant to be reviewed, by you or the `arabic-document-reviewer` agent), but the specific patterns it targets are tested and verified working.

### Usage

```bash
python3 skills/arabic-formal-writing/scripts/register_check.py path/to/draft.txt --doc-type letter --region maghreb
echo "النص هنا" | python3 skills/arabic-formal-writing/scripts/register_check.py - --json
```

Exit code is `0` by default (advisory); pass `--strict` to exit `1` when any flag fires (useful in CI).

## Installing

### Claude Code

Local, from this folder:
```
claude plugin add ./arabic-formal-writer
```

Once pushed to GitHub, this repo is a self-contained marketplace (see `.claude-plugin/marketplace.json`) — anyone can install directly:
```
claude plugin marketplace add Wooinxlkz/arabic-formal-writer
claude plugin install arabic-formal-writer@arabic-formal-writer-marketplace
```

### Manual / Claude.ai

The `skills/arabic-formal-writing/` directory is a standalone Agent Skill and can be added directly wherever custom skills are supported, even without the rest of the plugin (agents/commands are Claude Code-specific).

## Testing

```bash
python3 tests/run_tests.py            # 32 behavioral assertions against sample documents
python3 tests/validate_wordlists.py   # 11 static consistency checks on the word-list data itself
```

`run_tests.py` checks behavior (does the checker correctly flag/not-flag real sample text). `validate_wordlists.py` checks the data (no typos, no self-contradictions, no regex-breaking entries, no accidental no-op mappings, no country tag misattributed to the wrong family). Both run in CI on every push/PR.

## Validation status

As of v1.6.0, `DIALECT_TERMS` covers 63 terms across 6 families (Egyptian, Sudanese, Gulf, Levantine, Maghrebi, informal-chat), all cross-checked against CAMeL Lab's open Arabic frequency corpora (real Dialectal-Arabic vs. MSA word frequencies) — see `NOTICE.md` for the full methodology, including terms that were tested and *rejected* for looking plausible but showing weak/negative dialectal signal (a real, recurring failure mode: several common-sounding words turn out to be legitimate MSA homographs). That check has found and fixed one real bug (a term that contradicted this project's own recommended letter closing), plus one real government-sourced convention file for Saudi correspondence and a robustness-hardening pass (deduplicated flag spam, low-Arabic-content detection). This is real progress on accuracy and reliability, not just process — but it is not the same as native-speaker review, which still hasn't happened. See `NOTICE.md` for exactly what is and isn't verified.

## Limitations — read this before relying on it

- **Not a certified translation or legal tool.** Contracts drafted with this skill always include a disclaimer to have a licensed lawyer review anything with legal weight — see `NOTICE.md`.
- **The dialect/hamza word lists are curated, not exhaustive.** They cover well-documented, high-frequency patterns — they will not catch everything, and they are not a substitute for a native reviewer's judgment on a document that actually matters (an official government submission, a legal filing).
- **Regional convention data is a simplification.** Real usage varies by institution, era, and individual style within every region listed. Treat `regional-conventions.md` as a well-reasoned default, not a formal specification.
- **The shipped script makes no network calls at runtime** — `register_check.py` runs entirely locally against whatever text you give it, no API keys, no telemetry. This is separate from how its data was *validated during development*, which did use external sources (CAMeL Lab corpora, a Moroccan Darija dataset, a Saudi government PDF) — see `NOTICE.md` "Recommended sources" and "Validation performed" for exactly what was consulted and when. None of that is called at runtime; it informed the static word lists shipped in the file.
- **No native-speaker review has happened.** Every claim in this project has been checked against corpus statistics, cited government documents, or general knowledge — never against a native speaker reading real generated output and confirming it sounds right. This is the single biggest open gap; see `NOTICE.md` "Feedback and corrections."

## Security

- No `eval`, `exec`, shell commands, or dynamic code execution anywhere in `register_check.py` — it's regex and dict lookups against the text you pass it.
- No network calls, no file writes outside what you explicitly redirect via shell (`>`), no telemetry.
- Stress-tested (v1.6.0) against empty input, pure non-Arabic text, null/control characters, RTL/LTR mark characters, emoji, and a 5000-character single word with no spaces — no crashes found. This is not a formal security audit; it's targeted robustness testing against inputs a normal user might accidentally pass in.
- Not tested against adversarially crafted pathological input designed to trigger regex catastrophic backtracking (ReDoS) on very large inputs — the regex patterns used are simple (literal escapes, basic character classes) and not the nested-quantifier shapes typically associated with ReDoS, but this hasn't been specifically fuzzed.
- The script reads whatever file path you give it via the CLI (or stdin) — it does no path validation or sandboxing, same as any standard command-line tool. Don't run it against untrusted file paths in an automated pipeline without your own path validation.

## License

MIT — see `LICENSE`.

## Contributing

See `CONTRIBUTING.md`. Short version: this is most improvable by native speakers of the regions it covers, correcting or expanding the word lists and regional-convention notes, which were compiled in good faith but aren't authoritative (`NOTICE.md`).

## Changelog

See `CHANGELOG.md`. Currently v1.6.0.
