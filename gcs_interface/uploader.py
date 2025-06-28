from google.cloud import storage
from gcs_interface.downloader import list_files_in_bucket
from utils.time_utils import get_current_time, get_current_date
from utils.logger import logger

def upload_data(bucket_name: str, source_data, destination_blob_name):
    """Uploads the crypto json file to the bucket."""
    logger.info(f'Data Upload triggered to store for {destination_blob_name} at {get_current_time()}, {get_current_date()}...')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(source_data,content_type='application/json')
    logger.info(f'Data Upload Succesful for {destination_blob_name}...')
    return f"File has been uploaded to {destination_blob_name}."
