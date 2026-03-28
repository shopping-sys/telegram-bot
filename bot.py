import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ၁။ Gemini API Key
genai.configure(api_key="AizasyAp54QILRrcmZlx0R13ber47wtEniykDYA")
model = genai.GenerativeModel("gemini-1.5-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = model.generate_content(update.message.text)
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Gemini did not return any text.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    # ၂။ သင့်ရဲ့ Bot Token အသစ်ကို ဒီနေရာမှာ သေချာထည့်ပါ
    TOKEN = "8734152863:AAFNZWBpwHpzFNN3LPwar9VI7aijq8gs5jA"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)
