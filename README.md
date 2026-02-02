# Task – Lead Processing API

## Description

This project implements a small FastAPI-based webhook service that simulates a real-world lead processing pipeline.

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
<img width="996" height="212" alt="image" src="https://github.com/user-attachments/assets/cbdfde94-405d-421c-a5b1-98095cbb3258" />


4. The webhook will be available at:
```bash
http://127.0.0.1:8000/webhook
```
## make it public, Expose the service using ngrok (ngrok) (Run it in seperate terminal)
```bash
ngrok http 8000
```
## create ngrok account from here, if not done before
## Create a free ngrok account

Open this link:
https://dashboard.ngrok.com/signup

## Copy your authtoken
After login:
https://dashboard.ngrok.com/get-started/your-authtoken

## Add authtoken in WSL (one-time setup)
Run exactly what ngrok gives you:
```bash
ngrok config add-authtoken (copy your authtocken)
```
This writes to:
```bash
~/.config/ngrok/ngrok.yml
```
### Start tunnel again with ngrok http 8000 in the seperate terminal
<img width="863" height="291" alt="image" src="https://github.com/user-attachments/assets/3693e7df-2d24-4fbc-85c3-08b85a2c6b85" />

## Example: Sending a Test Lead
```bash
curl -X POST http://127.0.0.1:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "postcode": "66123",
    "solar_owner": "Ja",
    "phone": "0176111222333",
    "first_name": "Max",
    "last_name": "Mustermann",
    "street": "Musterstraße",
    "housenumber": "1",
    "city": "Musterstadt",
    "landingpage_url": "https://example.com",
    "unique_id": "123456",
    "utm_source": "google",
    "optin": "true",
    "solar_energy_consumption": "5000",
    "solar_offer_type": "Kaufen",
    "solar_property_type": "Einfamilienhaus",
    "product": {
      "name": "makler"
    }
  }'
```
This solution demonstrates how incoming leads can be validated, transformed, and forwarded to customer-specific APIs in a clean and extensible way, closely reflecting real-world lead distribution systems.

Note: “Swagger UI cannot fully represent the dynamic incoming lead schema. Testing was done using curl with raw JSON payloads, which mirrors real webhook behavior.”



