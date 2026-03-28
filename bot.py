import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ၁။ Gemini API Key (Key အသစ်ယူထားရင် ပိုကောင်းပါတယ်)
genai.configure(api_key="AizasyAp54QILRrcmZlx0R13ber47wtEniykDYA")
model = genai.GenerativeModel("gemini-1.5-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update or not update.message or not update.message.text:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Safety settings မပါဘဲ အရှင်းဆုံး စမ်းသပ်ပါမည်
        response = model.generate_content(update.message.text)
        
        if response and response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Gemini က စာသား ပြန်မထုတ်ပေးနိုင်ပါဘူး။")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    # ၂။ ဤနေရာတွင် @BotFather ထံမှရသော TOKEN အသစ်ကို ထည့်ပါ
    TOKEN = "8734152863:AAFNZWBpwHpzFNN3LPwar9VI7aijq8gs5jA"
    
    # Bot Application တည်ဆောက်ခြင်း
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Message များကို လက်ခံရန် Handler ထည့်ခြင်း
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling(drop_pending_updates=True)
