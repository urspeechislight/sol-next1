"""Tests for Arabic text normalization (pipeline.utils.arabic)."""

from __future__ import annotations

from pipeline.utils.arabic import normalize_arabic


def test_should_strip_diacritics_when_normalizing() -> None:
    """Tashkīl (fatḥa, kasra, ḍamma, sukūn, shadda) is stripped."""
    assert normalize_arabic("ثِقَة") == normalize_arabic("ثقة")
    assert normalize_arabic("صَدُوقٌ") == normalize_arabic("صدوق")


def test_should_normalize_alif_variants_when_present() -> None:
    """إ ، أ ، آ ، ٱ all collapse to bare alif ا."""
    bare = normalize_arabic("امام")
    assert normalize_arabic("إمام") == bare
    assert normalize_arabic("أمام") == bare
    assert normalize_arabic("آمام") == bare


def test_should_normalize_alif_maqsura_to_ya_when_present() -> None:
    """ى → ي for matching."""
    assert normalize_arabic("على") == normalize_arabic("علي")


def test_should_normalize_ta_marbuta_to_ha_when_present() -> None:
    """ة → ه for matching."""
    assert normalize_arabic("ثقة") == normalize_arabic("ثقه")


def test_should_strip_kashida_when_present() -> None:
    """Tatweel (ـ) is decoration only — strip it."""
    assert normalize_arabic("مســـلســـل") == normalize_arabic("مسلسل")


def test_should_collapse_internal_whitespace_when_normalizing() -> None:
    """Multi-space and tab runs collapse to single space; outer is stripped."""
    assert normalize_arabic("مجهول    الحال") == normalize_arabic("مجهول الحال")
    assert normalize_arabic("  ثقة  ") == "ثقه"


def test_should_return_empty_string_when_input_is_only_diacritics() -> None:
    """Diacritic-only input normalizes to empty."""
    assert normalize_arabic("ًٌٍَُِّْ") == ""


def test_should_keep_definite_article_when_normalizing() -> None:
    """The definite article ال is context-dependent; the normalizer leaves it."""
    assert normalize_arabic("الثقة") != normalize_arabic("ثقة")
    assert normalize_arabic("الثقة").startswith("ال")
