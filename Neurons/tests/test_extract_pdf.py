import types
import pytest

# Import the functions under test
from app.extract_pdf import (
    extract_font_styles,
    extract_logo_safezone_styles,
    extract_logo_colours,
    extract_palette_styles,
    extract_brand_compliance,
)

# ---------- helpers: fake PyMuPDF doc/page ----------
# Simply just fake text
class _FakePage:
    def __init__(self, text):
        self._text = text
    def get_text(self):
        return self._text

# A document of fake pages
class _FakeDoc:
    def __init__(self, pages_texts):
        # pages_texts: list[str]
        self._pages = [_FakePage(t) for t in pages_texts]
    def __iter__(self):
        return iter(self._pages)
    def close(self):
        pass

# Utility to patch fitz.open to return our fake doc
# Monkey patch is essentially just setting a fake attribute
# In this case we set the "fitz", i.e. "pymupdf", inside of the "extract_pdf.py" to use the fake pdf reader
# After pytest is run, the attributes are reset
def _patch_fitz_open(monkeypatch, pages_texts):
    import app.extract_pdf as mod
    def fake_open(*args, **kwargs):
        return _FakeDoc(pages_texts)
    monkeypatch.setattr(mod, "fitz", types.SimpleNamespace(open=fake_open))

# ---------- tests ----------

def test_extract_font_styles_primary_secondary(monkeypatch):
    # Simulate a PDF with lines where "Primary" and "Secondary" headings
    # are followed by font names on the next line (case-insensitive).
    text = "\n".join([
        "Random header",
        "PRIMARY",
        "Roboto Bold",
        "Some other line",
        "secondary",
        "Inter Regular",
        "Tail text"
    ])
    _patch_fitz_open(monkeypatch, [text])

    out = extract_font_styles(b"<pdf-bytes-ignored>")
    assert out == {
        "Primary": "Roboto Bold",
        "Secondary": "Inter Regular",
    }

def test_extract_font_styles_missing_headings(monkeypatch):
    # No Primary/Secondary; should return empty dict
    text = "Just a page without those headings"
    _patch_fitz_open(monkeypatch, [text])
    out = extract_font_styles(b"...")
    assert out == {}

def test_extract_logo_safezone_basic(monkeypatch):
    # The function:
    # - finds the first section containing "the safe zone"
    # - collects lines until blank/yes/no
    # - extracts a sentence containing "x is" as Value
    # - rest becomes Requirements
    lines = [
        "Introduction",
        "The Safe Zone",                    # start
        "For the logo, the safe zone is defined.",
        "Typically, X is equal to the height of the N.",
        "Keep clear space around the mark.",
        "YES",                               # stop
        "Another section"
    ]
    text = "\n".join(lines)
    _patch_fitz_open(monkeypatch, [text])

    out = extract_logo_safezone_styles(b"...")
    # Value should contain the sentence with "x is"
    assert "Value" in out and "x is" in out["Value"].lower()
    # Requirements should be the rest of the paragraph (joined)
    assert "Requirements" in out and "keep clear space" in out["Requirements"].lower()

def test_extract_logo_safezone_first_match_only(monkeypatch):
    # Ensure it stops after first matched section (break)
    page1 = "\n".join([
        "foo",
        "the safe zone",
        "x is the cap height.",
        "",
        "new section"
    ])
    page2 = "\n".join([
        "the safe zone",
        "x is different here",
    ])
    _patch_fitz_open(monkeypatch, [page1, page2])
    out = extract_logo_safezone_styles(b"...")
    assert "different" not in str(out).lower()

def test_extract_logo_colours_picks_hash_lines_when_primary_present(monkeypatch):
    # NOTE: current code requires literal "primary" (case sensitive) to be in the page text
    text = "\n".join([
        "Brand colours (primary and secondary)",  # contains "primary"
        "#112233",
        "Body",
        "#AABBCC"
    ])
    _patch_fitz_open(monkeypatch, [text])
    out = extract_logo_colours(b"...")
    assert out == {"Logo colours": ["#112233", "#AABBCC"]}

def test_extract_logo_colours_skips_when_primary_absent(monkeypatch):
    # Because of "if 'primary' in text:" (case sensitive), no colours extracted
    text = "\n".join(["Brand colours", "#112233", "#AABBCC"])
    _patch_fitz_open(monkeypatch, [text])
    out = extract_logo_colours(b"...")
    assert out == {"Logo colours": []}

def test_extract_palette_styles_collects_all_hash_lines(monkeypatch):
    text1 = "\n".join(["Intro", "#000000"])
    text2 = "\n".join(["#FFFFFF", "Footer"])
    _patch_fitz_open(monkeypatch, [text1, text2])
    out = extract_palette_styles(b"...")
    assert out == {"Colours": ["#000000", "#FFFFFF"]}

def test_extract_brand_compliance_composes_all(monkeypatch):
    # Compose a single fake page that hits all extractors
    page = "\n".join([
        "Primary", "Roboto",
        "Secondary", "Inter",
        "The safe zone", "X is cap height.", "Keep clear.",
        "primary palette below", "#112233",
        "#445566"
    ])
    _patch_fitz_open(monkeypatch, [page])

    out = extract_brand_compliance(b"...")
    # structure
    assert set(out.keys()) == {
        "font_styles", "logo_safezone", "logo_colour", "logo_colour_palette"
    }
    # spot check values
    assert out["font_styles"].get("Primary") == "Roboto"
    assert "#112233" in out["logo_colour"]["Logo colours"]
    assert "#445566" in out["logo_colour_palette"]["Colours"]
