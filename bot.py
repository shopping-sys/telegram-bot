import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ၁။ API Key အသစ်ကို ဒီမှာ ထည့်ပါ
genai.configure(api_key="AIzaSyDRp11oxZlNflcgO1544gUPunL5-yZmS6U")

# Model ကို နာမည်အပြည့်အစုံနဲ့ ခေါ်ကြည့်ပါ
model = genai.GenerativeModel("models/gemini-2.5-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Generation config ကို default ထားပြီး စမ်းပါ
        response = model.generate_content(update.message.text)
        
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Gemini did not return any text.")

    except Exception as e:
        # Error အမျိုးအစားကို ပိုသိသာအောင် ပြခိုင်းထားပါတယ်
        await update.message.reply_text(f"Error Type: {type(e).__name__}\nMessage: {str(e)}")

if __name__ == '__main__':
    # ၂။ Telegram Bot Token ကို ဒီမှာ ထည့်ပါ
    TOKEN = "8473779952:AAGqWhA-9xYjQU0nVyGLmRPNXlQ-RSFEZag"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is starting...")
    app.run_polling(drop_pending_updates=True)
