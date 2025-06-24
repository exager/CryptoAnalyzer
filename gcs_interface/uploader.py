from google.cloud import storage
from gcs_interface.downloader import list_files_in_bucket

def upload_data(bucket_name: str, source_data, destination_blob_name):
    """Uploads the crypto json file to the bucket."""
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(source_data,content_type='application/json')

    return f"File has been uploaded to {destination_blob_name}."
