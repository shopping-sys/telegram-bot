import os
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ၁။ API Key (ဒီနေရာမှာ ကိုယ့် Key ကို တိုက်ရိုက်ထည့်တာ ပိုသေချာပါတယ်)
API_KEY = "မင်းရဲ့_GEMINI_API_KEY_ဒီမှာထည့်" 
client = genai.Client(api_key=API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # စာသား မဟုတ်ရင် ပြန်ထွက်မယ်
    if not update.message.text: return
    
    # User ကို ခဏစောင့်ခိုင်းမယ်
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # ၂။ Gemini ဆီက အဖြေတောင်းခြင်း
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=update.message.text
        )
        
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Gemini က အဖြေမပေးနိုင်ပါဘူး။")
            
    except Exception as e:
        # Error အစစ်ကို Telegram မှာ မြင်ရအောင် လုပ်ထားပါတယ်
        await update.message.reply_text(f"Error တက်သွားပါတယ်: {str(e)}")

if __name__ == '__main__':
    # ၃။ Telegram Token
    TOKEN = "မင်းရဲ့_TELEGRAM_BOT_TOKEN_ဒီမှာထည့်"
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot စတင်လည်ပတ်ပါပြီ...")
    # drop_pending_updates က အရင်က ပိတ်မိနေတဲ့ message တွေကို ရှင်းထုတ်ပေးတယ်
    app.run_polling(drop_pending_updates=True)
