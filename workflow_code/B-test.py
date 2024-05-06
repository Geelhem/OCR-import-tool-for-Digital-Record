import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Open an image file
img = Image.open(r'C:\Users\MrGChene\dev_work\OCR\Sarnia_cherie_gf.jpg')

# Use Tesseract to do OCR on the image
text = pytesseract.image_to_string(img)

# Print the text
print('Success!')
