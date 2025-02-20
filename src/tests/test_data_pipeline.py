import os
import pytest

from src.data_ingestion.extract_text import extract_text_from_pdf
from src.data_ingestion.preprocess_text import clean_text, preprocess_text

# Sample test files
TEST_PDF = "tests/sample.pdf"
TEST_TEXT = "tests/sample.txt"

@pytest.fixture
def sample_pdf():
    """Creates a sample PDF file for testing."""
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a test PDF.", ln=True, align="C")
    pdf.output(TEST_PDF)
    yield TEST_PDF
    os.remove(TEST_PDF)

@pytest.fixture
def sample_text():
    """Creates a sample text file for testing."""
    text = "This is a test sentence. Machine learning is great!"
    with open(TEST_TEXT, "w") as f:
        f.write(text)
    yield TEST_TEXT
    os.remove(TEST_TEXT)

def test_extract_text_from_pdf(sample_pdf):
    """Tests extracting text from a PDF."""
    extracted_text = extract_text_from_pdf(sample_pdf)
    assert "This is a test PDF" in extracted_text

def test_clean_text():
    """Tests cleaning text by removing unwanted characters."""
    raw_text = "Hello!!! This is a TEST.\nNew line here."
    cleaned = clean_text(raw_text)

    print(f"\n[DEBUG] Cleaned text: '{cleaned}'")  # Print output for debugging

    assert cleaned == "Hello! This is a TEST. New line here."  # Adjust expected output


def test_preprocess_text():
    """Tests tokenization, stopword removal, and lemmatization."""
    raw_text = "The quick brown foxes are jumping!"
    processed = preprocess_text(raw_text)
    assert processed == "quick brown fox jump"  # Expected lemmatized output
