# CryptoLiner

An end-to-end crypto tracking pipeline that fetches hourly data from CoinGecko, stores it in GCS, and optionally exposes APIs to trigger ingestion — deployable via Google Cloud Run.

## Stack

- Python + Flask
- Google Cloud Storage
- Google Cloud Scheduler
- Docker + GitHub Actions (coming soon)

## Features

- Hourly ingestion of selected coins
- Modular fetch → transform → upload pipeline
- Flask API wrapper to trigger manually
- Fully containerized and GCP-deployable

## To Do

- Add dashboards + insights
- Optional LLM integration
