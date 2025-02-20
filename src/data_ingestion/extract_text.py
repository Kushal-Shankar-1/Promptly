import os
import PyPDF2
import pytesseract
import cv2
import logging
from PIL import Image

# Setup logging
log_dir = os.path.abspath("logs/")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "extract_text.log")

logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Ensure correct absolute paths
base_dir = os.path.abspath(os.path.dirname(__file__))
pdf_file = os.path.join(base_dir, "../data/Kushal_Resume.pdf")  # Absolute path to PDF
output_text_file = os.path.join(base_dir, "../data/Kushal_Resume.pdf.txt")  # Output file

logger.info(f"Using PDF file: {pdf_file}")

# Function to extract text from a regular PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
    return text.strip()

# Function to extract text from a scanned PDF using OCR
def extract_text_from_image(image_path):
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        text = pytesseract.image_to_string(gray)  # Apply OCR
        return text.strip()
    except Exception as e:
        logger.error(f"Failed to extract text from scanned image: {e}")
        return ""

# Main function to process PDFs
def extract_text(pdf_path, is_scanned=False):
    if is_scanned:
        return extract_text_from_image(pdf_path)
    else:
        return extract_text_from_pdf(pdf_path)

if __name__ == "__main__":
    if not os.path.exists(pdf_file):
        logger.error(f"Error: File {pdf_file} not found! Exiting...")
        exit(1)

    text = extract_text(pdf_file, is_scanned=False)

    if text:
        with open(output_text_file, "w") as txt_file:
            txt_file.write(text)
        logger.info(f"Extracted text saved to {output_text_file}")
    else:
        logger.warning("No text extracted from the PDF.")
