from flask import Flask, Request, jsonify, request
from pipeline.run_pipeline import run_hourly_updates, get_daily_currency_data
from werkzeug.datastructures import Headers
from utils.time_utils import get_current_date, get_current_time
from gcs_interface.downloader import get_recent_data, coin_data
import os
import traceback
from utils.logger import logger

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def status_check():
    logger.info('Base endpoint triggered...')
    return jsonify({"status":"This URI is working for the methods"}), 200

@app.route("/run", methods = ["POST"])
def run_job():
    logger.info('Triggered the pipeline run....')
    auth = request.headers.get("Authorization")
    if auth != f'{os.getenv("CLOUD_PUSHING_PROT")}':
        logger.debug(f'Expected Header data {os.getenv("CLOUD_PUSHING_PROT")}, instead got: {auth}')
        logger.error("Cannot run the piepline. Wrong Authentication token")
        return jsonify({"error": "Unauthorized"}), 401
    try:
        update1 = run_hourly_updates()
        update2 = get_daily_currency_data()
        return jsonify({"status-1": update1, "status-2": update2}), 200
    except Exception as e:
        logger.error(f'Pipeline Run Failure:\n {traceback.print_exc()}')
        return jsonify({"error": f"Got an error while trying to run the pipeline on {get_current_date()} at {get_current_time()}: " + str(e)}), 500

@app.route("/get-latest-data", methods = ["GET"])
def get_crypto_prices():
    logger.info(f"Triggered the endpoint to get the latest crypto data at {get_current_time()}, {get_current_date()}...")
    try:
        recent_data = get_recent_data()
        logger.info("Latest Crypto data fetched from the system.")
        return jsonify(recent_data), 200
    except Exception as e:
        logger.error(f'Got an Exception while fetching the latest data:\n {traceback.print_exc()}')
        return jsonify({"error": f"Got an error while fetching the data on {get_current_date()} at {get_current_time()}: " + str(e)}), 500

@app.route("/coin/<symbol>", methods = ["GET"])
def get_currency_price(symbol):
    logger.info(f"Getting the price trend data for currency {symbol}...")
    try:
        curr_data = coin_data(symbol)
        return jsonify(curr_data), 200
    except Exception as e:
        logger.error(f'Got an Exception while fetching the latest data:\n {traceback.print_exc()}')
        return jsonify({"error": f"Got an error while fetching the data on {get_current_date()} at {get_current_time()}: " + str(e)}), 500

def main(request: Request):
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))