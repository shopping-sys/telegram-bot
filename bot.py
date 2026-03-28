import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ၁။ Gemini API Key အသစ်ကို ဒီမှာ ထည့်ပါ
GOOGLE_API_KEY = "AIzaSyDRp11oxZlNflcgO1544gUPunL5-yZmS6U"
genai.configure(api_key=GOOGLE_API_KEY)

# ၂။ Model Name ကို gemini-1.5-pro လို့ပဲ ထားပါ (NotFound Error မတက်စေရန်)
model = genai.GenerativeModel("gemini-2.5-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # စာသားမဟုတ်တာတွေ ပို့ရင် ဘာမှမလုပ်ဘဲ ကျော်သွားပါမယ်
    if not update.message or not update.message.text:
        return

    # Bot က စာရိုက်နေသလိုပြအောင် လုပ်ခြင်း
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Gemini ဆီက အဖြေတောင်းခြင်း
        response = model.generate_content(update.message.text)
        
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Gemini ဆီက အဖြေမရရှိပါဘူးခင်ဗျာ။")

    except Exception as e:
        # Error တက်ရင် Telegram မှာ တန်းပြပါမယ်
        await update.message.reply_text(f"Error တက်နေပါတယ်ခင်ဗျာ: {str(e)}")

if __name__ == '__main__':
    # ၃။ Telegram Bot Token အသစ်ကို ဒီမှာ ထည့်ပါ
    # BotFather ဆီက ရလာတဲ့ Token အသစ် ဖြစ်ရပါမယ်
    BOT_TOKEN = "8473779952:AAGqWhA-9xYjQU0nVyGLmRPNXlQ-RSFEZag"
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Message Handler ထည့်ခြင်း
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is starting on Hugging Face...")
    app.run_polling()
