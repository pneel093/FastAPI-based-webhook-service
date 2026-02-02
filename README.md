# CHECKFOX Developer Test Task – Lead Processing API

## Description

This project implements a small FastAPI-based webhook service that simulates a real-world lead processing pipeline for CHECKFOX.

The service receives lead/contact data, validates it against customer-specific rules, transforms the data according to provided documentation, and forwards valid leads to a customer API endpoint.

## Task Requirements (Summary)

- Receive lead data on a single URL
- Validate leads:
  - ZIP code must start with 66*
  - The person must be the owner of the house
- Transform incoming data into the customer’s expected API format
- Forward valid leads to the customer API endpoint
- Use code for the transformation step (FastAPI / Python)

## Validation Logic

A lead is accepted only if:
- postcode starts with "66"
- solar_owner equals "Ja"
All other leads are ignored or rejected.

## Running the Project Locally

1. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate 
```

2. Install dependencies
```bash
pip install fastapi uvicorn requests
```

3. Start the server
```bash
uvicorn main:app --reload
```
4. The webhook will be available at:
```bash
http://127.0.0.1:8000/webhook
```
## make it public, Expose the service using ngrok (ngrok) (Run it in seperate terminal)
```bash
ngrok http 8000
```