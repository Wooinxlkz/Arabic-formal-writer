# Contributing

This project is most improvable by native speakers of the regions it covers — the dialect/hamza word lists and regional-convention notes were compiled in good faith but are explicitly not authoritative (see `NOTICE.md`).

## Most useful contributions, in order of value

1. **Correcting or expanding the dialect term list** in `skills/arabic-formal-writing/scripts/register_check.py` (`DIALECT_TERMS`). If a term is mislabeled by region, wrong, or missing a common high-frequency term you'd actually expect to see leak into formal writing, that's a high-value fix.
2. **Regional convention corrections** in `skills/arabic-formal-writing/references/regional-conventions.md` — numerals, dates, honorifics, and closing formulas vary by institution and era; if something's wrong for your country/context specifically, say so with the correction.
3. **New document-type templates** — academic recommendation letters, official complaints, notarization requests, etc. Follow the existing structure in `document-templates.md`: a template skeleton plus a short "Rules" list of the 2-4 things people most commonly get wrong.
4. **Test fixtures** — a real (anonymized) example of a document that should pass cleanly, or one with a specific flaw the checker currently misses, is more useful than a description of the flaw.

## Making a change to `register_check.py`

1. Make your change.
2. Run `python3 tests/run_tests.py` — all existing assertions must still pass.
3. If you added a new check or word-list entries, add a corresponding assertion to `tests/run_tests.py` (or a new fixture in `tests/fixtures/`) that would fail without your change. A word-list addition with no test proving it fires is not verifiable.
4. `python3 -m py_compile skills/arabic-formal-writing/scripts/register_check.py` to confirm it still compiles cleanly.

CI (`.github/workflows/tests.yml`) runs all of this automatically on PRs.

## Scope boundaries

Please don't expand this into:
- A general Arabic grammar/spellcheck tool (out of scope — this is specifically about formal-register signals, not general correctness)
- A dialect-to-MSA translator (the word list flags leakage; it isn't meant to become a full translation engine)
- Legal document generation beyond simple agreements (see the disclaimer requirement in `document-templates.md` §8 and `NOTICE.md`)

## Code style

`register_check.py` is deliberately dependency-free (Python 3 standard library only). Keep it that way — no new pip dependencies without a strong reason, since part of the point is that this runs anywhere with zero setup.
