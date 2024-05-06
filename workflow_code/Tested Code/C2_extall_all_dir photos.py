from tika import parser
import pytesseract
from PIL import Image
import os
#This Python script performs Optical Character Recognition (OCR) on a directory of image files containing text. It uses both Tika and Tesseract OCR engines to extract text from images, creating corresponding text files for each image.
#The extracted content is then stored in these text files, facilitating digitization, archival, and searchability of textual information within the images.
# Set the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define the path to your directory
dir_path = r'C:\Users\MrGChene\dev_work\Guernsey French Digital Record\Test Materials\histouaires guernésiaises'

# Check if the directory exists
if not os.path.isdir(dir_path):
    print(f"The directory {dir_path} does not exist.")
    exit()

# Iterate over all files in the directory
for filename in os.listdir(dir_path):
    image_path = os.path.join(dir_path, filename)

    # Skip directories and non-image files
    if os.path.isdir(image_path) or not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        continue

    try:
        # Use Tika to parse the file
        parsed = parser.from_file(image_path)

        # Extracted text is stored in 'content' key by Tika
        tika_text = parsed.get('content', '')

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
        print(f'Permission error: {e}. Please check the permissions for the file: {image_path}')
    except IOError as e:
        print(f'IOError: {e}. Tesseract could not process file: {image_path}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

# Optionally, you can also write the text extracted by Tika to a different file or compare it with Tesseract's output
