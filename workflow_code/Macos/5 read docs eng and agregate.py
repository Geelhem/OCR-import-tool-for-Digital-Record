import os
from tika import parser as tika_parser
import pytesseract
from PIL import Image
import logging
from collections import defaultdict
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Set the Tesseract command path for Windows and MacOS
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:  # MacOS (and other Unix-based OS)
    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Function to determine if a file is an image based on its extension
def is_image_file(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    return any(filename.lower().endswith(ext) for ext in image_extensions)

# Function to process files
def process_files(directory):
    # Dictionaries to hold file paths for aggregation
    gf_files = defaultdict(list)
    eng_files = defaultdict(list)

    # Regex to extract the base name and number from the file name
    name_pattern = re.compile(r'(.+?)(\d+)?(_gf|_eng)?(?=\.\w+$)', re.IGNORECASE)

    for entry in os.scandir(directory):
        if entry.is_file() and not entry.name.startswith('.'):
            file_path = entry.path
            logging.info(f"Processing file: {file_path}")

            # Extract base name, number, and suffix from file name
            match = name_pattern.match(entry.name)
            if match:
                base_name, number, suffix = match.groups()
                number = int(number) if number else 0  # Default to 0 if no number

                # Check if the file is an image
                if is_image_file(entry.name):
                    try:
                        # Open an image file using PIL
                        img = Image.open(file_path)
                        logging.info("Image file opened successfully")

                        # Use Tesseract to do OCR on the image
                        tesseract_text = pytesseract.image_to_string(img, lang='eng' if suffix == '_eng' else None)
                        logging.info(f"OCR performed on image file with suffix: {suffix}")

                        # Add the text and file number to the appropriate dictionary
                        if suffix == '_gf':
                            gf_files[base_name].append((number, tesseract_text))
                        elif suffix == '_eng':
                            eng_files[base_name].append((number, tesseract_text))

                    except IOError as e:
                        logging.error(f"Tesseract could not process file: {file_path}, error: {e}")
                else:
                    # Use Tika to parse the file
                    try:
                        parsed = tika_parser.from_file(file_path)
                        logging.info("File parsed using Tika")

                        # Extracted text is stored in 'content' key by Tika
                        tika_text = parsed.get('content', '')

                        # Add the text and file number to the appropriate dictionary
                        if suffix == '_gf':
                            gf_files[base_name].append((number, tika_text))
                        elif suffix == '_eng':
                            eng_files[base_name].append((number, tika_text))

                    except Exception as e:
                        logging.error(f"An error occurred while processing file: {file_path}, error: {e}")
        elif entry.is_dir():  # Recursively process subdirectories
            logging.info(f"Entering subdirectory: {entry.path}")
            process_files(entry.path)

    # Aggregate and write the contents to the respective files
    aggregate_contents(gf_files, directory, '_gf')
    aggregate_contents(eng_files, directory, '_eng')

def aggregate_contents(files_dict, directory, suffix):
    for base_name, texts in files_dict.items():
        # Sort the texts by their number
        sorted_texts = sorted(texts, key=lambda x: x[0])
        aggregated_text = ''.join(text[1] for text in sorted_texts)

        # Write the aggregated text to a file
        output_file_path = os.path.join(directory, f"{base_name}{suffix}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(aggregated_text)
            logging.info(f"Aggregated text written to: {output_file_path}")

# Prompt the user for the location of the directory
dir_path = input("Please enter the path to your directory: ")
logging.info(f"Directory path entered: {dir_path}")

# Start processing files
process_files(dir_path)

# Notify user of completion
logging.info("Finished processing all files.")
