import base64

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import TOKEN_TELEGRAM
from database import verificar_usuario, liberar_usuario
from pix_service import gerar_pagamento
from ai_service import responder
from contract_generator import gerar
from agreement_generator import gerar as gerar_acordo
from docx_generator import gerar_docx


# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Digite /pagar para iniciar a consulta")


# =========================
# PAGAMENTO PIX
# =========================
async def pagar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    qr_base64, copia = gerar_pagamento(user_id)

    imagem = base64.b64decode(qr_base64)

    with open("pix.png", "wb") as f:
        f.write(imagem)

    keyboard = [
        [InlineKeyboardButton("💳 Já paguei", callback_data=f"check_{user_id}")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=open("pix.png", "rb"),
        caption=f"📲 Pix Copia e Cola:\n\n{copia}",
        reply_markup=reply_markup
    )


# =========================
# CALLBACK (BOTÃO JÁ PAGUEI)
# =========================
async def verificar_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("check_"):

        user_id = data.split("_")[1]

        await query.edit_message_caption(
            caption="⏳ Verificando pagamento..."
        )

        # ⚠️ ainda é verificação local (sem webhook)
        if verificar_usuario(user_id):

            await query.edit_message_caption(
                caption="✅ Pagamento confirmado! Liberado."
            )

        else:

            await query.edit_message_caption(
                caption=(
                    "❌ Pagamento ainda não identificado.\n\n"
                    "📌 Se você acabou de pagar, aguarde até 1 minuto e tente novamente.\n\n"
                    "Se o problema persistir:\n"
                    "- verifique se o Pix foi concluído\n"
                    "- ou entre em contato com o suporte"
                )
            )


# =========================
# MENSAGENS NORMAIS
# =========================
async def responder_usuario(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if not verificar_usuario(user_id):
        await update.message.reply_text("Use /pagar primeiro")
        return

    texto = update.message.text.lower()

    if "contrato" in texto:
        contrato = gerar(texto)
        arquivo = gerar_docx(contrato)
        await update.message.reply_document(open(arquivo, "rb"))
        return

    if "acordo" in texto:
        acordo = gerar_acordo(texto)
        arquivo = gerar_docx(acordo)
        await update.message.reply_document(open(arquivo, "rb"))
        return

    resposta = responder(texto)
    await update.message.reply_text(resposta)


# =========================
# APP
# =========================
app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("pagar", pagar))

app.add_handler(CallbackQueryHandler(verificar_pagamento))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_usuario))

app.run_polling()