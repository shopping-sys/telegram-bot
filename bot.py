import os
from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text
        )
        reply = response.text if response.text else "No response from Gemini."
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Gemini error: " + str(e))

def main():
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN not found in .env")
        return

    if not GEMINI_KEY:
        print("GEMINI_API_KEY not found in .env")
        return

    print("Starting bot...")
    app = ApplicationBuilder().token(TOKEN).connect_timeout(30).read_timeout(30).write_timeout(30).pool_timeout(30).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()