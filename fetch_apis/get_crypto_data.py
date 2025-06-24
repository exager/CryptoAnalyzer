import requests
from utils.time_utils import get_current_date, get_current_time
from io import StringIO
import pandas as pd

def fetch_crypto_data(url, hdr):
    
    response = requests.get(url, headers=hdr)
    df = pd.DataFrame(response.json())

    df['recorded_time'] = str(get_current_date()) + "T" + str(get_current_time())
    cleaned_data = df.to_json(orient='records',indent = 4)
    return cleaned_data