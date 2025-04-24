import logging import random import os from PIL import Image, ImageDraw, ImageFont import requests from io import BytesIO from telegram import Update from telegram.constants import ParseMode from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes from dotenv import load_dotenv

Load environment variables from .env file

load_dotenv()

Enable logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) logger = logging.getLogger(name)

Bot token from environment variables

TOKEN = os.getenv("BOT_TOKEN")

A function to create the couple image

def generate_couple_image(user1_name, user2_name, img_url): response = requests.get(img_url) img = Image.open(BytesIO(response.content)).convert("RGBA") draw = ImageDraw.Draw(img) font = ImageFont.load_default()

# Add text or shayari
shayari = "Dil se dil milte hain,\nYeh mohabbat hai apni kahani!"
draw.text((10, 10), f"Couple of the Day\n{user1_name} ❤️ {user2_name}\n\n{shayari}", font=font, fill="white")

img_path = "couple_image.png"
img.save(img_path)
return img_path

/start command

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Welcome to the Couple Bot!")

/couples command

async def couple(update: Update, context: ContextTypes.DEFAULT_TYPE): chat_id = update.message.chat_id chat_members = [await context.bot.get_chat_member(chat_id, user_id) for user_id in context.application.chat_data.get(chat_id, {}).get("users", []) if user_id != update.message.from_user.id]

if len(chat_members) < 2:
    await update.message.reply_text("Kam se kam 2 members hone chahiye! Add karne ke liye kuch log message bhejein.")
    return

user1 = random.choice(chat_members).user
user2 = random.choice([u.user for u in chat_members if u.user.id != user1.id])

background_url = "https://i.ibb.co/RGxSJ7kG/lovepik-couple-back-png-image-401205486-wh1200.png"
image_path = generate_couple_image(user1.first_name, user2.first_name, background_url)

with open(image_path, "rb") as photo:
    await update.message.reply_photo(photo=photo, caption=f"Couple of the Day: [{user1.first_name}](tg://user?id={user1.id}) ❤️ [{user2.first_name}](tg://user?id={user2.id})", parse_mode=ParseMode.MARKDOWN)

Track users who send messages

async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE): chat_id = update.message.chat_id user_id = update.message.from_user.id if not context.application.chat_data.get(chat_id): context.application.chat_data[chat_id] = {"users": set()} context.application.chat_data[chat_id]["users"].add(user_id)

Main entry point

if name == 'main': app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("couples", couple))
app.add_handler(MessageHandler(None, track_users))

app.run_polling()

