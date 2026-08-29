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

## Recommended sources for validating or expanding the word lists

This project's dialect/hamza lists were compiled from general knowledge, not cross-checked against a peer-reviewed linguistic resource. That is the single biggest accuracy gap in this project, and it's worth being specific about the right way to close it rather than leaving it vague.

The Arabic-NLP research community maintains real, annotated dialect resources that are a categorically stronger validation source than another AI-generated wordlist:

- **MADAR Corpus & Lexicon** (Bouamor et al., 2018, NYU Abu Dhabi CAMeL Lab) — a parallel corpus/lexicon covering 25 Arabic city dialects plus MSA, with ~47,000 lexical entries each mapped to MSA/English/French. The most directly useful resource for this project's purpose, since it's structured as dialect-term → MSA-equivalent, which is exactly the shape `DIALECT_TERMS` uses. `https://camel.abudhabi.nyu.edu/madar/` — requires a data license agreement to download; check current terms before redistributing any derived list.
- **NADI (Nuanced Arabic Dialect Identification)** shared tasks, UBC-NLP — annual country- and province-level dialect corpora across all 21 Arab countries, useful for confirming which terms are actually associated with which country rather than a broader regional guess. `https://github.com/UBC-NLP/nadi`
- **QADI** (QCRI, "Arabic Dialect Identification in the Wild") — dialect ID at the country level from real social-media text. `https://github.com/qcri/QADI`
- **IADD** — an integrated dataset combining multiple prior dialect-ID corpora into one labeled set. `https://github.com/JihadZa/IADD`

**How this should be used, concretely:** if you're expanding `DIALECT_TERMS` or `HAMZA_ERRORS`, the right process is (1) check whether the dataset's license permits the use you have in mind, (2) look up the term/pattern against the corpus rather than relying on memory or another AI's output, (3) add it with a test assertion per `CONTRIBUTING.md`. A word-list entry justified by "a research corpus confirmed this pattern in real annotated text" is a materially stronger claim than "this seemed right" — say which one it is when you contribute.

## No data collection, no network calls

This plugin performs no network requests, collects no user data, and sends nothing anywhere. `register_check.py` runs entirely locally against the text you give it. The skill and agent instructions direct Claude's behavior when the plugin is active; they do not by themselves transmit any information beyond Claude's normal operation.

## Attribution

Built by Karim ([@Wooinxlkz](https://github.com/Wooinxlkz)) as an independent, original project. No third-party code, models, or datasets are bundled — `register_check.py` uses only the Python 3 standard library.

## Feedback and corrections

If you're a native speaker of any covered region and notice something inaccurate in the regional conventions, dialect lists, or templates, corrections are genuinely welcome — this is exactly the kind of detail that's easy to get subtly wrong from outside a specific regional context, and the project is better for being checked against real native usage.
