import tika
import requests
from tika import parser

import warnings
warnings.filterwarnings('ignore')

# Start running the tika service
tika.initVM()

from tika import parser
try:
    # Attempt to parse a dummy file (you can replace with an actual file path)
    parsed_content = parser.from_file('"C:\Users\MrGChene\OneDrive - The Ladies'College\Additional info Lauren and Chloe Peterson\ILP French Lauren Peterson.pdf"', serverEndpoint='http://localhost:9998/tika')
    print("Tika server is running and accessible.")
except Exception as e:
    print(f"Error: {e}")
    print("Tika server is not running or not accessible.")
