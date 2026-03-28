import os
import google.generativeai as genai
from google.generativeai import types
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# 1. Gemini API Key Configuration
# မှတ်ချက် - လုံခြုံရေးအရ ဒီ Key ကို နောက်ပိုင်းမှာ အသစ်လဲရန် အကြံပြုလိုပါတယ်
genai.configure(api_key="AizasyAp54QILRrcmZlx0R13ber47wtEniykDYA")

# 2. Model Setup
model = genai.GenerativeModel("gemini-1.5-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text:
        return

    # Bot က စာရိုက်နေသလို ပြပေးရန်
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # 3. Safety Settings (အရေးကြီးဆုံးအပိုင်း)
        # မျက်တောင်ဖွင့်ပိတ် " " မပါဘဲ types.HarmCategory ကို တိုက်ရိုက်သုံးရပါမယ်
        safety_settings = [
            {
                "category": types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                "threshold": types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
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

        # 4. Generate Content
        response = model.generate_content(
            contents=update.message.text,
            safety_settings=safety_settings
        )

        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Gemini did not return any text.")

    except Exception as e:
        # Error တက်ရင် Telegram မှာ ပြပေးရန်
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    # 5. Telegram Bot Token
    TOKEN = "8606318283:AAG0Jbln4DTQmwiL3q4ceHXE603dj7U5tq8"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Message တွေကို လက်ခံမည့် Handler
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running...")
    # Update ဟောင်းတွေကို ကျော်ပြီး အသစ်ကနေ စတင်ရန်
    app.run_polling(drop_pending_updates=True)
