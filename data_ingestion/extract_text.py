import PyPDF2
import pytesseract
import cv2
import os
from PIL import Image

# Function to extract text from a regular PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to extract text from a scanned PDF using OCR
def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    text = pytesseract.image_to_string(gray)  # Apply OCR
    return text

# Main function to process PDFs
def extract_text(pdf_path, is_scanned=False):
    if is_scanned:
        return extract_text_from_image(pdf_path)
    else:
        return extract_text_from_pdf(pdf_path)

# Example usage with your resume
if __name__ == "__main__":
    pdf_file = "data/Kushal_Resume.pdf"  # Update this to the actual filename
    text = extract_text(pdf_file, is_scanned=False)  # Set to True if it's a scanned PDF
    print(text)
