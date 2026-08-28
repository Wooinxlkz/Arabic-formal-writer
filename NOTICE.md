# Notice

## Not legal, professional, or certified-translation advice

This plugin helps draft and review formal Arabic documents. It is **not**:
- A certified translation service or a substitute for a professional translator on documents that require certification (visa applications, legal filings, notarized documents, etc.)
- A legal service. Any contract, agreement, or document with real legal or financial consequences produced with this tool **must** be reviewed by a licensed lawyer in the relevant jurisdiction before it is signed or relied upon. The contract template in `skills/arabic-formal-writing/references/document-templates.md` (§8) includes this disclaimer by design — do not remove it when using that template.
- An official-register grammar authority. The `register_check.py` script is a heuristic linter built from documented, common failure patterns — it is not a certified Arabic grammar/spellcheck engine and does not claim completeness.

## Regional convention data

The regional conventions documented in `references/regional-conventions.md` (numerals, date formats, honorifics, closing formulas) are a good-faith, generalized summary intended as a sensible default — they are simplifications of real, varied practice that differs by specific institution, era, and individual/organizational style. They were compiled from general knowledge of formal Arabic writing conventions and are not sourced from a single authoritative standards document, because no single unified standard exists across the regions covered. Treat them as a starting point, not a specification, especially for high-stakes documents (government/legal submissions) — verify against the specific receiving institution's own conventions where possible.

## Dialect and hamza word lists

The informal/dialect term list and the hamza-error list in `register_check.py` are curated manually for this project, covering common, well-documented patterns in Egyptian, Gulf, Levantine, and Maghrebi/Darija informal Arabic, plus general chat-register terms. They are:
- **Not exhaustive.** Absence of a flag does not mean a document is dialect-free or error-free.
- **Not a dialect classifier or NLP model.** This is literal string matching against a fixed list — it has no understanding of Arabic morphology beyond the simple word-boundary heuristics implemented in the script.
- Intended to catch common, high-confidence patterns as a first pass, not to replace a native speaker's review for anything that matters.

## No data collection, no network calls

This plugin performs no network requests, collects no user data, and sends nothing anywhere. `register_check.py` runs entirely locally against the text you give it. The skill and agent instructions direct Claude's behavior when the plugin is active; they do not by themselves transmit any information beyond Claude's normal operation.

## Attribution

Built by Karim ([@Wooinxlkz](https://github.com/Wooinxlkz)) as an independent, original project. No third-party code, models, or datasets are bundled — `register_check.py` uses only the Python 3 standard library.

## Feedback and corrections

If you're a native speaker of any covered region and notice something inaccurate in the regional conventions, dialect lists, or templates, corrections are genuinely welcome — this is exactly the kind of detail that's easy to get subtly wrong from outside a specific regional context, and the project is better for being checked against real native usage.
