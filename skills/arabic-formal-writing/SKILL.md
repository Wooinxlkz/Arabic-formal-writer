---
name: arabic-formal-writing
description: Write, translate, or review formal Modern Standard Arabic (MSA) documents — official/business letters, administrative correspondence, CVs, resumes, cover letters, reports, memos, minutes, and simple contracts/agreements. Make sure to use this skill whenever the user asks for Arabic writing help involving anything official, professional, administrative, academic, or business-related — letters to institutions, government correspondence, job applications, formal emails, reports — even if they don't say "formal" explicitly, and even if the request is in English but the output should be in Arabic. Also use this skill to review or correct existing Arabic formal text for register consistency, calque/translation artifacts, numeral and date-format consistency, and regional-convention correctness (Gulf, Egyptian, Levantine, or Maghrebi/Algerian formal norms). Do NOT use this skill for casual chat, social media captions, or marketing copy in Arabic — that is a different register entirely.
---

# Arabic Formal Writing

A skill for producing and reviewing formal Modern Standard Arabic (MSA) documents that read like they were written by a native professional — not translated, not dialect-leaking, and not defaulting to one region's conventions when the user didn't ask for that.

## Why this skill exists

Most Arabic writing help available today (including generic prompting) has three recurring problems:
1. **It defaults to Gulf or Egyptian formal conventions** even when the user is writing from or to the Maghreb, the Levant, or wants neutral Pan-Arab MSA.
2. **It reads as translated** — English/French sentence structure wearing Arabic words (calques), overly literal connectors, wrong sentence rhythm.
3. **It mixes registers** — a dialect word or informal phrase slipping into an otherwise formal document, or Western/Arabic-Indic numerals used inconsistently in the same document.

This skill exists to catch and prevent exactly those three failure modes, using a real checklist and a deterministic script — not just "write formally" as an instruction.

## Step 1 — Establish the brief

Before writing, determine (ask only what's not inferable from context):
- **Document type**: official letter, admin correspondence, CV/resume, cover letter, report, memo, meeting minutes, or simple contract/agreement. See `references/document-templates.md` for the full list and structure of each.
- **Regional convention**: Gulf, Egyptian, Levantine, Maghrebi/Algerian, or neutral Pan-Arab (default when unspecified — see `references/regional-conventions.md`). This affects date format, honorifics, numeral convention, and a handful of standard closing phrases — NOT the core grammar, which is always standard MSA.
- **Recipient/purpose**: who it's going to (institution, employer, individual) and what outcome the user wants — this shapes tone level (there are three formality tiers within MSA itself; see below).
- **Language of the brief vs. output**: the user may describe the request in English/French/Darija — the output is MSA regardless, unless they explicitly ask for a bilingual document.

If the user says "just write it," proceed with neutral Pan-Arab MSA conventions and the formality tier that matches the document type by default (see `references/tone-tiers.md`), and note the assumption briefly in your reply.

## Step 2 — Draft using the right structural template

Open `references/document-templates.md` and use the matching template for structure (opening address, body ordering, closing, signature block). Do not invent structure freehand for official letters or CVs — these have real conventions that native readers expect, and deviating reads as foreign.

Key non-negotiables while drafting:
- **Numerals**: pick ONE convention (Western 0-9 or Arabic-Indic ٠-٩) for the whole document and stay consistent. Neutral MSA and Maghrebi contexts almost always use Western numerals in formal documents; Gulf/Egyptian formal documents often use Arabic-Indic. Default per `references/regional-conventions.md` unless the user specifies.
- **Hamza correctness**: أ / إ / ا / ء / ئ / ؤ placement is a formality signal — get it right, don't approximate.
- **No calques**: don't translate English/French idioms literally into Arabic. Say it the way a native formal-Arabic document would say it, even if the phrasing diverges from the source language structure.
- **Sentence rhythm**: formal Arabic favors coordinated clauses (و، حيث، إذ) over the short choppy sentences typical of translated English. But don't over-correct into run-ons — see the check in Step 3 for the acceptable range.
- **One register only**: no dialect words, no code-switched English/French terms unless they're the standard technical term with no established Arabic equivalent (e.g. a software product name).

## Step 3 — Run the register check (do this every time, not optionally)

Run the bundled checker against your draft before presenting it:

```bash
python3 scripts/register_check.py <path-to-draft.txt-or-paste-via-stdin>
```

Or pipe text directly:
```bash
echo "النص هنا" | python3 scripts/register_check.py -
```

The script checks, deterministically:
- Numeral consistency (mixed Western/Arabic-Indic digits)
- Dialect/informal word leakage (flags common Gulf/Egyptian/Levantine/Darija colloquialisms with their MSA equivalents)
- Common hamza errors (a curated pattern list, not exhaustive — still use your own judgment)
- Missing opening/closing conventions for letter-type documents
- Average sentence length outliers (too choppy = translated-feeling; too run-on = unreadable)
- Latin-script leakage (untransliterated English/French words with no technical justification)

Fix every flag before presenting the document, or explain to the user why a flag is a false positive in that specific case (e.g., a brand name correctly left in Latin script).

For a deeper structural/tone review beyond what the script catches, delegate to the `arabic-document-reviewer` agent bundled with this plugin — it applies the full checklist in `references/review-checklist.md` including things a script can't catch (actual tone appropriateness, cultural register, whether the closing formula matches the relationship/hierarchy implied).

## Step 4 — Present the result

Give the user:
1. The final Arabic document
2. A one-line note of which regional convention and formality tier you used (so they can ask for a different one)
3. If they asked for review/correction rather than fresh drafting, a short summary of what was changed and why — not a line-by-line diff unless asked

## Reference files

- `references/document-templates.md` — structure for every supported document type
- `references/regional-conventions.md` — Gulf/Egyptian/Levantine/Maghrebi conventions: numerals, dates, honorifics, closings
- `references/tone-tiers.md` — the three MSA formality tiers and which documents use which
- `references/review-checklist.md` — the full manual checklist used by the reviewer agent
- `references/common-calques.md` — a running list of English/French → bad-Arabic calques to avoid, with correct alternatives

## Testing

This skill ships with `tests/` containing real sample drafts (good and deliberately flawed) and expected `register_check.py` output. If you modify `register_check.py`, run:

```bash
python3 tests/run_tests.py
```

before considering the change done. All tests must pass — this is a deterministic script, not a vibe check.
