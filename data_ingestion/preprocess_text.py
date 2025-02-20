import os
import spacy
import re

# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Ensure absolute paths
base_dir = os.path.abspath(os.path.dirname(__file__))  # Get script directory
input_file = os.path.join(base_dir, "../data/Kushal_Resume.pdf.txt")
output_file = os.path.join(base_dir, "../data/Kushal_Resume_preprocessed.txt")

print(f"Processing text from: {input_file}")

def clean_text(text):
    """Removes unwanted characters, symbols, and extra spaces."""
    text = re.sub(r"\n+", " ", text)  # Remove multiple newlines
    text = re.sub(r"[^a-zA-Z0-9.,!? ]", "", text)  # Keep only text and punctuation
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

def preprocess_text(text):
    """Tokenizes text, removes stopwords, and lemmatizes words."""
    doc = nlp(text.lower())  # Convert to lowercase
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

if __name__ == "__main__":
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found! Run extract_text.py first!")
        exit(1)

    with open(input_file, "r") as file:
        raw_text = file.read()

    cleaned_text = clean_text(raw_text)
    processed_text = preprocess_text(cleaned_text)

    # Save processed text to a new file
    with open(output_file, "w") as output:
        output.write(processed_text)

    print(f"Preprocessed text saved to {output_file}")
