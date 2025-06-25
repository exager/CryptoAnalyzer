import os
from utils.list_coins import load_coin_list
from utils.time_utils import get_current_date, get_current_time
from fetch_apis.get_crypto_data import fetch_crypto_data
from gcs_interface.uploader import upload_data
from gcs_interface.manage_crypto import run_coin_history

def run(gcs_bucket: str = os.getenv("GCS_BUCKET")):
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
    print(uploader_msg)
    if get_current_time()[:5] == '00-00':
        run_coin_history(gcs_bucket)
