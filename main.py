from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("API_KEY")
API_URL = os.environ.get("API_URL")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text
    await update.message.reply_text("⏳ Downloading, please wait...")

    headers = {
        "Authorization": API_KEY
    }

    params = {
        "url": link
    }

    r = requests.get(API_URL, headers=headers, params=params)

    if r.status_code == 200:
        data = r.json()
        download_url = data.get("download_url")

        if download_url:
            await update.message.reply_video(download_url)
        else:
            await update.message.reply_text("❌ Download failed.")
    else:
        await update.message.reply_text("❌ API error.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
