#!/usr/bin/env python3
"""
validate_wordlists.py — Static consistency checks on DIALECT_TERMS and
HAMZA_ERRORS in register_check.py.

This is a different layer of testing than tests/run_tests.py: that suite
checks behavior against sample documents. This script checks the data
itself for internal bugs that behavior tests wouldn't necessarily catch:
typos, self-contradictions, and regex-breaking entries. Both matter —
correct code operating on bad data still gives wrong answers.

Run: python3 tests/validate_wordlists.py
"""

import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "arabic-formal-writing", "scripts"))
import register_check  # noqa: E402

PASS = 0
FAIL = 0
WARN = 0


def ok(name):
    global PASS
    PASS += 1
    print(f"  ok   - {name}")


def fail(name, detail=""):
    global FAIL
    FAIL += 1
    print(f"  FAIL - {name}  {detail}")


def warn(name, detail=""):
    global WARN
    WARN += 1
    print(f"  WARN - {name}  {detail}")


def check_hamza_wrong_ne_correct():
    """A hamza 'wrong' form should never be identical to its 'correct' form —
    that would mean the entry does nothing, or worse, that it's a typo where
    someone edited one side and not the other."""
    bad = []
    for wrong, correct in register_check.HAMZA_ERRORS.items():
        if wrong.strip() == correct.strip():
            bad.append(wrong)
    if bad:
        fail("hamza entries where wrong == correct", f"{bad}")
    else:
        ok(f"all {len(register_check.HAMZA_ERRORS)} hamza entries have wrong != correct")


def check_dialect_no_empty_or_whitespace_only():
    bad = [k for k in register_check.DIALECT_TERMS if not k.strip()]
    if bad:
        fail("empty/whitespace-only dialect terms found")
    else:
        ok(f"no empty dialect term keys ({len(register_check.DIALECT_TERMS)} total)")


def check_dialect_term_not_equal_to_its_own_equivalent():
    """A dialect term flagged as informal shouldn't have an MSA 'equivalent'
    that's literally the same string — that's a no-op flag."""
    bad = []
    for term, (equivalent, family, countries) in register_check.DIALECT_TERMS.items():
        if term.strip() == equivalent.strip():
            bad.append(term)
    if bad:
        fail("dialect terms whose MSA equivalent equals the term itself", f"{bad}")
    else:
        ok("no dialect term is a no-op relative to its own MSA equivalent")


def check_dialect_terms_have_valid_region_labels():
    valid_families = set(register_check.REGION_TAXONOMY.keys())
    bad = {}
    for term, (equivalent, family, countries) in register_check.DIALECT_TERMS.items():
        if family not in valid_families:
            bad[term] = family
    if bad:
        fail("dialect terms with unrecognized family labels", f"{bad}")
    else:
        ok(f"all family labels valid ({sorted(valid_families)})")


def check_dialect_countries_belong_to_their_family():
    """A term tagged with a country code must have that country actually
    listed under its family in REGION_TAXONOMY — catches copy-paste errors
    like tagging a Gulf term with a Maghreb country code."""
    bad = []
    for term, (equivalent, family, countries) in register_check.DIALECT_TERMS.items():
        allowed = set(register_check.REGION_TAXONOMY.get(family, []))
        for c in countries:
            if c not in allowed:
                bad.append((term, family, c))
    if bad:
        fail("dialect terms with a country code that doesn't belong to their family", f"{bad}")
    else:
        ok("all country tags belong to their declared family")


def check_dialect_countries_are_known_codes():
    """Every country code used must exist in COUNTRY_NAMES (catches typos
    in the ISO code itself, e.g. 'dza' instead of 'dz')."""
    bad = []
    for term, (equivalent, family, countries) in register_check.DIALECT_TERMS.items():
        for c in countries:
            if c not in register_check.COUNTRY_NAMES:
                bad.append((term, c))
    if bad:
        fail("dialect terms with an unrecognized country code", f"{bad}")
    else:
        ok("all country codes are recognized in COUNTRY_NAMES")


def check_no_duplicate_terms_across_case_variants():
    """Catches accidental near-duplicates like 'أوكي' vs 'اوكي' being intentional
    (they are, both spellings exist) vs an actual copy-paste duplicate key,
    which Python's dict would silently overwrite rather than error on."""
    # Since DIALECT_TERMS is a dict literal, true duplicate keys are silently
    # overwritten by Python at parse time and invisible here — so instead we
    # re-read the source file and check for duplicate key lines directly.
    src_path = os.path.join(os.path.dirname(__file__), "..", "skills",
                             "arabic-formal-writing", "scripts", "register_check.py")
    with open(src_path, "r", encoding="utf-8") as f:
        src = f.read()

    dialect_block = re.search(r"DIALECT_TERMS = \{(.*?)\n\}", src, re.DOTALL)
    if not dialect_block:
        fail("could not locate DIALECT_TERMS block in source for duplicate-key scan")
        return
    keys_in_source = re.findall(r'"([^"]+)":\s*\(', dialect_block.group(1))
    seen = set()
    dupes = set()
    for k in keys_in_source:
        if k in seen:
            dupes.add(k)
        seen.add(k)
    if dupes:
        fail("duplicate DIALECT_TERMS keys found in source (Python silently keeps only the last)", f"{dupes}")
    else:
        ok(f"no duplicate keys in DIALECT_TERMS source ({len(keys_in_source)} entries scanned)")


def check_regex_compiles_for_every_term():
    """Every dialect term must produce a valid, working regex per the pattern
    construction used in check_dialect_leakage — including multi-word terms
    like 'شو في' which contain a literal space."""
    bad = []
    for term in register_check.DIALECT_TERMS:
        try:
            pattern = re.compile(r"(?<![\u0621-\u064A])" + re.escape(term) + r"(?![\u0621-\u064A])")
            pattern.search(term)  # every term should at minimum match itself in isolation
            if not pattern.search(term):
                bad.append((term, "does not match itself"))
        except re.error as e:
            bad.append((term, str(e)))
    if bad:
        fail("dialect terms with regex issues", f"{bad}")
    else:
        ok("every dialect term compiles and self-matches as a regex")


def check_hamza_entries_not_prefix_of_each_other_unexpectedly():
    """If one hamza 'wrong' string is a prefix of another, the shorter one
    firing first could mask context needed for the longer, more specific
    pattern (e.g. 'ان ' as a prefix of 'ان شاء الله' style entries). This
    project currently avoids that shape, but a future contributor could
    reintroduce it, so guard it here."""
    keys = list(register_check.HAMZA_ERRORS.keys())
    issues = []
    for i, a in enumerate(keys):
        for b in keys:
            if a != b and b.startswith(a) and len(a) < len(b):
                issues.append((a, b))
    if issues:
        warn("hamza entries where one is a prefix of another (verify intentional)", f"{issues}")
    else:
        ok("no unexpected prefix relationships among hamza entries")


def check_closing_patterns_nonempty():
    if not register_check.CLOSING_PATTERNS:
        fail("CLOSING_PATTERNS is empty")
    else:
        ok(f"CLOSING_PATTERNS has {len(register_check.CLOSING_PATTERNS)} entries")


def check_latin_whitelist_lowercase():
    """LATIN_WHITELIST is matched via .lower() in check_latin_leakage, so any
    uppercase entries in the whitelist itself would silently never match."""
    bad = [w for w in register_check.LATIN_WHITELIST if w != w.lower()]
    if bad:
        fail("LATIN_WHITELIST contains non-lowercase entries that will never match", f"{bad}")
    else:
        ok("LATIN_WHITELIST entries are all lowercase (matches .lower() comparison in code)")


def main():
    print("[validate_wordlists.py]")
    check_hamza_wrong_ne_correct()
    check_dialect_no_empty_or_whitespace_only()
    check_dialect_term_not_equal_to_its_own_equivalent()
    check_dialect_terms_have_valid_region_labels()
    check_dialect_countries_belong_to_their_family()
    check_dialect_countries_are_known_codes()
    check_no_duplicate_terms_across_case_variants()
    check_regex_compiles_for_every_term()
    check_hamza_entries_not_prefix_of_each_other_unexpectedly()
    check_closing_patterns_nonempty()
    check_latin_whitelist_lowercase()

    print(f"\n{'='*40}\n{PASS} passed, {WARN} warnings, {FAIL} failed\n{'='*40}")
    sys.exit(1 if FAIL > 0 else 0)


if __name__ == "__main__":
    main()
