from tika import parser
import pytesseract
from PIL import Image

# Set the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define the path to your image
image_path = r'C:\Users\MrGChene\dev_work\Guernsey French Digital Record\Test Materials\Sarnia_cherie_gf.png'

# Use Tika to parse the image file
parsed = parser.from_file(image_path)

# Extracted text is stored in 'content' key
text = parsed.get('content', '')

# Check if text is None or empty
if text:
    print('Text found:', text)
    # Write the text to a file
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(text)
else:
    print('No text could be extracted from the image.')

print('done')
