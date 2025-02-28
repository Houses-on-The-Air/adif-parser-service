# ADIF Parser Service

## Overview

This FastAPI microservice accepts an ADIF file upload, extracts unique callsigns, determines an award tier, and returns the data in JSON format.

## Features

- Accepts ADIF file uploads
- Extracts unique callsigns
- Determines an award tier based on the number of unique callsigns
- Returns results as a JSON object

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- adif_io

## Installation

1. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

2. Run the application:

   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Docker Usage

### Build the Docker Image

```sh
docker build -t adif-parser-service .
```

### Run the Container

```sh
docker run -p 8000:8000 adif-parser-service
```

## API Endpoint

- `POST /upload_adif/`
  - Accepts an ADIF file and returns JSON with:

    ```json
    {
      "unique_addresses": 10,
      "award_tier": "Bronze",
      "callsign": "AB1CDE"
    }
    ```
