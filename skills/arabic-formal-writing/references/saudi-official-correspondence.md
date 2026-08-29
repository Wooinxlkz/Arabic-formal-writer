# Saudi Official Correspondence — Sourced Conventions

Unlike most of `regional-conventions.md`, which is a good-faith general summary, everything in this file is drawn from a single citable, authoritative source: **"دليل المراسلات الكتابية" (Official Correspondence Manual), 1st edition (1440H), Saudi Ministry of Finance**, published via King Saud University's faculty site. It documents the Ministry's actual internal standards for official letters (كتاب), meeting minutes (محضر), reports (تقرير), ministerial decisions (قرار وزاري), circulars (تعميم), and presentation memos (مذكرة عرض).

This is one government ministry's internal style guide, not a pan-Gulf or pan-Saudi legal standard — other Saudi ministries, and other Gulf countries, may differ. Treat this as a real, well-sourced data point for the Saudi/government-formal register specifically, not as automatically generalizable to all Gulf correspondence. Where it conflicts with the general Gulf guidance in `regional-conventions.md`, this file is the more specific and better-sourced one for Saudi government correspondence.

## Naming: كتاب vs. خطاب

This ministry's manual consistently uses **كتاب** for "official letter," not **خطاب** — its own corrections table explicitly flags "خطابي/خطابكم" as incorrect in favor of "كتابي/كتابكم." `document-templates.md` in this project uses خطاب رسمي as the general term, which remains correct and widely understood across the Arab world — but if drafting specifically for a Saudi government ministry, prefer كتاب for "the letter itself" to match this convention.

## Honorific and closing formula, by rank

The manual specifies a precise pairing of opening honorific and closing formula based on the recipient's rank — using the wrong pairing (e.g. a Minister-level closing for a Director General) is a real error, not just a stylistic slip:

| Recipient | Opening honorific | Closing formula |
|---|---|---|
| The King | خادم الحرمين الشريفين [name] حفظه الله ورعاه | وتفضلوا بقبول وافر التقدير والاحترام |
| Crown Prince | صاحب السمو الملكي الأمير [name] ...حفظه الله | (same tier as above) |
| Princes (سمو) | صاحب السمو الملكي / صاحب السمو + position (name often omitted) حفظه الله | ولسموكم أطيب تحياتي |
| Ministers / heads of government bodies (معالي) | صاحب المعالي + position, أو معالي + position سلمه الله | ولمعاليكم تحياتي |
| Multiple recipients | — | وتقبلوا تحياتي |
| Directors-general / أصحاب السعادة | — | ولكم تحياتي |

Internal ministry correspondence (within the same ministry) omits the opening honorific/dua entirely — it goes straight to السلام عليكم ورحمة الله وبركاته.

## Date format — more specific than the general Gulf guidance

For official documents and event/report dates, this manual specifies **Hijri date first, followed by the word الموافق ("corresponding to"), then the Gregorian date**, in that order — not Gregorian-primary as might be assumed:

```
12/4/1440هـ الموافق 2018/12/20م
```

This is a more specific and sourced version of the general "Gulf: both calendars, Hijri often primary" note in `regional-conventions.md`.

## Numerals — a real correction to the general assumption

This ministry's manual explicitly specifies **Western digits (0–9)** for its official correspondence, with the reversed comma (،) as the thousands separator and the period (.) as the decimal separator between riyals and halalas (e.g. `20,000.21` = 20,000 riyals and 21 halalas). This is worth flagging clearly: it runs against the common assumption (including the general note previously in `regional-conventions.md`) that Gulf official documents default to Arabic-Indic digits. At minimum, this shows the real convention varies by institution even within one country — don't assume either digit system for a Saudi government document without checking the specific receiving body's own practice.

## Subject line length

The موضوع (subject) line should be concise — the manual specifies **no more than ten words**, describing the content clearly, and should not include reference/tracking numbers (except for royal decrees and Council of Ministers resolutions, which do cite the number).

## A selection of the manual's own "correct vs. common mistake" table

This is a real official list of frequent errors in Saudi government correspondence, restructured here (not reproduced verbatim as a table) as additional calque/error patterns beyond what's in `common-calques.md`:

- Avoid the English loanword الإيميل — use البريد الإلكتروني
- "أنا كمدير لقسم..." (using كـ + noun to mean "as/in my capacity as") is discouraged — prefer "أنا بصفتي مديراً لقسم..."
- "تعتبر" is commonly overused where "تعد" (considered/regarded as) is more precise
- "سوف لن أذهب" is a redundant double negative/future construction — just "لن أذهب"
- "ينبغي على الموظف..." is a common misuse — ينبغي does not take على; use "يجب على الموظف..." instead
- Periphrastic verb constructions like "تقوم الوزارة بمتابعة ذلك" are discouraged in favor of the direct verb: "تتابع الوزارة ذلك"
- The loanword كروكي (sketch/diagram) is discouraged in favor of رسم or رفع مساحي
- "شيئ" (missing the correct hamza placement) should be "شيء" — this project's `HAMZA_ERRORS` now includes this, space-bounded to avoid false-flagging the unrelated word مشيئة

## Source

"دليل المراسلات الكتابية" (Official Correspondence Manual), 1st edition, 1440H, Saudi Ministry of Finance. Retrieved via King Saud University Faculty site: `https://faculty.ksu.edu.sa/sites/default/files/190710_dlyl_lmrslt.pdf`
