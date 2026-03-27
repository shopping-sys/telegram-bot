import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import google.generativeai as genai
import subprocess

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Video → Audio extract
def extract_audio(video_path, audio_path):
    subprocess.run([
        "ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path
    ])

# Fake speech-to-text (later upgrade to Whisper)
def speech_to_text(audio_path):
    return "This is sample extracted speech from video"

# Gemini translate
def translate_text(text):
    prompt = f"Translate this into Myanmar:\n{text}"
    response = model.generate_content(prompt)
    return response.text

# Handle video
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.video.get_file()
    video_path = "video.mp4"
    audio_path = "audio.mp3"

    await file.download_to_drive(video_path)

    extract_audio(video_path, audio_path)

    text = speech_to_text(audio_path)
    mm_text = translate_text(text)

    await update.message.reply_text(mm_text)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(MessageHandler(filters.VIDEO, handle_video))

print("Bot running...")
app.run_polling()
