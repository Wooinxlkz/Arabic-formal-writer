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

This project's dialect/hamza lists were originally compiled from general knowledge. As of the v1.3.0 update, the full `DIALECT_TERMS` list has been cross-checked against real corpus-frequency data — see "Validation performed" below for what that found and changed. Further expansion should follow the same approach rather than reverting to unchecked additions.

The Arabic-NLP research community maintains real, annotated dialect resources that are a categorically stronger validation source than another AI-generated wordlist:

- **CAMeL Lab Arabic Frequency Lists** (Khalifa et al., 2021, NYU Abu Dhabi) — word-frequency counts derived from the CAMeLBERT pretraining corpus, split by variety: Classical Arabic (2.4M unique words / 847M tokens), Dialectal Arabic — mixed dialects (6.7M unique words / 5.8B tokens), and MSA (11.4M unique words / 12.6B tokens). Openly downloadable (GitHub Releases, no license gate). `https://github.com/CAMeL-Lab/Camel_Arabic_Frequency_Lists` — this is what was actually used for the v1.3.0 cross-check below.
- **MADAR Corpus & Lexicon** (Bouamor et al., 2018, NYU Abu Dhabi CAMeL Lab) — ~47,000 dialect→MSA/English/French entries across 25 Arabic city dialects. Requires a signed data-license agreement to download. `https://camel.abudhabi.nyu.edu/madar/`
- **NADI** (UBC-NLP) — annual country/province-level dialect ID shared-task corpora, all 21 Arab countries. `https://github.com/UBC-NLP/nadi`
- **QADI** (QCRI) — dialect ID from real social-media text. `https://github.com/qcri/QADI`
- **Darija Open Dataset (DODa)** — ~150,000 Darija↔English entries, specifically Moroccan. Licensed **CC BY-NC 4.0** (non-commercial) — usable to verify individual terms, but its data must not be bulk-copied into this MIT-licensed repo. `https://github.com/darija-open-dataset/dataset`

## Validation performed (v1.3.0)

Every entry in `DIALECT_TERMS` was checked against the CAMeL Lab frequency lists by computing each word's frequency ratio between the Dialectal Arabic (DA) corpus and the Modern Standard Arabic (MSA) corpus. A high DA/MSA ratio means a term is genuinely dialect-skewed; a ratio near or below 1 means the term is roughly as common in real MSA text as in dialectal text — i.e. it's a poor signal for "informal leakage" and risks false-positiving correct formal writing.

**Six terms were removed** for having a DA/MSA ratio at or below 1.5, each with a plausible legitimate-MSA explanation confirmed by inspection:
- `خالص` (ratio 0.8) — legitimate MSA word ("pure/sincere/exempt"); critically, it also appears inside this project's own recommended closing formula `مع خالص التحية`. Its presence in `DIALECT_TERMS` was a genuine self-contradiction bug: a document using our own recommended closing would have been incorrectly flagged. A regression test (`test_khales_closing_not_flagged_as_dialect`) now guards against reintroducing this.
- `تمام` (ratio 0.8) — legitimate MSA word ("completion/perfection")
- `قاع` (ratio 0.6) — legitimate MSA word ("floor/bottom", e.g. قاع البحر)
- `هلأ` (ratio 0.7) — no clear positive dialectal signal in the corpus data
- `أبغى` (ratio 1.0) — overlaps with the classical/MSA root بغى / ابتغى ("to seek/desire")
- `زين` (ratio 1.5) — overlaps with classical/poetic MSA usage ("adorned/beautiful")

**One entry was corrected and one added** after cross-checking against DODa (Moroccan-specific): the original `ماكاش` entry does not appear in the Moroccan Darija corpus at all — the attested Moroccan form is `ماكاينش`/`ماكاين`. Rather than replace it outright, both are now kept: CAMeL's aggregated cross-dialect data confirms `ماكاش` is real and strongly dialectal (ratio 11.5) — just more specifically Algerian/Tunisian than Moroccan — while `ماكاينش` (ratio 6.6) covers the Moroccan form.

**One term was kept despite a borderline ratio**, noted here for transparency rather than silently kept: `كاين` (ratio 1.5) has no identified MSA homograph and is a core, extremely common Maghrebi term ("there is/exists"), so it was retained — but the ratio is genuinely weaker than most of the list, and it's a reasonable candidate for future review if it turns out to false-positive in practice.

The full before/after list is in `CHANGELOG.md`.

## No data collection, no network calls

This plugin performs no network requests, collects no user data, and sends nothing anywhere. `register_check.py` runs entirely locally against the text you give it. The skill and agent instructions direct Claude's behavior when the plugin is active; they do not by themselves transmit any information beyond Claude's normal operation.

## Attribution

Built by Karim ([@Wooinxlkz](https://github.com/Wooinxlkz)) as an independent, original project. No third-party code, models, or datasets are bundled — `register_check.py` uses only the Python 3 standard library.

## Feedback and corrections

If you're a native speaker of any covered region and notice something inaccurate in the regional conventions, dialect lists, or templates, corrections are genuinely welcome — this is exactly the kind of detail that's easy to get subtly wrong from outside a specific regional context, and the project is better for being checked against real native usage.
