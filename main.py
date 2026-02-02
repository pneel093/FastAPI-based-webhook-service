from fastapi import FastAPI, Request
import requests

app = FastAPI()

USER_ID = "patel"
CUSTOMER_API_URL = f"https://contactapi.static.fyi/lead/receive/fake/{USER_ID}/"
AUTH_HEADER = {
    "Authorization": "Bearer FakeCustomerToken",
    "Content-Type": "application/json"
}

# Attribute mapping (from customer_attribute_mapping.json)
ATTRIBUTE_MAPPING = {
    "solar_energy_consumption": {"is_numeric": True},
    "solar_monthly_electricity_bill": {"is_numeric": True},
    "solar_offer_type": {"values": ["Beides interessant", "Mieten", "Kaufen"]},
    "solar_owner": {"values": ["Ja", "Nein", "In Auftrag"]},
    "solar_power_storage": {"values": ["Ja", "Nein", "Noch nicht sicher"]},
    "solar_property_type": {"values": [
        "Einfamilienhaus", "Zweifamilienhaus", "Mehrfamilienhaus", "Firmengebäude",
        "Freilandfläche", "Garage", "Carport", "Scheune/Landwirtschaft",
        "Lagerhalle", "Industrie"
    ]},
    "solar_roof_age": {"values": [
        "Erst in Planung", "Gerade erst gebaut",
        "Jünger als 30 Jahre", "Älter als 30 Jahre"
    ]},
    "solar_roof_condition": {"values": [
        "Asbestbelastet", "Frisch renoviert", "Guter Zustand",
        "In Ordnung", "Renovierungsbedürftig", "Neubau"
    ]},
    "solar_roof_material": {"values": [
        "Asbest", "Bitumen", "Blech/Trapezblech", "Dachziegel",
        "Gründach", "Holzdach", "Kies", "Schiefer",
        "Schindeldach", "Andere"
    ]},
    "solar_roof_type": {"values": [
        "Andere", "Flachdach", "Kaffeemühlenhaus", "Krüppelwalmdach",
        "Mansardendach", "Pultdach", "Satteldach",
        "Versetztes Pultdach", "Walmdach", "Winkelwalmdach", "Zwerchdach"
    ]},
    "solar_south_location": {"values": [
        "Ja", "Nein", "Teilweise", "Nicht sicher",
        "Keine (Flachdach)", "Süd", "Süd-West", "Süd-Ost", "West", "Ost"
    ]},
    "solar_usage": {"values": [
        "Eigenverbrauch", "Netzeinspeisung",
        "Netzeinspeisung und Eigenverbrauch"
    ]},
    "solar_area": {"is_numeric": True}
}


@app.post("/webhook")
async def receive_lead(request: Request):
    data = await request.json()

    postcode = data.get("postcode") or data.get("zip", "")
    phone = data.get("phone")

    # Business rules
    if not postcode.startswith("66"):
        return {"status": "rejected", "reason": "postcode not allowed"}

    if data.get("solar_owner") != "Ja":
        return {"status": "rejected", "reason": "not a homeowner"}

    if not phone:
        return {"status": "rejected", "reason": "missing phone"}

    # Validate & map attributes
    lead_attributes = {}
    for key, rules in ATTRIBUTE_MAPPING.items():
        value = data.get(key)
        if not value:
            continue

        if rules.get("is_numeric") and not str(value).isdigit():
            continue

        if "values" in rules and value not in rules["values"]:
            continue

        lead_attributes[key] = value

    payload = {
        "lead": {
            "phone": phone,
            "email": data.get("email"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "street": data.get("street"),
            "housenumber": data.get("housenumber"),
            "postcode": postcode,
            "city": data.get("city"),
            "country": "de"
        },
        "product": {
            "name": "solar"
        },
        "lead_attributes": lead_attributes,
        "meta_attributes": {
            "landingpage_url": data.get("landingpage_url"),
            "unique_id": data.get("unique_id"),
            "utm_source": data.get("utm_source"),
            "optin": data.get("optin")
        }
    }

    response = requests.post(
        CUSTOMER_API_URL,
        headers=AUTH_HEADER,
        json=payload,
        timeout=10
    )

    return {
        "status": "sent",
        "customer_status": response.status_code,
        "customer_response": response.text
    }
