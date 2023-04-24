from datetime import date
from google.cloud import storage
import os.path
from get_time_data import year, quarter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials/dstreportdata-48acf2cbeed0.json"

def get_file_list(year, quarter):
    client = storage.Client()
    blobs = list(client.list_blobs(bucket_or_name="dst_datalake", prefix=f"report_data/{year}"))
    q_list = []
    for blob in blobs:
        if not blob.name.endswith('/'):
            item_quarter = (int(blob.name[22:24]) - 1) // 3 + 1
            if item_quarter == quarter:
                q_list.append(blob.name)
    return q_list


# Initialise a client
storage_client = storage.Client()
# Create a bucket object for our bucket
bucket = storage_client.get_bucket("dst_datalake")

directory = f"data/q{quarter}/"
if not os.path.exists(directory):
    os.makedirs(directory)

for item in get_file_list(year, quarter):
    # Create a blob object from the filepath
    blob = bucket.blob(f"{item}")
    # Download the file to a destination
    blob.download_to_filename(f"{directory}{item[17:]}")