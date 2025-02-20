import PyPDF2
import pytesseract
import cv2
import os
from PIL import Image

# Ensure correct absolute paths
base_dir = os.path.abspath(os.path.dirname(__file__))  # Get the directory of this script
pdf_file = os.path.join(base_dir, "../data/Kushal_Resume.pdf")  # Absolute path to PDF
output_text_file = os.path.join(base_dir, "../data/Kushal_Resume.pdf.txt")  # Output file

print(f"Using PDF file: {pdf_file}")

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

if __name__ == "__main__":
    if not os.path.exists(pdf_file):
        print(f"Error: File {pdf_file} not found! Exiting...")
        exit(1)

    text = extract_text(pdf_file, is_scanned=False)

    # Save the extracted text to a file
    with open(output_text_file, "w") as txt_file:
        txt_file.write(text)

    print(f"Extracted text saved to {output_text_file}")
