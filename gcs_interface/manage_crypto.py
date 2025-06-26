from google.cloud import storage
from utils.list_coins import load_coin_list
from gcs_interface.downloader import list_files_in_bucket, download_file_data
from gcs_interface.uploader import upload_data
from utils.time_utils import get_previous_date
import json

def run_coin_history(bucket_name: str):
    coins = load_coin_list().split(',')
    search_term = 'market/currency/'
    blobs = list_files_in_bucket(bucket_name = bucket_name, prefix = search_term)
    crypto_path = 'market/crypto/'
    files_to_append = list_files_in_bucket(bucket_name = bucket_name, prefix = crypto_path)
    if len(blobs) > 0:
        prev_day_filepath = crypto_path + get_previous_date()
        files_to_append = list_files_in_bucket(bucket_name = bucket_name, prefix = prev_day_filepath)

    create_coin_data(bucket_name, files_to_append, coins, destination = 'market/currency/')


def create_coin_data(bucket_name: str, file_list, coins, destination):
    coins_dict = {}
    for coin in coins:
         coins_dict[coin] = []

    for blob in file_list:
        hourly_data = download_file_data(bucket_name, blob.name)
        for coin_info in hourly_data:
            timestamp_data = {
                'symbol': coin_info['symbol'],
                'name': coin_info['name'],
                'price': coin_info['current_price'],
                'market_cap': coin_info['market_cap'],
                'rank': coin_info['market_cap_rank'],
                'volume': coin_info['total_volume'],
                'price_change_24h': coin_info['price_change_24h'],
                'price_change_percentage_24h': coin_info['price_change_percentage_24h'],
                'record_date': coin_info['recorded_time'].split('T')[0],
                'record_time': coin_info['recorded_time'].split('T')[1][:5].replace('-',':')
            }
            coins_dict[coin_info['symbol']].append(timestamp_data)
        
    for coin in coins:
        curr_path = destination + coin + '.json'
        data = download_file_data(bucket_name = bucket_name, filepath = curr_path)
        for timestamp_data in coins_dict[coin]:
            data.append(timestamp_data)
        # Now that we have the data, just upload it whole
        upload_data(bucket_name = bucket_name, source_data = json.dumps(data), destination_blob_name = curr_path)