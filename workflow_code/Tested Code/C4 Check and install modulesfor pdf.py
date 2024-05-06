import os
import subprocess
import sys
import urllib.request
import zipfile
from pdf2image import convert_from_path

# Function to check if a module is installed, and install it if it's not
def install_module(module_name):
    try:
        __import__(module_name)
        print(f"Module '{module_name}' is already installed.")
    except ImportError:
        print(f"Module '{module_name}' is not installed. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name])

# Check and install required modules
install_module('tika')
install_module('pytesseract')
install_module('Pillow')  # PIL is now under the name Pillow
install_module('pdf2image')

# Function to check if poppler is installed and in PATH
def is_poppler_installed():
    try:
        subprocess.Popen(["pdfinfo"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

# Function to install poppler
def install_poppler():
    print("Poppler is not installed. Installing...")
    poppler_url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v21.11.0-0/Release-21.11.0-0.zip"
    poppler_zip = "poppler.zip"

    # Download poppler
    urllib.request.urlretrieve(poppler_url, poppler_zip)

    # Extract poppler
    with zipfile.ZipFile(poppler_zip, 'r') as zip_ref:
        zip_ref.extractall("poppler")

    # Clean up the zip file
    os.remove(poppler_zip)

    # Add poppler to PATH
    poppler_bin = os.path.abspath(os.path.join("poppler", "bin"))
    os.environ["PATH"] += os.pathsep + poppler_bin

    print(f"Poppler installed to {poppler_bin} and added to PATH.")
    return poppler_bin

# Check if poppler is installed and in PATH
poppler_path = ''
if not is_poppler_installed():
    poppler_path = install_poppler()
else:
    print("Poppler is installed and found in PATH.")
    poppler_path = os.path.join(os.environ['PROGRAMFILES'], 'poppler', 'bin')

# Rest of your code...
# When calling convert_from_path, use the poppler_path variable
# images = convert_from_path(file_path, poppler_path=poppler_path)
