from google.cloud import storage
from utils.list_coins import load_coin_list
from gcs_interface.downloader import list_files_in_bucket, download_file_data
from gcs_interface.uploader import upload_data
from utils.time_utils import get_previous_date
import json

def run_coin_history(bucket_name: str):
    coins = load_coin_list().split(',')
    for coin in coins:
        search_term = 'market/currency/' + coin + '.json'
        data = download_file_data(bucket_name, search_term)

        if len(data) == 0:
            create_coin_data(bucket_name, coin, destination = search_term)
        
        else:
            last_day_path = 'market/crypto/' + get_previous_date() + '/'
            files = list_files_in_bucket(bucket_name = bucket_name, prefix = last_day_path)
            files_to_append = files[-24:]
            for blob in files_to_append:
                data.append(get_coin_data_from_file(bucket_name, coin, blob))
            
            upload_data(bucket_name = bucket_name, source_data = data, destination_blob_name = search_term)

def create_coin_data(bucket_name: str, coin_symbol, destination):
    market_data_address = 'market/crypto/'
    blobs = list_files_in_bucket(bucket_name = bucket_name, prefix = market_data_address)
    data_for_coin = []
    for blob in blobs:
        content = download_file_data(bucket_name, blob.name)
        data_for_coin.append(get_coin_data_from_file(bucket_name, coin_symbol, blob))
    
    # Now that we have the data, just upload it whole
    upload_data(bucket_name = bucket_name, source_data = data_for_coin, destination_blob_name = destination)

def get_coin_data_from_file(bucket_name: str, coin_symbol: str, blob_file: str):
    file_content = download_file_data(bucket_name = bucket_name, filepath = blob_file.name)
    for crypto_data in file_content:
            if crypto_data['symbol'] == coin_symbol:
                timestamp_data = {
                    'symbol': crypto_data['symbol'],
                    'name': crypto_data['name'],
                    'price': crypto_data['current_price'],
                    'market_cap': crypto_data['market_cap'],
                    'rank': crypto_data['market_cap_rank'],
                    'volume': crypto_data['total_volume'],
                    'price_change_24h': crypto_data['price_change_24h'],
                    'price_change_percentage_24h': crypto_data['price_change_percentage_24h'],
                    'record_date': crypto_data['recorded_time'].split('T')[0],
                    'record_time': crypto_data['recorded_time'].split('T')[1][:5].replace('-',':')
                }
                return timestamp_data
    return {}