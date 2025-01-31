# extract_text.py 0.1

import pytesseract
from PIL import Image
import argparse
import logging
import sys
import os


def setup_logging():
    logging.basicConfig(level=logging.INFO, filename='app.log',
                        format='%(asctime)s %(levelname)s:%(message)s')


def extract_text(image_path, output_path):
    try:
        # If Tesseract is not in your PATH, specify the full path
        # Uncomment and modify the following line if necessary
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        # Save the extracted text
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text.strip())
        logging.info(f"Extracted text saved to {output_path}")
        print(f"Extracted text saved to {output_path}")
        return True
    except Exception as e:
        logging.exception("Error extracting text:")
        print(f"Error extracting text: {e}", file=sys.stderr)
        return False


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Extract text from an image using pytesseract.")
    parser.add_argument('--input', type=str, required=True, help='Path to the input image.')
    parser.add_argument('--output', type=str, default='extracted_text.txt', help='Path to save the extracted text.')

    args = parser.parse_args()

    # Check if the image file exists
    if not os.path.isfile(args.input):
        logging.error(f"Input file {args.input} does not exist.")
        print(f"Input file {args.input} does not exist.", file=sys.stderr)
        sys.exit(1)

    success = extract_text(args.input, args.output)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
