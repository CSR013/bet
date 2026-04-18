import requests
from config import MP_ACCESS_TOKEN, VALOR_CONSULTA

def gerar_pagamento(user_id):

    headers = {
        "Authorization": f"Bearer {MP_ACCESS_TOKEN.strip()}",
        "Content-Type": "application/json"
    }

    payload = {
        "transaction_amount": float(VALOR_CONSULTA),
        "description": "Consulta",
        "payment_method_id": "pix",
        "external_reference": str(user_id),
        "payer": {
            "email": f"user{user_id}@email.com"
        }
    }

    r = requests.post(
        "https://api.mercadopago.com/v1/payments",
        json=payload,
        headers=headers
    )

    data = r.json()

    if r.status_code not in [200, 201]:
        raise Exception(data)

    tx = data["point_of_interaction"]["transaction_data"]

    return tx["qr_code_base64"], tx["qr_code"]