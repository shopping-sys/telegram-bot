import os
import asyncio
from google import genai # Library အသစ်
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ၁။ Gemini Client အသစ် Setup
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_ID = "gemini-1.5-flash"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text: return

    # User ကို ခဏစောင့်ဖို့ ပြောမယ်
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # ၂။ Gemini ဆီက အဖြေတောင်းခြင်း
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=user_text
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("ခဏလေးနော်၊ အလုပ်များနေလို့ပါ။")

if __name__ == '__main__':
    # ၃။ Telegram Bot Setup
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is starting...")
    app.run_polling(drop_pending_updates=True) # တစ်ခြားနေရာမှာ Run နေတာရှိရင် ဖယ်ထုတ်ပေးတယ်
