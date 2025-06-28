import requests
from utils.time_utils import get_current_date, get_current_time
from io import StringIO
import pandas as pd
from utils.logger import logger

def fetch_crypto_data(url, hdr):
    logger.info(f'Triggered Data Fetching from the CoinGecko API at {get_current_time()}, {get_current_date()}...')
    response = requests.get(url, headers=hdr)
    df = pd.DataFrame(response.json())

    df['recorded_time'] = str(get_current_date()) + "T" + str(get_current_time())
    cleaned_data = df.to_json(orient='records',indent = 4)
    logger.info("Sending the json file for required data")
    return cleaned_data