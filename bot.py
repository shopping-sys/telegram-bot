import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# 1. API Key Configuration
genai.configure(api_key="AizasyAp54QILRrcmZlx0R13ber47wtEniykDYA")

# 2. Model Setup (Flash model က ပိုမြန်ပါတယ်)
model = genai.GenerativeModel("gemini-1.5-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text:
        return

    # Bot က စာရိုက်နေသလို ပြပေးရန်
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # မလိုအပ်တဲ့ safety_settings တွေကို အကုန်ဖြုတ်လိုက်ပါပြီ
        # ဒါဆိုရင် Error တက်စရာ အကြောင်းမရှိတော့ပါဘူး
        response = model.generate_content(update.message.text)

        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Gemini did not return any text.")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    # 3. Telegram Bot Token
    TOKEN = "8606318283:AAG0Jbln4DTQmwiL3q4ceHXE603dj7U5tq8"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Message တွေကို လက်ခံမည့် Handler
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)
