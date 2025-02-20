import os
import spacy
import re
import logging

# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")

# ✅ Ensure correct base directory (Move up two levels to project root)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
log_dir = os.path.join(base_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "preprocess_text.log")

logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ✅ Use absolute paths based on `base_dir`
data_dir = os.path.join(base_dir, "data")
input_file = os.path.join(data_dir, "Kushal_Resume.pdf.txt")
output_file = os.path.join(data_dir, "Kushal_Resume_preprocessed.txt")

logger.info(f"Processing text from: {input_file}")

def clean_text(text):
    """Removes unwanted characters, symbols, and extra spaces while keeping periods, commas, exclamation marks, and question marks."""
    text = re.sub(r"([!?])\1+", r"\1", text)  # Replace multiple ! or ? with a single one
    text = re.sub(r"[^\w\s.,!?]", "", text)  # Remove everything except letters, numbers, spaces, ., , !, ?
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

def preprocess_text(text):
    """Tokenizes text, removes stopwords, and lemmatizes words."""
    doc = nlp(text.lower())  # Convert to lowercase
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

if __name__ == "__main__":
    if not os.path.exists(input_file):
        logger.error(f"❌ Error: {input_file} not found! Run extract_text.py first!")
        print(f"❌ Error: {input_file} not found! Run extract_text.py first!")
        exit(1)

    with open(input_file, "r") as file:
        raw_text = file.read()

    if not raw_text.strip():
        logger.warning("⚠️ Warning: Input text file is empty.")
        print("⚠️ Warning: Input text file is empty.")
        exit(1)

    cleaned_text = clean_text(raw_text)
    processed_text = preprocess_text(cleaned_text)

    with open(output_file, "w") as output:
        output.write(processed_text)

    logger.info(f"✅ Preprocessed text saved to {output_file}")
    print(f"✅ Preprocessed text saved to {output_file}")
