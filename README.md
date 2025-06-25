# CryptoLiner

An end-to-end crypto tracking pipeline that fetches hourly data from CoinGecko, stores it in GCS, and optionally exposes APIs to trigger ingestion — deployable via Google Cloud Run. This pipeline is dockerised, so it can run without the hassle of version mismatch for the dependencies(Trust me, faced the issue and learnt the hard way) 

## Stack

- Python + Flask
- Google Cloud Storage
- Google Cloud Run
- Google Cloud Scheduler
- Docker 

## Features

- Hourly ingestion of selected coins
- Modular fetch → transform → upload pipeline
- Flask API wrapper to trigger manually
- Fully containerized and GCP-deployable

## To Do

- Add dashboards + insights
- Optional LLM integration

## Frontend To Be Added soon