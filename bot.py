import os
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Replace with your actual Gemini API Key
client = genai.Client(api_key="AIzaSyAp54QILRRcmZlxOR13ber47wtEniykDYA")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text: return
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=update.message.text,
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                ]
            )
        )
        
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Gemini did not return any text.")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    # Replace with your actual Telegram Bot Token
    TOKEN = "8606318283:AAGOJbln4dTQmwIL3q4ceHXE6O3dj7U5tq8"
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)
