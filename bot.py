import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Setup Gemini
genai.configure(api_key="မင်းရဲ့_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    if not video: return

    wait_msg = await update.message.reply_text("⏳ Gemini က Video ကို စစ်ဆေးနေပါတယ်...")

    # Video ကို Download ဆွဲခြင်း
    file = await context.bot.get_file(video.file_id)
    video_path = f"{video.file_id}.mp4"
    await file.download_to_drive(video_path)

    # Gemini ဆီသို့ Video ပို့ပြီး Transcript တောင်းခြင်း
    sample_file = genai.upload_file(path=video_path)
    response = model.generate_content([sample_file, "Summarize this video or transcribe the audio."])

    # အဖြေပြန်ပို့ခြင်း
    await wait_msg.edit_text(response.text)
    
    # ဖိုင်ပြန်ဖျက်ခြင်း (Storage မပြည့်အောင်)
    os.remove(video_path)

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.run_polling() 
