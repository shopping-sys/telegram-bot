import os
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from faster_whisper import WhisperModel

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

model = WhisperModel("base")  # small / medium / large

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video

    if not video:
        await update.message.reply_text("Video မတွေ့ဘူး")
        return

    await update.message.reply_text("📥 Video download လုပ်နေတယ်...")

    file = await context.bot.get_file(video.file_id)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        await file.download_to_drive(temp_video.name)
        video_path = temp_video.name

    await update.message.reply_text("🎧 Audio → Subtitle ပြောင်းနေတယ်...")

    segments, _ = model.transcribe(video_path)

    subtitle_text = ""
    for segment in segments:
        start = int(segment.start)
        end = int(segment.end)
        subtitle_text += f"[{start}s - {end}s]\n{segment.text}\n\n"

    await update.message.reply_text(subtitle_text[:4000])  # Telegram limit

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.VIDEO, handle_video))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
