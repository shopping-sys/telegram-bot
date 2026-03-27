import os
import google.generativeai as genai  # Gemini အတွက်
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Gemini Setup လုပ်ခြင်း
# API_KEY ကို Environment Variable ထဲမှာ ထည့်ထားတာ ပိုစိတ်ချရပါတယ်
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) 
model = genai.GenerativeModel('gemini-1.5-flash') # <--- ဒီမှာ Flash ပြောင်းတာပါ

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    
    # စောင့်ဆိုင်းနေစဉ် Message ပို့ထားမယ်
    status_msg = await update.message.reply_text("🚀 Gemini Flash က အလုပ်လုပ်နေပါပြီ...")

    # Video ကို ယာယီ Download ဆွဲခြင်း
    file = await context.bot.get_file(video.file_id)
    video_path = f"{video.file_id}.mp4"
    await file.download_to_drive(video_path)

    # Gemini ဆီပို့ပြီး အသံကို စာသားပြောင်းခိုင်းခြင်း (သို့မဟုတ်) Summary လုပ်ခြင်း
    video_file = genai.upload_file(path=video_path)
    response = model.generate_content([video_file, "Please transcribe the audio or summarize this video."])

    # အဖြေပြန်ပို့ပြီး ယာယီဖိုင်ကို ဖျက်ခြင်း
    await status_msg.edit_text(response.text)
    os.remove(video_path)

# ကျန်တဲ့ main() function ကတော့ အတူတူပါပဲ
