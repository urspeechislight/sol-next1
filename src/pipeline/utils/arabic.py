"""Arabic text normalization for lexical lookup.

Per the lexicon-companion design (Option 2), config/lexicons/*.yaml maps
Arabic surface forms to canonical IDs. The loader normalizes each surface
key once at load time; pipeline extractors normalize their input via the
same function before lookup. Both ends agree on the same normal form, so
the runtime lookup is dict access.

Operations performed by `normalize_arabic` (in order):
  1. NFC composition (consistent decomposition).
  2. Strip diacritics (tashkīl + Quranic recitation marks).
  3. Strip kashida (tatweel — pure decoration).
  4. Normalize alif variants (إ ، أ ، آ ، ٱ → ا).
  5. Normalize alif maqsura → yāʾ (ى → ي).
  6. Normalize tāʾ marbūṭa → hāʾ (ة → ه).
  7. Collapse internal whitespace; strip outer.

Operations explicitly NOT performed:
  - Stripping the definite article (ال). Context-dependent — lexicons
    list both forms when both are attested in the corpus.
  - Stemming or lemmatization. Broken plurals and verb forms remain
    distinct. (CAMeL Tools / Farasa territory; out of scope here.)
"""

from __future__ import annotations

import re
import unicodedata

# Unicode ranges (precise; see Unicode Arabic / Arabic Supplement / Arabic
# Presentation Forms blocks):
#   U+064B–U+065F : tashkīl (fatḥa, kasra, ḍamma, sukūn, shadda, tanwīn, ...)
#   U+0670        : alif khanjariyya (superscript alif)
#   U+06D6–U+06ED : Quranic recitation marks
#   U+0640        : kashida / tatweel
#   U+0625 / U+0623 / U+0622 / U+0671 : إ ، أ ، آ ، ٱ — alif variants
#   U+0649 : ى — alif maqsura
#   U+0629 : ة — tāʾ marbūṭa
_DIACRITICS_RE = re.compile(r"[ً-ٰٟۖ-ۭ]")
_KASHIDA_RE = re.compile(r"ـ")
_ALIF_VARIANTS_RE = re.compile(r"[إأآٱ]")
_ALIF_MAQSURA_RE = re.compile(r"ى")
_TA_MARBUTA_RE = re.compile(r"ة")
_WHITESPACE_RE = re.compile(r"\s+")

_BARE_ALIF = "ا"  # ا
_YA = "ي"  # ي
_HA = "ه"  # ه


def normalize_arabic(text: str) -> str:
    """Return `text` normalized for Arabic lexical lookup.

    See module docstring for the operations performed and explicitly skipped.
    Empty / whitespace-only input returns an empty string.
    """
    text = unicodedata.normalize("NFC", text)
    text = _DIACRITICS_RE.sub("", text)
    text = _KASHIDA_RE.sub("", text)
    text = _ALIF_VARIANTS_RE.sub(_BARE_ALIF, text)
    text = _ALIF_MAQSURA_RE.sub(_YA, text)
    text = _TA_MARBUTA_RE.sub(_HA, text)
    return _WHITESPACE_RE.sub(" ", text).strip()
