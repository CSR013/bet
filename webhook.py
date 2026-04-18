from flask import Flask, request
import requests
from database import liberar_usuario
from config import MP_ACCESS_TOKEN

app = Flask(__name__)

# ✅ ROTA HOME (TESTE DO SITE)
@app.route("/")
def home():
    return "Bot rodando com sucesso"


# ✅ WEBHOOK DO MERCADO PAGO
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    if data["type"] == "payment":

        payment_id = data["data"]["id"]

        r = requests.get(
            f"https://api.mercadopago.com/v1/payments/{payment_id}",
            headers={"Authorization": f"Bearer {MP_ACCESS_TOKEN}"}
        )

        payment = r.json()

        if payment.get("status") == "approved":

            user_id = payment.get("external_reference")
            liberar_usuario(user_id)

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)