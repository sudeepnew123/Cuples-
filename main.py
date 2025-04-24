import logging
import random
import os
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from telegram import Update, Bot, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token from environment variables
TOKEN = os.getenv("BOT_TOKEN")

# A function to create the couple image
def generate_couple_image(user1, user2, img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))

    # Add customizations
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Add text or shayari
    shayari = "Dil se dil milte hain,\nYeh mohabbat hai apni kahani!"
    draw.text((10, 10), f"Couple of the Day\n\n{shayari}", font=font, fill="white")

    # Save the final image
    img.save("couple_image.jpg")
    return "couple_image.jpg"

# /couples command to fetch random members and create an image
def couple(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    members = update.message.chat.get_members()
    
    # Select 2 random members
    member1 = random.choice(members)
    member2 = random.choice([m for m in members if m != member1])
    
    # Fetch their profile photos
    photo1 = member1['user']['photo']
    photo2 = member2['user']['photo']
    
    # Background link you provided
    background_url = "https://i.ibb.co/RGxSJ7kG/lovepik-couple-back-png-image-401205486-wh1200.png"

    # Generate the couple image
    image_path = generate_couple_image(photo1, photo2, background_url)

    # Send the final image to the group
    update.message.reply_photo(photo=open(image_path, 'rb'), caption=f"Couple of the Day: {member1['user']['username']} ❤️ {member2['user']['username']}")

# Start command to initialize the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the Couple Bot!")

# Error handling
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f"Update {update} caused error {context.error}")

def main():
    # Start the Bot
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("couples", couple))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start polling
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()