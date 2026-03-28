import os
import google.generativeai as genai
from dotenv import load_dotenv

# Environment variables တွေကို load လုပ်မယ်
load_dotenv()

# Secret ထဲက key ကို ဆွဲထုတ်မယ်
api_key = os.environ.get("GEMINI_API_KEY")

# Gemini ကို configure လုပ်မယ်
genai.configure(api_key=api_key)

# Model စသုံးမယ်
model = genai.GenerativeModel("gemini-2.5-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    # ၃။ Telegram Bot Token ကို ဒီမှာထည့်ပါ (သို့မဟုတ် Secret ထဲမှာ BOT_TOKEN ဆိုပြီး ထည့်သုံးပါ)
    app = ApplicationBuilder().token("8473779952:AAGqWhA-9xYjQU0nVyGLmRPNXlQ-RSFEZag").build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
