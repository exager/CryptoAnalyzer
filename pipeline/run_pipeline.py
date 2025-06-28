import os
from utils.list_coins import load_coin_list
from utils.time_utils import get_current_date, get_current_time
from fetch_apis.get_crypto_data import fetch_crypto_data
from gcs_interface.uploader import upload_data
from gcs_interface.downloader import list_files_in_bucket
from gcs_interface.manage_crypto import run_coin_history
from utils.logger import logger

def run_hourly_updates(gcs_bucket: str = os.getenv("GCS_BUCKET")):
    file_name = f'market/crypto/{ get_current_date() }/T{ get_current_time()[:2]}'
    if len(list_files_in_bucket(gcs_bucket, file_name)) > 0:
        return "File is already present, no need to re-upload"
    coins = load_coin_list()
    coins = coins.replace(',','%2C')
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd" + "&symbols=" + coins + "&order=market_cap_desc"

    header_data = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.getenv("CRYPTO_API_KEY")
    }

    market_data = fetch_crypto_data(url, header_data)

    # UPLOAD
    dest_file_location = 'market/crypto/' + str(get_current_date()) + '/T' + str(get_current_time()) + '.json'
    uploader_msg = upload_data(os.getenv("GCS_BUCKET"), market_data, dest_file_location)
    return uploader_msg

def get_daily_currency_data(gcs_bucket: str = os.getenv("GCS_BUCKET")):
    if get_current_time()[:2] == '23':
        run_coin_history(gcs_bucket)
        logger.info(f'Updating the data for currency files for {get_current_date()}, {get_current_time()}')
        return "Uploaded into the bins"
    return "Not the time"
