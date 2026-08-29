#!/usr/bin/env python3
"""
register_check.py — Deterministic formal-Arabic register checker.

Checks a piece of Arabic text for common signals that a formal document
is not actually in a clean, consistent formal register:

  - mixed numeral systems (Western 0-9 vs Arabic-Indic ٠-٩) in one document
  - informal / dialect word leakage (Gulf, Egyptian, Levantine, Maghrebi/Darija)
  - a curated list of common hamza mistakes
  - missing subject line / closing formula for letter-type documents
  - sentence-length outliers (too choppy or true run-ons)
  - untransliterated Latin-script leakage without technical justification

This is a heuristic linter, not a grammar engine. It is designed to catch
the specific, well-documented failure modes described in
references/common-calques.md and references/regional-conventions.md —
it will not catch everything, and every flag should be reviewed by a
human (or the arabic-document-reviewer agent) before being treated as
gospel. False positives are expected and acceptable; false negatives on
these specific patterns are what the test suite guards against.

Usage:
    python3 register_check.py <path/to/file.txt>
    python3 register_check.py -                 # read from stdin
    echo "..." | python3 register_check.py - --doc-type letter --region maghreb

Exit code: 0 always in normal use (this is advisory, not a gate).
Pass --strict to exit 1 when any flag is raised (useful in CI/tests).
"""

import sys
import re
import json
import argparse
from dataclasses import dataclass, field, asdict
from typing import Optional


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

ARABIC_INDIC_DIGITS = set("٠١٢٣٤٥٦٧٨٩")
WESTERN_DIGITS = set("0123456789")

# Curated, labeled dialect/informal terms -> MSA equivalent.
# Not exhaustive by design — see module docstring. Region label is informational.
DIALECT_TERMS = {
    # Egyptian
    "عايز": ("أريد", "egyptian"),
    "عاوز": ("أريد", "egyptian"),
    "ازيك": ("كيف حالك", "egyptian"),
    "كده": ("هكذا", "egyptian"),
    "مش": ("ليس", "egyptian"),
    "ايه": ("ماذا", "egyptian"),
    "دلوقتي": ("الآن", "egyptian"),
    "لسه": ("ما زال / حتى الآن", "egyptian"),
    "علشان": ("لأجل / من أجل", "egyptian"),
    "فين": ("أين", "egyptian"),
    "بجد": ("حقاً", "egyptian"),
    # Gulf
    "شلونك": ("كيف حالك", "gulf"),
    "وايد": ("كثيراً", "gulf"),
    "شنو": ("ماذا", "gulf"),
    "عيل": ("إذاً", "gulf"),
    "چذي": ("هكذا", "gulf"),
    "يبه": ("يا هذا", "gulf"),
    "شخبارك": ("كيف حالك", "gulf"),
    "الحين": ("الآن", "gulf"),
    "مو": ("ليس", "gulf"),
    # Levantine
    "شو": ("ماذا", "levantine"),
    "هيك": ("هكذا", "levantine"),
    "منيح": ("جيد", "levantine"),
    "هلق": ("الآن", "levantine"),
    "كتير": ("كثيراً", "levantine"),
    "ليش": ("لماذا", "levantine"),
    "بدي": ("أريد", "levantine"),
    "شو في": ("ما الأمر", "levantine"),
    # Maghrebi / Darija
    "بزاف": ("كثيراً", "maghrebi"),
    "واش": ("هل", "maghrebi"),
    "دابا": ("الآن", "maghrebi"),
    "كاين": ("يوجد", "maghrebi"),
    "ماكاش": ("لا يوجد", "maghrebi"),
    "ماكاينش": ("لا يوجد", "maghrebi"),
    "راه": ("إنّ / في الواقع", "maghrebi"),
    "بصح": ("لكن", "maghrebi"),
    "نتاع": ("الخاص بـ", "maghrebi"),
    "بغيت": ("أردت / أريد", "maghrebi"),
    "علاش": ("لماذا", "maghrebi"),
    "شحال": ("كم", "maghrebi"),
    "مليح": ("جيد", "maghrebi"),
    # Pan-dialect / chat-register informal words that leak in from any region
    "أوكي": ("حسناً", "informal-chat"),
    "اوكي": ("حسناً", "informal-chat"),
    "يلا": ("هيا", "informal-chat"),
    "هاي": ("مرحباً", "informal-chat"),
    "بايباي": ("مع السلامة", "informal-chat"),
    "ثانكس": ("شكراً", "informal-chat"),
}

# Curated common hamza errors: (wrong_form -> correct_form).
# Kept intentionally short and high-confidence to limit false positives.
HAMZA_ERRORS = {
    "هاذا": "هذا",
    "هاذه": "هذه",
    "انشاء الله": "إن شاء الله",
    "ان شاء الله": "إن شاء الله",
    "الان": "الآن",
    "او ": "أو ",  # trailing space avoids matching inside other words
    "اخر ": "آخر ",
    "اسلوب": "أسلوب",
    "اخبار": "أخبار",
    "امور": "أمور",
    "اجل": "أجل",
    "اعمال": "أعمال",
    "امكانية": "إمكانية",
    "استاذ": "أستاذ",
    "ابدا": "أبداً",
    "اجابة": "إجابة",
    "امس": "أمس",
    "انسان": "إنسان",
}

# Closing formulas recognized as valid formal closings (see regional-conventions.md)
CLOSING_PATTERNS = [
    "مع خالص التحية",
    "تفضلوا بقبول فائق الاحترام",
    "تفضلوا بقبول أسمى",
    "تفضلوا بقبول عبارات التقدير",
    "أطيب التمنيات",
    "وتفضلوا بقبول",
]

SUBJECT_LINE_PATTERN = re.compile(r"الموضوع\s*[:：]")

# Latin-script sequences allowed without flagging (common legitimate tech/brand terms).
LATIN_WHITELIST = {
    "email", "e-mail", "linkedin", "cv", "pdf", "url", "wifi", "usb",
}


@dataclass
class Flag:
    check: str
    severity: str  # "error" | "warning" | "info"
    message: str
    snippet: str = ""
    suggestion: str = ""


@dataclass
class Report:
    flags: list = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def add(self, check, severity, message, snippet="", suggestion=""):
        self.flags.append(Flag(check, severity, message, snippet, suggestion))

    def to_dict(self):
        return {
            "flags": [asdict(f) for f in self.flags],
            "stats": self.stats,
            "flag_count": len(self.flags),
        }


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_numeral_consistency(text: str, report: Report):
    western = sum(1 for c in text if c in WESTERN_DIGITS)
    indic = sum(1 for c in text if c in ARABIC_INDIC_DIGITS)
    report.stats["western_digit_count"] = western
    report.stats["arabic_indic_digit_count"] = indic
    if western > 0 and indic > 0:
        report.add(
            check="numeral_consistency",
            severity="error",
            message=(
                f"Document mixes Western digits ({western} found) and "
                f"Arabic-Indic digits ({indic} found). Pick one convention "
                "for the whole document — see references/regional-conventions.md."
            ),
        )


def check_dialect_leakage(text: str, report: Report):
    for term, (equivalent, region) in DIALECT_TERMS.items():
        # word-boundary-ish match using surrounding whitespace/punctuation
        pattern = re.compile(r"(?<![\u0621-\u064A])" + re.escape(term) + r"(?![\u0621-\u064A])")
        matches = pattern.findall(text)
        if matches:
            report.add(
                check="dialect_leakage",
                severity="warning",
                message=(
                    f"Found informal/dialect term '{term}' ({region}) "
                    f"{len(matches)}x in a formal document."
                ),
                snippet=term,
                suggestion=f"Use '{equivalent}' instead.",
            )


def check_hamza_errors(text: str, report: Report):
    for wrong, correct in HAMZA_ERRORS.items():
        if wrong in text:
            count = text.count(wrong)
            report.add(
                check="hamza_error",
                severity="warning",
                message=f"Possible hamza/spelling issue: '{wrong.strip()}' found {count}x. Verify in context.",
                snippet=wrong.strip(),
                suggestion=f"Likely correct form: '{correct.strip()}'.",
            )


def check_letter_conventions(text: str, doc_type: Optional[str], report: Report):
    if doc_type not in ("letter", "admin", "correspondence"):
        return
    if not SUBJECT_LINE_PATTERN.search(text):
        report.add(
            check="missing_subject_line",
            severity="error",
            message="No 'الموضوع:' subject line found — required for official/admin letters.",
            suggestion="Add 'الموضوع: ...' near the top of the letter.",
        )
    if not any(p in text for p in CLOSING_PATTERNS):
        report.add(
            check="missing_closing_formula",
            severity="warning",
            message="No recognized formal closing formula found before the signature.",
            suggestion="See references/regional-conventions.md for closing formula options by formality level.",
        )


def _split_sentences(text: str):
    # Split on Arabic/Latin sentence-enders. Keep it simple and dependency-free.
    parts = re.split(r"[.!؟?]+", text)
    return [p.strip() for p in parts if p.strip()]


def check_sentence_length(text: str, report: Report):
    sentences = _split_sentences(text)
    if not sentences:
        return
    word_counts = [len(s.split()) for s in sentences]
    avg = sum(word_counts) / len(word_counts)
    report.stats["sentence_count"] = len(sentences)
    report.stats["avg_words_per_sentence"] = round(avg, 1)

    if avg < 4 and len(sentences) >= 3:
        report.add(
            check="sentence_rhythm",
            severity="info",
            message=(
                f"Average sentence length is very short ({avg:.1f} words). "
                "Formal MSA typically favors coordinated clauses (و، حيث، إذ) "
                "over many short standalone sentences — see references/common-calques.md."
            ),
        )

    for s, wc in zip(sentences, word_counts):
        if wc > 60:
            report.add(
                check="run_on_sentence",
                severity="warning",
                message=f"Sentence has {wc} words — likely a run-on, consider splitting.",
                snippet=(s[:80] + "…") if len(s) > 80 else s,
            )


def check_latin_leakage(text: str, report: Report):
    for match in re.finditer(r"[A-Za-zÀ-ÿ]{2,}", text):
        word = match.group(0)
        low = word.lower()
        if low in LATIN_WHITELIST:
            continue
        if word.isupper() and len(word) <= 5:
            # likely an acronym/brand — don't flag
            continue
        report.add(
            check="latin_script_leakage",
            severity="info",
            message=f"Untransliterated Latin-script word '{word}' found — verify it's a justified proper noun/technical term.",
            snippet=word,
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def analyze(text: str, doc_type: Optional[str] = None, region: Optional[str] = None) -> dict:
    report = Report()
    report.stats["char_count"] = len(text)
    report.stats["doc_type"] = doc_type
    report.stats["region"] = region

    check_numeral_consistency(text, report)
    check_dialect_leakage(text, report)
    check_hamza_errors(text, report)
    check_letter_conventions(text, doc_type, report)
    check_sentence_length(text, report)
    check_latin_leakage(text, report)

    return report.to_dict()


def _read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Formal Arabic register checker")
    parser.add_argument("path", help="Path to a text file, or '-' for stdin")
    parser.add_argument("--doc-type", default=None,
                         choices=["letter", "admin", "correspondence", "cv", "report",
                                  "memo", "minutes", "contract", "other"],
                         help="Document type, enables extra checks (e.g. subject line for letters)")
    parser.add_argument("--region", default=None,
                         choices=["neutral", "gulf", "egypt", "levant", "maghreb"],
                         help="Regional convention context (informational, included in output)")
    parser.add_argument("--strict", action="store_true",
                         help="Exit with code 1 if any flag was raised (useful for CI/tests)")
    parser.add_argument("--json", action="store_true",
                         help="Print raw JSON only (no human-readable summary)")
    args = parser.parse_args()

    text = _read_input(args.path)
    result = analyze(text, doc_type=args.doc_type, region=args.region)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"--- register_check.py report ---")
        print(f"stats: {json.dumps(result['stats'], ensure_ascii=False)}")
        print(f"flags: {result['flag_count']}")
        for f in result["flags"]:
            print(f"  [{f['severity'].upper()}] {f['check']}: {f['message']}")
            if f.get("snippet"):
                print(f"      snippet: {f['snippet']}")
            if f.get("suggestion"):
                print(f"      suggestion: {f['suggestion']}")
        print(json.dumps(result, ensure_ascii=False))  # machine-readable line for tooling

    if args.strict and result["flag_count"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
