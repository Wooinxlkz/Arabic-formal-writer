# Regional Conventions

The grammar and vocabulary of formal MSA does not change by region — a well-formed sentence is correct everywhere. What changes is a small set of surface conventions. Get these wrong and a document reads as "translated from somewhere else" even if the grammar is flawless.

Use **Neutral / Pan-Arab** as the default when the user doesn't specify a region or recipient. Switch only when the user names a country/institution, or the recipient context makes it obvious (e.g. "writing to the Algerian ministry of...").

## Numerals

| Region | Convention |
|---|---|
| Neutral / Pan-Arab | Western digits (0-9) |
| Maghreb (Algeria, Morocco, Tunisia, Libya, Mauritania) | Western digits (0-9) — near-universal in formal documents due to French administrative legacy |
| Gulf (Saudi, UAE, Qatar, Kuwait, Bahrain, Oman) | Arabic-Indic digits (٠-٩) common in official/government documents, Western digits common in business |
| Egypt | Arabic-Indic digits (٠-٩) traditional in official documents, Western increasingly common in business/tech |
| Levant (Syria, Lebanon, Jordan, Palestine) | Western digits (0-9) most common |

**Rule: pick one and never mix within a single document.** This is the single most common consistency failure in AI-generated Arabic documents.

## Date format

| Region | Format | Calendar |
|---|---|---|
| Maghreb | DD/MM/YYYY, Gregorian (الميلادي) by default | Gregorian; Hijri only if explicitly religious/legal context |
| Gulf | DD/MM/YYYY or written-out day name + Hijri date often included alongside Gregorian in official documents | Both, Hijri often primary in government docs |
| Egypt | DD/MM/YYYY, Gregorian | Gregorian |
| Levant | DD/MM/YYYY, Gregorian | Gregorian |

If the document is for a government/religious institution and the region isn't specified, ask or default to including both Gregorian and Hijri dates — safer than omitting.

## Honorific / address conventions

- **Neutral / most regions**: السيد / السيدة / الأستاذ / الأستاذة + full name, or السادة (plural, for addressing an institution)
- **Gulf, higher formality expected**: titles are used more heavily and consistently — سعادة (for officials), معالي (ministers+), صاحب السمو (royalty) — do not use these outside their actual rank; overusing honorifics reads as obsequious, underusing them in a Gulf government context reads as disrespectful
- **Maghreb**: السيد/السيدة is standard; French-derived professional titles (دكتور، أستاذ، مهندس) are commonly used before the name and expected in academic/technical correspondence — more so than in some other regions
- **Egypt/Levant**: similar to neutral, with أستاذ/أستاذة used more broadly as a general respectful title even outside academia

## Closing formulas (خاتمة المجاملة)

Roughly ascending formality — match to hierarchy and region:

1. مع خالص التحية — (routine, peer-level)
2. وتفضلوا بقبول فائق الاحترام — (standard formal letter closing, safe default)
3. وتفضلوا بقبول أسمى/فائق عبارات التقدير والاحترام — (higher formality, addressing officials/institutions — more common in Gulf and Maghreb government correspondence)
4. راجين من الله أن... / مع أطيب التمنيات — (softer, used in Levant/Egypt more than Gulf/Maghreb official contexts)

Default to #2 unless the recipient's rank or the region's convention calls for #3.

## Loanwords and technical terms

- Maghreb formal writing (Algeria especially) has a higher tolerance for established French technical/administrative terms transliterated or used directly when there is no common Arabic equivalent in daily administrative use (e.g. رقم التعريف الجبائي vs. informal use of "matricule fiscal" in speech — but the formal *written* document should still use the Arabic term). **Default to full Arabic even in Maghrebi context for written formal documents** — the French tolerance is a spoken/informal-writing phenomenon, not a formal-document one. Flag this distinction to the user if they ask for heavy French-term retention in a formal document.
- Gulf/Egypt formal writing has near-zero tolerance for English/French loanwords in official documents outside of proper nouns (company/product names).

## When the user names a country not listed above

Ask which of the four conventions above it's closest to, or default to Neutral / Pan-Arab and note the assumption. Don't guess a convention for a country you're not confident about.
