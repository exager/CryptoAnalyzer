from flask import Flask, Request, jsonify
from pipeline.run_pipeline import run
from werkzeug.datastructures import Headers
from utils.time_utils import get_current_date, get_current_time

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def status_check():
    return jsonify({"status":"This URI is working for the methods"}), 200

@app.route("/run", methods = ["POST"])
def run_job():
    try:
        run()
        return jsonify({"status": "Pipeline executed"}), 200
    except Exception as e:
        return jsonify({"error": f"Got an error while trying to run the pipeline on {get_current_date()} at {get_current_time}: " + str(e)}), 500

def main(request: Request):

    mutable_headers = Headers(request.headers.items())
    # Use Flask's test_request_context to handle the incoming request inside your Flask app
    with app.test_request_context(
        path=request.path,
        base_url=request.base_url,
        query_string=request.query_string,
        method=request.method,
        headers=mutable_headers,
        data=request.get_data()
    ):
        resp = app.full_dispatch_request()
        return resp