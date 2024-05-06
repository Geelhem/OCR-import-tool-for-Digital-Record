import subprocess
import sys
import importlib.util
import platform
import logging
import requests
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Function to prompt the user for confirmation
def confirm_installation(message):
    response = input(message + " (yes/no): ").lower()
    return response == 'yes'

# Function to install a Python module
def install_module(module_name):
    if confirm_installation(f"Do you want to install the '{module_name}' module?"):
        subprocess.run([sys.executable, "-m", "pip", "install", module_name], check=True)
        logging.info(f"Module '{module_name}' has been installed.")
    else:
        logging.info(f"Module '{module_name}' installation skipped by user.")

# Function to install Tesseract OCR
def install_tesseract():
    operating_system = platform.system()
    if operating_system == "Darwin":  # macOS
        tesseract_cmd = '/opt/homebrew/bin/tesseract'  # Set the correct path for Homebrew-installed Tesseract
        try:
            subprocess.run([tesseract_cmd, "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            logging.info("Tesseract OCR is installed.")
        except subprocess.CalledProcessError:
            if confirm_installation("Tesseract OCR is NOT installed. Do you want to install it using Homebrew?"):
                subprocess.run(["brew", "install", "tesseract"], check=True)
                logging.info("Tesseract OCR has been installed.")
            else:
                logging.info("Tesseract OCR installation skipped by user.")
    else:
        logging.error("Automatic installation of Tesseract OCR is not supported on this operating system.")

        # Add Tesseract path to system PATH
        tesseract_path = '/opt/homebrew/bin'  # Adjust this path as needed
        os.environ["PATH"] += os.pathsep + tesseract_path
        logging.info(f"Tesseract path added to system PATH: {tesseract_path}")

# Function to download the latest Tika server jar
def download_tika_server():
    if confirm_installation("Do you want to download the latest Tika server jar?"):
        tika_server_url = "https://www.apache.org/dyn/closer.cgi/tika/tika-server-1.24.1.jar"
        response = requests.get(tika_server_url, stream=True)
        with open("tika-server.jar", "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        logging.info("The latest Tika server jar has been downloaded.")
    else:
        logging.info("Tika server jar download skipped by user.")

# Function to check if a Python module is installed
def check_module_installed(module_name):
    if importlib.util.find_spec(module_name) is None:
        logging.error(f"Module '{module_name}' is NOT installed.")
        install_module(module_name)
    else:
        logging.info(f"Module '{module_name}' is installed.")

# Check for PIL (Pillow) module
check_module_installed('PIL')

# Check for tika module
check_module_installed('tika')

# Check if Tesseract is installed and add to system PATH
install_tesseract()

# Download the latest Tika server jar
download_tika_server()
