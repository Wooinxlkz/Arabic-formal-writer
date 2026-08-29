#!/usr/bin/env python3
"""
Test suite for register_check.py.

Runs the checker against fixture documents (one clean, one deliberately
flawed) and asserts on the specific checks we expect to fire or stay
silent. This is a real regression test, not a smoke test — if you change
register_check.py and these fail, you broke something specific.

Run: python3 tests/run_tests.py
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "arabic-formal-writing", "scripts"))
import register_check  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")

PASS = 0
FAIL = 0


def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ok   - {name}")
    else:
        FAIL += 1
        print(f"  FAIL - {name}  {detail}")


def load(fixture):
    with open(os.path.join(FIXTURES, fixture), "r", encoding="utf-8") as f:
        return f.read()


def checks_by_name(result, check_name):
    return [f for f in result["flags"] if f["check"] == check_name]


def test_good_letter():
    print("\n[test_good_letter]")
    text = load("good_letter.txt")
    result = register_check.analyze(text, doc_type="letter", region="maghreb")

    check("no numeral consistency flag",
          len(checks_by_name(result, "numeral_consistency")) == 0,
          f"got {checks_by_name(result, 'numeral_consistency')}")
    check("no dialect leakage flags",
          len(checks_by_name(result, "dialect_leakage")) == 0,
          f"got {checks_by_name(result, 'dialect_leakage')}")
    check("subject line detected (no missing_subject_line flag)",
          len(checks_by_name(result, "missing_subject_line")) == 0)
    check("closing formula detected (no missing_closing_formula flag)",
          len(checks_by_name(result, "missing_closing_formula")) == 0)
    check("no hamza errors flagged",
          len(checks_by_name(result, "hamza_error")) == 0,
          f"got {checks_by_name(result, 'hamza_error')}")


def test_flawed_letter():
    print("\n[test_flawed_letter]")
    text = load("flawed_letter.txt")
    result = register_check.analyze(text, doc_type="letter", region="maghreb")

    check("numeral consistency flag fires (mixed digits)",
          len(checks_by_name(result, "numeral_consistency")) == 1)
    check("dialect leakage detects at least 3 distinct terms",
          len(checks_by_name(result, "dialect_leakage")) >= 3,
          f"got {len(checks_by_name(result, 'dialect_leakage'))}")
    check("catches 'عايز' specifically",
          any(f["snippet"] == "عايز" for f in checks_by_name(result, "dialect_leakage")))
    check("catches 'واش' specifically",
          any(f["snippet"] == "واش" for f in checks_by_name(result, "dialect_leakage")))
    check("missing subject line flagged",
          len(checks_by_name(result, "missing_subject_line")) == 1)
    check("missing closing formula flagged",
          len(checks_by_name(result, "missing_closing_formula")) == 1)
    check("hamza errors flagged (هاذا / انشاء الله / او)",
          len(checks_by_name(result, "hamza_error")) >= 2,
          f"got {checks_by_name(result, 'hamza_error')}")
    check("flag_count is nonzero overall",
          result["flag_count"] > 0)


def test_numeral_consistency_isolated():
    print("\n[test_numeral_consistency_isolated]")
    western_only = register_check.analyze("هذا نص فيه رقم 123 فقط.")
    check("western-only digits: no flag",
          len(checks_by_name(western_only, "numeral_consistency")) == 0)

    indic_only = register_check.analyze("هذا نص فيه رقم ١٢٣ فقط.")
    check("arabic-indic-only digits: no flag",
          len(checks_by_name(indic_only, "numeral_consistency")) == 0)

    mixed = register_check.analyze("هذا نص فيه رقم 123 و ١٢٣ معاً.")
    check("mixed digits: flag fires",
          len(checks_by_name(mixed, "numeral_consistency")) == 1)


def test_latin_leakage_whitelist():
    print("\n[test_latin_leakage_whitelist]")
    text = "أرسل السيرة الذاتية عبر email أو CV بصيغة PDF."
    result = register_check.analyze(text)
    flagged_words = {f["snippet"] for f in checks_by_name(result, "latin_script_leakage")}
    check("whitelisted terms (email/CV/PDF) not flagged",
          "email" not in flagged_words and "CV" not in flagged_words and "PDF" not in flagged_words,
          f"flagged: {flagged_words}")

    text2 = "سأقوم بذلك ASAP وسأخبرك whatever happens."
    result2 = register_check.analyze(text2)
    flagged_words2 = {f["snippet"] for f in checks_by_name(result2, "latin_script_leakage")}
    check("non-whitelisted lowercase word 'whatever' flagged",
          "whatever" in flagged_words2,
          f"flagged: {flagged_words2}")


def test_sentence_rhythm():
    print("\n[test_sentence_rhythm]")
    choppy = "جئت. رأيت. كتبت. ذهبت. عدت. انتهيت."
    result = register_check.analyze(choppy)
    check("very short choppy sentences trigger sentence_rhythm info flag",
          len(checks_by_name(result, "sentence_rhythm")) == 1)

    normal = load("good_letter.txt")
    result2 = register_check.analyze(normal)
    check("normal letter does not trigger sentence_rhythm flag",
          len(checks_by_name(result2, "sentence_rhythm")) == 0)


def test_doc_type_gating():
    print("\n[test_doc_type_gating]")
    # Without doc_type=letter, missing subject/closing checks should not run at all.
    text = "نص عادي بدون أي بنية رسالة رسمية."
    result = register_check.analyze(text, doc_type=None)
    check("no doc_type: subject/closing checks don't fire",
          len(checks_by_name(result, "missing_subject_line")) == 0 and
          len(checks_by_name(result, "missing_closing_formula")) == 0)

    result2 = register_check.analyze(text, doc_type="cv")
    check("doc_type=cv: subject/closing checks don't fire (letter-only checks)",
          len(checks_by_name(result2, "missing_subject_line")) == 0 and
          len(checks_by_name(result2, "missing_closing_formula")) == 0)


def test_khales_closing_not_flagged_as_dialect():
    """Regression test for a real bug found via CAMeL Lab frequency-list
    cross-check: خالص is legitimate MSA (appears in the standard formal
    closing 'مع خالص التحية', listed in CLOSING_PATTERNS itself) and must
    never be flagged as Egyptian dialect leakage, or every letter using our
    own recommended closing formula would incorrectly fail its own check."""
    print("\n[test_khales_closing_not_flagged_as_dialect]")
    text = (
        "الموضوع: طلب معلومات\n\n"
        "السيد المدير المحترم،\n"
        "تحية طيبة وبعد،\n\n"
        "أرجو منكم موافاتي بالمعلومات المطلوبة في أقرب وقت ممكن.\n\n"
        "مع خالص التحية،\n"
        "الاسم"
    )
    result = register_check.analyze(text, doc_type="letter")
    check("'خالص' inside the standard closing formula is not flagged as dialect leakage",
          not any(f["snippet"] == "خالص" for f in checks_by_name(result, "dialect_leakage")),
          f"got {checks_by_name(result, 'dialect_leakage')}")
    check("the standard closing itself is recognized (no missing_closing_formula flag)",
          len(checks_by_name(result, "missing_closing_formula")) == 0)


def main():
    test_good_letter()
    test_flawed_letter()
    test_numeral_consistency_isolated()
    test_latin_leakage_whitelist()
    test_sentence_rhythm()
    test_doc_type_gating()
    test_khales_closing_not_flagged_as_dialect()

    print(f"\n{'='*40}\n{PASS} passed, {FAIL} failed\n{'='*40}")
    sys.exit(1 if FAIL > 0 else 0)


if __name__ == "__main__":
    main()
