# stk_push.py
import requests
import base64
from datetime import datetime
import json
from .mpesa_config import *

def get_access_token():
    """Generate M-Pesa access token"""
    url = (
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        if MPESA_ENV == "sandbox"
        else "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    )
    res = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    if res.status_code == 200:
        return res.json()["access_token"]
    else:
        print("❌ Failed to get access token:", res.text)
        return None


def initiate_stk_push(phone, amount, event_name, user_id):
    """Initiate STK Push"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()).decode()
    access_token = get_access_token()

    if not access_token:
        print("❌ Could not get access token.")
        return {"error": "Failed to authenticate"}

    payload = {
        "BusinessShortCode": MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": MPESA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": f"Event-{event_name}",
        "TransactionDesc": f"Payment for {event_name} by user {user_id}",
    }

    stk_url = (
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        if MPESA_ENV == "sandbox"
        else "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    )

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}

    print(f"🚀 Sending STK Push for event: {event_name}")
    response = requests.post(stk_url, json=payload, headers=headers)
    try:
        res_json = response.json()
    except json.JSONDecodeError:
        res_json = {"raw_response": response.text}

    # Save for debugging
    with open("stk_event_response.json", "w") as file:
        json.dump(res_json, file, indent=4)

    return res_json
