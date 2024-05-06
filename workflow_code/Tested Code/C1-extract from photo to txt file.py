from tika import parser
import pytesseract
from PIL import Image
import os
#This Python script is designed to perform Optical Character Recognition (OCR) on an image file containing text. The script utilizes two different OCR libraries: Tika and Tesseract, to extract text from images. 
#Tika is used for parsing the image file and extracting any embedded text, while Tesseract, a more powerful OCR engine, is employed to analyze the image and convert any visible text into a string format.

# Set the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define the path to your image
image_path = r'C:\Users\MrGChene\dev_work\Guernsey French Digital Record\Test Materials\Sarnia_cherie_gf.png'

try:
    # Use Tika to parse the image file
    parsed = parser.from_file(image_path)

    # Extracted text is stored in 'content' key by Tika
    tika_text = parsed['content']

    # Open an image file using PIL
    img = Image.open(image_path)

    # Use Tesseract to do OCR on the image
    tesseract_text = pytesseract.image_to_string(img)

    # Determine the base name of the image file and create a new text file name
    base_name = os.path.basename(image_path)
    text_file_name = os.path.splitext(base_name)[0] + '.txt'

    # Define the path for the new text file
    text_file_path = os.path.join(os.path.dirname(image_path), text_file_name)

    # Write the text extracted by Tesseract to a file with the same base name as the image
    with open(text_file_path, 'w', encoding='utf-8') as file:
        file.write(tesseract_text)

    # Print the location and content from Tesseract to the console
    print(f'The text extracted by Tesseract has been written to: {text_file_path}')
    print('The content extracted by Tesseract is:')
    print(tesseract_text)

except PermissionError as e:
    print(f'Permission error: {e}')
    print('Please check that you have the necessary permissions and that the file is not open in another program.')
except Exception as e:
    print(f'An error occurred: {e}')

# Optionally, you can also write the text extracted by Tika to a different file or compare it with Tesseract's output
