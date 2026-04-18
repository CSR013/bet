from reportlab.pdfgen import canvas
from datetime import datetime


def assinar_pdf(nome):

    caminho = "assinatura.pdf"

    c = canvas.Canvas(caminho)

    c.drawString(100, 700, f"Assinado digitalmente por: {nome}")

    c.drawString(100, 680, f"Data: {datetime.now()}")

    c.save()

    return caminho