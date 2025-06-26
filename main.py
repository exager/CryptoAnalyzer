from flask import Flask, Request, jsonify
from pipeline.run_pipeline import run_hourly_updates, get_daily_currency_data
from werkzeug.datastructures import Headers
from utils.time_utils import get_current_date, get_current_time
from gcs_interface.downloader import get_recent_data
import os

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def status_check():
    return jsonify({"status":"This URI is working for the methods"}), 200

@app.route("/run", methods = ["POST"])
def run_job():
    try:
        update1 = run_hourly_updates()
        update2 = get_daily_currency_data()
        return jsonify({"status-1": update1, "status-2": update2}), 200
    except Exception as e:
        return jsonify({"error": f"Got an error while trying to run the pipeline on {get_current_date()} at {get_current_time()}: " + str(e)}), 500

@app.route("/get-latest-data", methods = ["GET"])
def get_crypto_prices():
    try:
        recent_data = get_recent_data()
        return jsonify(recent_data), 200
    except Exception as e:
        return jsonify({"error": f"Got an error while fetching the data on {get_current_date()} at {get_current_time()}: " + str(e)}), 500

def main(request: Request):
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))