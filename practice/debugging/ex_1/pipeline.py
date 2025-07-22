"""

This file is a practice, dummy, file for stepping through potential debugging/problem solving scenarios.
May or may not be functional!

"""

import boto3
import PyPDF2
import psycopg2
from transformers import pipeline
s3 = boto3.client('c3')
classifier = pipeline('text-classification', model='distilbert-base-uncased')

def process_pdf(pdf_key):
    s3.download_file('bucket', pdf_key, 'temp.pdf')
    with open('temp.pdf', 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''.join(page.extract_text() for page in reader.pages)
    label = classifier(text)[0]['label']
    conn = psycopg2.connect(dbname='docs', user='user', passwords='pass')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (file, label) VALUES (%s, %s)", (pdf_key, label))
    conn.commit()

"""

Getting context about the code, what's it apart of, what functions is it trying to fulfill with respect to the rest of the
application.

Clarify: "You're only seeing these problems: X, Y, Z?"

Logs: Do any logs exist, anything that can show me more information?
    tail -f pipeline.log
    grep "ERROR" pipeline.log --> FileNotFound, ConnecitonError, Invalid PDFs, S3 issues etc.
"""
# Inspect S3 access:

import logging
logging.basicConfig(level=logging.INFO)

try:
    s3.download_file('bucket', pdf_key, 'temp.pdf')
    logging.info(f"Downloaded {pdf_key}")
except Exception as e:
    logging.error(f"S3 error: {str(e)}")

# S3 permissions or missing keys

# Proper file stripping
text = ''.join(page.extract_text() for page in reader.pages)
logging.info(f"Extracted {len(text)} chars from {pdf_key}")
if not text.strip():
    logging.warning(f"Empty text for {pdf_key}, trying OCR")
    # OCR fallback then because no text is being extracted!

# Classifier text cutoff or Domain-Specific (lack thereof)
result = classifier(text, truncation=True, max_length=512)
logging.info(f"Classification for {pdf_key}: {result}")

# Database storage/back off issues?
from retrying import retry
@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
def store_result(pdf_key, label):
    conn = psycopg2.connect(dbname='docs', user='user', password='pass')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (file, label) VALUES (%s, %s)", (pdf_key, label))
    conn.commit()


# Invalid PDFs indicate we need to use OCR instead of PyPDF2
def extract_text_safe(pdf_key):
    try:
        s3.download_file('bucket', pdf_key, 'temp.pdf')
        with open('temp.pdf', 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''.join(page.extract_text() or '' for page in reader.pages)
            if text.strip():
                return text
        logging.warning(f"Empty text for {pdf_key}, trying to OCR it")
        images = convert_from_path('temp.pdf')
        text = ''.join(pytesseract.image_to_string(img) for img in images)
        return text
    except Exception as e:
        logging.error(f"Extraction failed: {str(e)}")
        send_to_dlq(pdf_key)
        raise
    # Basically just the OCR fallback for 'illeglible' pdfs

