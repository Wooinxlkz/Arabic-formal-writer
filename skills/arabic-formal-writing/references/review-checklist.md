# Manual Review Checklist

Used by the `arabic-document-reviewer` agent, and applicable by the main skill directly for a lighter self-review pass. This is the layer that catches what `register_check.py` structurally cannot — actual judgment calls.

Run through every item; don't skip any silently.

## 1. Structural fit
- [ ] Does the document match the correct template in `document-templates.md` for its type?
- [ ] Is anything present that shouldn't be for this document type (e.g. emotional language in an administrative complaint, a photo/personal-info field in a CV that wasn't requested)?
- [ ] Is anything conventionally required missing (subject line on a letter, decisions section on minutes)?

## 2. Register consistency
- [ ] Is the formality tier (`tone-tiers.md`) consistent from opening to closing? A common failure: Tier 1 opener with a Tier 3 closing, or vice versa.
- [ ] Does the closing formula's formality actually match the addressee's implied rank/relationship?
- [ ] Any single sentence that reads noticeably more/less formal than its neighbors?

## 3. Regional convention correctness
- [ ] If a region was specified or implied, does the document follow that region's numeral/date/honorific conventions (`regional-conventions.md`), not a different region's by default?
- [ ] If no region was specified, does it use Neutral / Pan-Arab conventions rather than accidentally defaulting to one region's specific norms?

## 4. Naturalness (the hardest, most important check)
- [ ] Read the document as if you were the native recipient. Does any sentence make you pause and think "a person wouldn't actually write it this way"? That's a calque or an over-literal structure — flag it even if grammatically correct.
- [ ] Are there any stacked hedges, English-style topic-fronting, or short choppy sentence chains per `common-calques.md`?
- [ ] Would this document, shown to a native formal-Arabic writer from the target region, be identifiable as AI-assisted or translated? If yes, identify specifically why and fix it — don't just note the concern.

## 5. Content correctness (not this skill's job to verify facts, but check obvious issues)
- [ ] Any placeholder text left un-filled ([اسم]، [التاريخ] etc.) that should have been resolved?
- [ ] For contracts specifically: is the legal-review disclaimer present per `document-templates.md` §8?
- [ ] Internal consistency — does a date/name/number mentioned once match if it's referenced again later in the document?

## Output format for the review

When acting as the reviewer agent, report back:
1. **Pass/needs-work** verdict per section above (not just overall)
2. Specific line/phrase quotes for anything flagged, with the suggested fix
3. A final corrected version if requested, or a list of changes if the user wants to apply them themselves
