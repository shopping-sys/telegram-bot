import os
import google.generativeai as genai
from google.generativeai import types
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Replace with your actual Gemini API Key
genai.configure(api_key="AizasyAp54QILRrcmZlx0R13ber47wtEniykDYA")

# Client ကို model ထဲမှာ တိုက်ရိုက်သုံးတာ ပိုအဆင်ပြေပါတယ်
model = genai.GenerativeModel("gemini-1.5-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Safety settings ကို enum type အနေနဲ့ သတ်မှတ်ခြင်း
        safety_settings = [
            {
                "category": types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                "threshold": types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                "threshold": types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                "threshold": types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                "threshold": types.HarmBlockThreshold.BLOCK_NONE,
            },
        ]

        response = model.generate_content(
            contents=update.message.text,
            safety_settings=safety_settings
        )

        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Gemini did not return any text.")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    # Replace with your actual Telegram Bot Token
    TOKEN = "8606318283:AAG0Jbln4DTQmwiL3q4ceHXE603dj7U5tq8"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Message handler setting
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)
