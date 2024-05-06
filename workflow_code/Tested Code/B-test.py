import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# This code copies the text from photo and paste it in the console.
# Open an image file
img = Image.open(r'C:\Users\MrGChene\dev_work\Guernsey French Digital Record\Test Materials\Sarnia_cherie_gf.png')

# Use Tesseract to do OCR on the image
text = pytesseract.image_to_string(img)

# Print the text
print('Success!')
