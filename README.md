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
│   └── run_tests.py                     # 22 assertions, all passing
├── LICENSE
├── NOTICE.md
├── CONTRIBUTING.md
└── CHANGELOG.md
```

## Document types covered

Official/business letters · administrative correspondence · CVs/resumes · cover letters · reports · internal memos · meeting minutes · simple contracts & agreements (with a mandatory legal-review disclaimer — see `NOTICE.md`).

## Regional conventions covered

Neutral/Pan-Arab (default) · Gulf · Egyptian · Levantine · Maghrebi/Algerian — numerals, date formats, honorifics, and closing formulas for each. Core grammar is always standard MSA; only these surface conventions change by region.

## The checker: `register_check.py`

A dependency-free Python 3 script (standard library only) that checks a draft for:

- **Mixed numeral systems** — Western (0-9) vs Arabic-Indic (٠-٩) used inconsistently in one document
- **Dialect/informal word leakage** — a curated, labeled list covering Egyptian, Gulf, Levantine, and Maghrebi/Darija terms, each with its MSA equivalent
- **Common hamza errors** — a curated high-confidence list (kept short deliberately to limit false positives)
- **Missing subject line / closing formula** for letter-type documents
- **Sentence-rhythm outliers** — both "too choppy" (translated-feeling) and true run-ons
- **Untransliterated Latin-script leakage** without technical justification

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
python3 tests/run_tests.py            # 24 behavioral assertions against sample documents
python3 tests/validate_wordlists.py   # 9 static consistency checks on the word-list data itself
```

`run_tests.py` checks behavior (does the checker correctly flag/not-flag real sample text). `validate_wordlists.py` checks the data (no typos, no self-contradictions, no regex-breaking entries, no accidental no-op mappings). Both run in CI on every push/PR.

## Validation status

As of v1.3.0, the full `DIALECT_TERMS` list (47 terms) has been cross-checked against CAMeL Lab's open Arabic frequency corpora (real Dialectal-Arabic vs. MSA word frequencies, not another AI-generated list) — see `NOTICE.md` for the full methodology. That check found and fixed one real bug (a term that contradicted this project's own recommended letter closing) and removed six terms that turned out to be legitimate MSA words rather than dialect. This is real progress on accuracy, not just process — but it is not the same as native-speaker review, which still hasn't happened. See `NOTICE.md` for exactly what is and isn't verified.

## Limitations — read this before relying on it

- **Not a certified translation or legal tool.** Contracts drafted with this skill always include a disclaimer to have a licensed lawyer review anything with legal weight — see `NOTICE.md`.
- **The dialect/hamza word lists are curated, not exhaustive.** They cover well-documented, high-frequency patterns — they will not catch everything, and they are not a substitute for a native reviewer's judgment on a document that actually matters (an official government submission, a legal filing).
- **Regional convention data is a simplification.** Real usage varies by institution, era, and individual style within every region listed. Treat `regional-conventions.md` as a well-reasoned default, not a formal specification.
- **No network calls, no external data sources.** Everything here is static reference material and a local script — there's no live dialect-detection model or API behind this.

## License

MIT — see `LICENSE`.

## Contributing

See `CONTRIBUTING.md`. Short version: this is most improvable by native speakers of the regions it covers, correcting or expanding the word lists and regional-convention notes, which were compiled in good faith but aren't authoritative (`NOTICE.md`).

## Changelog

See `CHANGELOG.md`. Currently v1.1.0.
