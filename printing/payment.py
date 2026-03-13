import requests
import uuid


def request_momo_payment(amount, phone):

    url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"

    reference_id = str(uuid.uuid4())

    headers = {
        "X-Reference-Id": reference_id,
        "X-Target-Environment": "sandbox",
        "Ocp-Apim-Subscription-Key": "YOUR_SUBSCRIPTION_KEY",
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ACCESS_TOKEN"
    }

    payload = {
        "amount": str(amount),
        "currency": "EUR",
        "externalId": reference_id,
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": phone
        },
        "payerMessage": "Print Order Payment",
        "payeeNote": "ABC Enterprise Printing"
    }

    response = requests.post(url, json=payload, headers=headers)

    return reference_id, response.json()