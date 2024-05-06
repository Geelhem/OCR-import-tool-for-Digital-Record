from tika import parser
import pytesseract
from PIL import Image
import os
from pdf2image import convert_from_path

# Set the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define the path to your directory
dir_path = r'C:\Users\MrGChene\dev_work\OCR\content'

# Iterate over all files in the directory
for filename in os.listdir(dir_path):
    file_path = os.path.join(dir_path, filename)

    # Check if the path is a file
    if os.path.isfile(file_path):
        # Use Tika to parse the file
        parsed = parser.from_file(file_path)

        # Extracted text is stored in 'content' key by Tika
        tika_text = parsed['content']

        # Check if the file is a PDF
        if file_path.lower().endswith('.pdf'):
            # Convert the PDF to a list of images
            images = convert_from_path(file_path)
            for i, img in enumerate(images):
                try:
                    # Use Tesseract to do OCR on the image
                    tesseract_text = pytesseract.image_to_string(img)

                    # Determine the base name of the image file and create a new text file name
                    base_name = os.path.basename(file_path)
                    text_file_name = os.path.splitext(base_name)[0] + f'_page{i}.txt'

                    # Define the path for the new text file
                    text_file_path = os.path.join(os.path.dirname(file_path), text_file_name)

                    # Write the text extracted by Tesseract to a file with the same base name as the image
                    with open(text_file_path, 'w', encoding='utf-8') as file:
                        file.write(tesseract_text)

                    # Print the location and content from Tesseract to the console
                    print(f'The text extracted by Tesseract has been written to: {text_file_path}')
                    print('The content extracted by Tesseract is:')
                    print(tesseract_text)
                except IOError:
                    print(f'Tesseract could not process page {i} of file: {file_path}')
        else:
            print(f'Skipped non-PDF file: {file_path}')
    else:
        print(f'Skipped directory: {file_path}')
