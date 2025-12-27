# 🚀 CryptoAnalyzer - Automated Cryptocurrency Data Pipeline and Public APIs

**CryptoAnalyzer** is a cloud-native cryptocurrency analytics platform that fetches, processes, and stores market data from CoinGecko using a fully automated pipeline. This pipeline is dockerised, so it can run without the hassle of version mismatch for the dependencies(Trust me, faced the issue and learnt the hard way). It is beautifully designed with a powerful backend stack hosted on Google Cloud.



## 📦 What It Does

- ⛓️ Fetches live data hourly using **Cloud Scheduler + Cloud Run**
- 🛠️ Modular Approach: Fetch → Transform → Upload Pipeline
- 📁 Updates and stores JSON files per hour of the day and per coin in **Google Cloud Storage**
- 🌐 Exposes Flask-based API endpoints to access the processed data
- 📊 So easy to access that Frontend dashboard displays price trends, moving averages, volume bars
- 🔐 Secured endpoints for data uploads and POST methods to make sure that your pipeline is free from outside tampering.
- 🧠 LLM integrations (upcoming) will add auto-generated insights per coin



## 🧰 Tech Stack

- **Cloud Platform:** Google Cloud Platform (Cloud Build, Cloud Run, Cloud Scheduler, Google Cloud Storage)
- **Backend:** Python, Flask, Docker
- **Data Source:** [CoinGecko API](https://www.coingecko.com/en/api)



# 🌐 Live API Endpoint

**Base URL:**  [CryptoAnalyzer](https://crypto-analyzer-service-1073952782451.us-central1.run.app/)



## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/get-latest-data` | Get the latest snapshot of all tracked coins |
| `GET`  | `/coin/<symbol>` | Get full historical data for a specific coin |
| `POST`  | `/run` | Triggers the pipeline to fill the hourly files and each of the crypto files |



## 🚀 Deployment

This project is designed to run **exclusively on GCP**:

### Pre-requisites
- Google Cloud Platform account with access to Cloud Run, Google Cloud Storage
- Service Account to be used for automated filling of the files, with atleast `Storage Object Admin` and `Cloud Run Invoker` roles.
- An API key to access data from CoinGecko. [Get from here](https://www.coingecko.com/en/developers/dashboard)

1. **Clone this repo into your system and go to this repository**
   If you want to get data pipeline enabled for your own custom crypto-currencies, just add their names in this file, [Coin List](resources/coin_list.txt)
2. **Build Docker Image:**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/IMAGE_NAME_FOR_THE_BUILD
   ```
3. **Create a GCP Cloud Run Service:**
   ```bash
   gcloud run deploy NAME_FOR_CLOUD_RUN_SERVICE \
   --image gcr.io/YOUR_PROJECT_ID/IMAGE_NAME_FOR_THE_BUILD \
   --region REGION \
   --platform managed \
   --allow-unauthenticated \
   --timeout=900 \
   --memory=512Mi \
   --service-account=SERVICE-ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com \
   --set-env-vars "GCS_BUCKET=GCS_BUCKET_TO_STORE_FILES,CRYPTO_API_KEY=API_KEY_FROM_COINGECKO,CLOUD_PUSHING_PROT=KEY_FOR_TRIGGERING_THE_PIPELINE"
   ```
   To prevent the secrets from getting exposed, they are passed during the Service build command itself. Provide the GCS bucket name and the CoinGecko API key as well. Apart from these, mention each detail correctly from the GCloud platform here and use a custom string for `CLOUD_PUSHING_PROT` as this will prevent any outsider from triggering the pipeline unnecessarily. You can also enable OIDC security provided by Google by simply replacing `--allow-unauthenticated` with `--no-allow-unauthenticated`, but, keep in mind the GET API endpoints will also be encrypted, and only visible if you deploy the frontend on GCP as well...

   Once the build is successful, you'll receive the URI for you Cloud Run service, use that in the next step to schedule the run. Alternatively, the URI can be located throught the Cloud Run dashboard in GCP.
   
4. **Create a GCP Cloud Run Service:**
   ```bash
   gcloud scheduler jobs create http JOB_NAME \
   --schedule="0 * * * *" \
   --uri="URI_FOR_GCLOUD_RUN_SERVICE/run" \
   --http-method=POST \
   --headers="Authorization=KEY_FOR_TRIGGERING_THE_PIPELINE" \
   --location=REGION
   ```
   This will trigger the execution for the URI with endpoint `/run` and method POST, every hour at `0` minutes.... In the headers, use the same `KEY_FOR_TRIGGERING_THE_PIPELINE` for Authorization that you used while creating the run service. Additionally, if you used OIDC encryption, use `--oidc-service-account-email="SERVICE-ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com"`

And Voila, the crypto pipeline for your system is now up and running.
Want to check, just head to your browser and type in:
> <URI_FOR_GCLOUD_RUN_SERVICE>
It would show something like this
 ```json
  {
  "status": "This URI is working for the methods"
  }
  ```
> <URI_FOR_GCLOUD_RUN_SERVICE>/get-latest-data
 ```json
 [
  {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1696501400",
    "current_price": 107187,
  ...
```

## Frontend Demo Link
  This one is a simple Demo with very limited capabilities of the pipeline data.
  > [🚀 CryptoLiner](https://crypto-liner-asje.vercel.app/)
