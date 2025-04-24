import logging
import random
import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token from environment variables
TOKEN = os.getenv("BOT_TOKEN")

# In-memory active users store
active_users = set()

# A function to create the couple image
def generate_couple_image(user1_name, user2_name, img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Add text or shayari
    shayari = "Dil se dil milte hain,\nYeh mohabbat hai apni kahani!"
    draw.text((10, 10), f"Couple of the Day\n{user1_name} ❤️ {user2_name}\n\n{shayari}", font=font, fill="white")

    img_path = "couple_image.png"
    img.save(img_path)
    return img_path

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Couple Bot!")

# /couples command
async def couple(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(active_users) < 2:
        await update.message.reply_text("Kam se kam 2 active users hone chahiye! Chat me thoda message bhej bhai log.")
        return

    user_ids = list(active_users)
    user1_id, user2_id = random.sample(user_ids, 2)

    user1 = await context.bot.get_chat_member(update.effective_chat.id, user1_id)
    user2 = await context.bot.get_chat_member(update.effective_chat.id, user2_id)

    background_url = "https://i.ibb.co/RGxSJ7kG/lovepik-couple-back-png-image-401205486-wh1200.png"
    image_path = generate_couple_image(user1.user.first_name, user2.user.first_name, background_url)

    with open(image_path, "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=f"❤️ Couple of the Day:\n[{user1.user.first_name}](tg://user?id={user1.user.id}) + [{user2.user.first_name}](tg://user?id={user2.user.id}) ❤️",
            parse_mode=ParseMode.MARKDOWN
        )

# Track active users
async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        user_id = update.message.from_user.id
        active_users.add(user_id)

# Main bot startup
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("couples", couple))
    app.add_handler(MessageHandler(None, track_users))

    app.run_polling()
  
