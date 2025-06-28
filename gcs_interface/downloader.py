import os
from google.cloud import storage
from utils.logger import logger
import json

def get_recent_data():
    bucket_name = os.getenv("GCS_BUCKET")
    prefix = "market/crypto/"
    blobs = list_files_in_bucket(bucket_name = bucket_name, prefix=prefix)
    latest_blob = blobs[-1]
    logger.info(f'Found the data file {latest_blob.name}, sending to download...')
    # Finally storing and sending the data from the file
    return download_file_data(bucket_name = bucket_name, filepath = latest_blob.name)

def coin_data(coin: str):
    bucket_name = os.getenv("GCS_BUCKET")
    filepath = f"market/currency/{coin}.json"
    return download_file_data(bucket_name = bucket_name, filepath = filepath)

def download_file_data(bucket_name, filepath):
    logger.info(f'Download path triggered for {filepath}.')
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    logger.info(f'Connected to GCS Bucket {bucket_name}.')
    blob_file = bucket.blob(filepath)
    if blob_file.exists(client):
        content = json.loads(blob_file.download_as_text())
        logger.info(f'Downloaded file sent as JSON file...')
        return content
    else:
        logger.info(f'No file present for {filepath}. Sending an empty JSON...')
        return []

def list_files_in_bucket(bucket_name = os.getenv("GCS_BUCKET"), prefix = None):
    logger.info(f'Finding the list of files present for the Path prefix {prefix}...')
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix)
    blobs = sorted(blobs, key=lambda b: b.name) 
    logger.info(f'Found {sum(1 for blob in blobs)} files...')
    return blobs