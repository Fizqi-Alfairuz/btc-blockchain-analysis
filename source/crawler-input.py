import os
import requests
import pandas as pd
from urllib.parse import urlparse
from pathlib import Path

# Define file paths
csv_file = r"inputs_url_20250101-20250228.csv"  # Change this to the actual path of your CSV file
download_dir = r"D:\Kamsiber\Bitcoin Blockchain Analytics\Database\input"  # Change this to your desired download directory

# Ensure the download directory exists
Path(download_dir).mkdir(parents=True, exist_ok=True)

# Read the CSV file
df = pd.read_csv(csv_file, sep=";", header=None)  # Assuming URLs are separated by ";"
urls = df.values.flatten()  # Convert DataFrame to a list

# Function to download a file
def download_file(url, folder):
    try:
        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_file"  # Fallback if no filename in URL

        file_path = os.path.join(folder, filename)
        temp_file_path = file_path + ".part"  # Temporary file to prevent partial downloads being marked as complete

        # Check if file already exists
        if os.path.exists(file_path):
            print(f"File already exists: {filename}, skipping download.")
            return

        # Download the file in chunks
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes

        # Write to a temporary file
        with open(temp_file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # Rename temp file to final filename upon successful download
        os.rename(temp_file_path, file_path)
        print(f"Downloaded: {filename}")

    except Exception as e:
        print(f"Failed to download {url}: {e}")
        # Ensure incomplete files are deleted
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Removed incomplete file: {temp_file_path}")

# Download each file
for url in urls:
    if isinstance(url, str) and url.strip():  # Ensure it's a valid URL
        download_file(url.strip(), download_dir)

print("All downloads complete!")
