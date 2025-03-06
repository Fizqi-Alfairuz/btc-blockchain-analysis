import csv
from datetime import datetime, timedelta

# Define the date range
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

# Define the file name
csv_filename = "blocks_url_20240101-20241231.csv"

# Open the CSV file for writing
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=';')

    
    # Generate the URLs
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d")
        url = f"https://gz.blockchair.com/bitcoin/blocks/blockchair_bitcoin_blocks_{date_str}.tsv.gz"
        writer.writerow([url])
        current_date += timedelta(days=1)

print(f"CSV file '{csv_filename}' has been generated successfully.")