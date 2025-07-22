import logging
import PyPDF2
from transformers import pipeline
import json

# Logging to file and console
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pipeline.log'),
            logging.StreamHandler()
        ]
)

# Init your classifier

classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')

def extract_text(pdf_path):
    """Extracting and logging text from a PDF."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''.join(page.extract_text() or '' for page in reader.pages)
            logging.info(f"Extracted text from {pdf_path}, length: {len(text)} chars")
            if not text.strip():
                logging.warning(f"Empty text extract from {pdf_path}")
            # Option to log first 100 (or XXXX) chars of input PDF text
            logging.info(f"Input text sample (first 100 chars): {text[:100]}")
            return text
        except Exception as e:
            logging.error(f"Failed to extract text from {pdf_path}: {str(e)}")
            raise
def classify_text(text, pdf_path):
    """Classify text and log predictions."""
    try:
        if not text.strip():
            logging.error(f"No valid text to classify for {pdf_path}")
            return None, None
        result = classifier(text, truncation=True, max_length=512)
        label = result[0]['label']
        # Log prediction details
        logging.info(f"Classification for {pdf_path}: label={label}, score={score:.4f}")
        # Log input text sample used for classification
        logging.debug(f"Classified text sample (first 100 chars): {text[:100]}")
        return label, score
    except Exception as e:
        logging.error(f"Classification failed for {pdf_path}: {str(e)}")
        raise

def process_pdf(pdf_path):
    """Process a single PDF."""
    try:
        text = extract_text(pdf_path)
        label, score = classify_text(text, pdf_path)
        return {"file": pdf_path, "label": label, "score": score}
    except Exception as e:
        logging.error(f"Processing failed for {pdf_path}: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    pdf_path = "sample.pdf"
    result = process_pdf(pdf_path)
    if result:
        logging.info(f"Processed {pdf_path}: {json.dumps(result)}")
