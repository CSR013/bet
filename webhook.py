from flask import Flask, request
from database import liberar_usuario

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    if data["type"] == "payment":

        payment_id = data["data"]["id"]

        import requests
        from config import MP_ACCESS_TOKEN

        r = requests.get(
            f"https://api.mercadopago.com/v1/payments/{payment_id}",
            headers={"Authorization": f"Bearer {MP_ACCESS_TOKEN}"}
        )

        payment = r.json()

        if payment.get("status") == "approved":

            user_id = payment.get("external_reference")

            liberar_usuario(user_id)

    return "OK"