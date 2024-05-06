from tika import parser
import os

def read_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):  # Adjust the file extension as needed
            file_path = os.path.join(directory_path, filename)
            parsed_content = parser.from_file(file_path)
            text_content = parsed_content["content"]
            # Process the text content as needed (e.g., write to a file)

if __name__ == "__main__":
    directory_to_read = r"C:\Users\MrGChene\Downloads\Additional info Lauren and Chloe Peterson"
    read_directory(directory_to_read)
