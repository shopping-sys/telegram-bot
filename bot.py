import os
import logging
import requests
import google.generativeai as genai

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY")
if not HF_TOKEN:
    raise ValueError("Missing HF_TOKEN")

genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

HF_MODEL = "google/flan-t5-base"

def ask_huggingface(prompt: str) -> str:
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()

        if isinstance(data, list) and len(data) > 0:
            item = data[0]
            if isinstance(item, dict):
                return item.get("generated_text", str(item))
            return str(item)

        if isinstance(data, dict):
            return data.get("generated_text", str(data))

        return str(data)
    except Exception as e:
        return f"Hugging Face error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "မင်္ဂလာပါ 👋\n\n"
        "Commands:\n"
        "/ask <question> - Google AI နဲ့မေး\n"
        "/hf <text> - Hugging Face နဲ့မေး\n"
    )
    await update.message.reply_text(text)

async def ask_google(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args).strip()

    if not prompt:
        await update.message.reply_text("အသုံးပြုပုံ: /ask မင်းမေးချင်တာ")
        return

    try:
        response = gemini_model.generate_content(prompt)
        answer = response.text if hasattr(response, "text") else "No response."
        await update.message.reply_text(answer[:4000])
    except Exception as e:
        await update.message.reply_text(f"Google API error: {e}")

async def ask_hf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args).strip()

    if not prompt:
        await update.message.reply_text("အသုံးပြုပုံ: /hf မင်းမေးချင်တာ")
        return

    answer = ask_huggingface(prompt)
    await update.message.reply_text(answer[:4000])

async def normal_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    try:
        response = gemini_model.generate_content(user_text)
        answer = response.text if hasattr(response, "text") else "No response."
        await update.message.reply_text(answer[:4000])
    except Exception:
        answer = ask_huggingface(user_text)
        await update.message.reply_text(answer[:4000])

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask_google))
    app.add_handler(CommandHandler("hf", ask_hf))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, normal_chat))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
