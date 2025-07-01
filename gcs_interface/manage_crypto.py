from google.cloud import storage
from utils.list_coins import load_coin_list
from gcs_interface.downloader import list_files_in_bucket, download_file_data
from gcs_interface.uploader import upload_data
from utils.time_utils import get_current_date, get_current_time, get_previous_date
from utils.logger import logger
import json

def run_coin_history(bucket_name: str):
    logger.info(f'Triggered the Currency File data upload/append for {get_current_date()}, {get_current_time()}')
    coins = load_coin_list().split(',')
    logger.info(f'  Collected coins info.')
    search_term = 'market/currency/'
    blobs = list_files_in_bucket(bucket_name = bucket_name, prefix = search_term)
    crypto_path = 'market/crypto/'
    files_to_append = list_files_in_bucket(bucket_name = bucket_name, prefix = crypto_path)
    if len(blobs) > 0:
        logger.info(f'  Coins data already present, moving ahead with appending the files...')
        curr_hour_filepath = crypto_path + get_current_date() +'/T' + get_current_time()[:2]
        files_to_append = list_files_in_bucket(bucket_name = bucket_name, prefix = curr_hour_filepath)

    create_coin_data(bucket_name, files_to_append, coins, destination = 'market/currency/')


def create_coin_data(bucket_name: str, file_list, coins, destination):
    coins_dict = {}
    for coin in coins:
         coins_dict[coin] = []

    logger.info('Preparing the coins data for each crypto-currency to be uploaded into the bucket')
    for blob in file_list:
        logger.info(f'Fetching data from file {blob.name}...')
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
        logger.info(f'Appending the file {curr_path} with the data upto {get_previous_date()}...')
        data = download_file_data(bucket_name = bucket_name, filepath = curr_path)
        for timestamp_data in coins_dict[coin]:
            data.append(timestamp_data)

        # Now that we have the data, just upload it whole
        logger.info("Data appended, now uploading....")
        upload_data(bucket_name = bucket_name, source_data = json.dumps(data), destination_blob_name = curr_path)