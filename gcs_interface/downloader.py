import os
from google.cloud import storage
import json

def get_recent_data():
    bucket_name = os.getenv("GCS_BUCKET")
    prefix = "market/crypto/"
    blobs = list_files_in_bucket(bucket_name = bucket_name, prefix=prefix)
    latest_blob = blobs[-1]

    # Finally storing and sending the data from the file
    return download_file_data(bucket_name = bucket_name, filepath = latest_blob.name)

def download_file_data(bucket_name, filepath):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob_file = bucket.blob(filepath)
    if blob_file.exists(client):
        content = json.loads(blob_file.download_as_text())
        return content
    else:
        return {}

def list_files_in_bucket(bucket_name = os.getenv("GCS_BUCKET"), prefix = None):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix)
    blobs = sorted(blobs, key=lambda b: b.name) 
    return blobs