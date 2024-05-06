import os
import requests
from tika import parser

def download_tika_server_jar(version="1.18"):
    # Specify the Tika server download URL
    tika_server_url = f"https://archive.apache.org/dist/tika/tika-server-{version}/tika-server-{version}.jar"
    
    # Set the local path where the JAR file will be saved
    local_jar_path = os.path.join(os.getcwd(), f"tika-server-{version}.jar")
    
    # Download the Tika server JAR file
    response = requests.get(tika_server_url)
    with open(local_jar_path, "wb") as jar_file:
        jar_file.write(response.content)
    
    return local_jar_path

def read_directory(directory_path):
    # Download Tika server JAR (if not already downloaded)
    tika_server_jar_path = download_tika_server_jar()
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):  # Adjust the file extension as needed
            file_path = os.path.join(directory_path, filename)
            parsed_content = parser.from_file(file_path, serverEndpoint=f"http://localhost:9998/tika")
            text_content = parsed_content["content"]
            # Process the text content as needed (e.g., write to a file)

if __name__ == "__main__":
    directory_to_read = r"C:\Users\MrGChene\Downloads\Additional info Lauren and Chloe Peterson"
    read_directory(directory_to_read)
