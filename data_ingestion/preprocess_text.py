import spacy
import re

# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")

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

# Example usage
if __name__ == "__main__":
    input_file = "data/Kushal_Resume.pdf.txt"

    try:
        with open(input_file, "r") as file:
            raw_text = file.read()
        
        cleaned_text = clean_text(raw_text)
        processed_text = preprocess_text(cleaned_text)

        # Save processed text to a new file
        with open("data/Kushal_Resume_preprocessed.txt", "w") as output_file:
            output_file.write(processed_text)

        print("Preprocessed text saved to data/Kushal_Resume_preprocessed.txt")
    
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Run extract_text.py first!")
