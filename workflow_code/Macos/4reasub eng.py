import os
from tika import parser as tika_parser
import pytesseract
from PIL import Image
import logging

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
    for entry in os.scandir(directory):
        if entry.is_file() and not entry.name.startswith('.'):
            file_path = entry.path
            logging.info(f"Processing file: {file_path}")

            # Check if the file is an image
            if is_image_file(entry.name):
                try:
                    # Open an image file using PIL
                    img = Image.open(file_path)
                    logging.info("Image file opened successfully")

                    # Check if the file name contains '_eng' before the file extension
                    if '_eng' in os.path.splitext(entry.name)[0]:
                        # Use Tesseract to do OCR on the image with English language
                        tesseract_text = pytesseract.image_to_string(img, lang='eng')
                        logging.info("OCR performed on image file with English language")
                    else:
                        # Use Tesseract to do OCR on the image without specifying language
                        tesseract_text = pytesseract.image_to_string(img)
                        logging.info("OCR performed on image file")

                    # Determine the base name of the image file and create a new text file name
                    text_file_name = os.path.splitext(entry.name)[0] + '.txt'

                    # Define the path for the new text file
                    text_file_path = os.path.join(directory, text_file_name)

                    # Write the text extracted by Tesseract to a file with the same base name as the image
                    with open(text_file_path, 'w', encoding='utf-8') as file:
                        file.write(tesseract_text)
                        logging.info(f"Text extracted by Tesseract written to: {text_file_path}")

                except IOError as e:
                    logging.error(f"Tesseract could not process file: {file_path}, error: {e}")
            else:
                # Use Tika to parse the file
                try:
                    parsed = tika_parser.from_file(file_path)
                    logging.info("File parsed using Tika")

                    # Extracted text is stored in 'content' key by Tika
                    tika_text = parsed.get('content', '')

                    # Determine the base name of the file and create a new text file name
                    text_file_name = os.path.splitext(entry.name)[0] + '.txt'

                    # Define the path for the new text file
                    text_file_path = os.path.join(directory, text_file_name)

                    # Check if Tika extracted any text and write to a file
                    if tika_text:
                        with open(text_file_path, 'w', encoding='utf-8') as file:
                            file.write(tika_text)
                            logging.info(f"Text extracted by Tika written to: {text_file_path}")
                    else:
                        logging.warning(f"No text extracted from file: {file_path}")
                except Exception as e:
                    logging.error(f"An error occurred while processing file: {file_path}, error: {e}")
        elif entry.is_dir():  # Recursively process subdirectories
            logging.info(f"Entering subdirectory: {entry.path}")
            process_files(entry.path)

# Prompt the user for the location of the directory
dir_path = input("Please enter the path to your directory: ")
logging.info(f"Directory path entered: {dir_path}")

# Start processing files
process_files(dir_path)

# Notify user of completion
logging.info("Finished processing all files.")

#This script will now treat any file with ‘_eng’ in its name as an English text file for OCR purposes. 
#It will process all files in the specified directory and its subdirectories, performing OCR on image files and using Tika to extract text from other document types.