import os
import requests
import pandas as pd
from urllib.parse import urlparse
from pathlib import Path

# Define file paths
csv_file = r"blocks_url_20240101-20241231.csv"  # Change this to the actual path of your CSV file
download_dir = r"D:\Kamsiber\Bitcoin Blockchain Analytics\Database\block"  # Change this to your desired download directory

# Ensure the download directory exists
Path(download_dir).mkdir(parents=True, exist_ok=True)

# Read the CSV file
df = pd.read_csv(csv_file, sep=";", header=None)  # Assuming URLs are separated by ";"
urls = df.values.flatten()  # Convert DataFrame to a list

# Function to download a file
def download_file(url, folder):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes
        
        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_file"  # Fallback if no filename in URL

        file_path = os.path.join(folder, filename)
        
        # Save the file
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Download each file
for url in urls:
    if isinstance(url, str) and url.strip():  # Ensure it's a valid URL
        download_file(url.strip(), download_dir)

print("All downloads complete!")