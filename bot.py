import discord
import requests
import random
import os
from dotenv import load_dotenv
import threading
from flask import Flask

# Load environment variables from .env file
load_dotenv()

# Get the TOKEN from the environment variables
TOKEN = os.getenv("TOKEN")  # Ensure you have your token in the .env file

R34_API_URL = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags={tag}"

def get_r34_image(tag):
    try:
        # Format the URL with the provided tag
        url = R34_API_URL.format(tag=tag)
        response = requests.get(url)
        response.raise_for_status()  # Check for errors in the request

        # Parse the JSON response
        data = response.json()

        # If the response is valid and contains posts, return a random image URL
        if data and isinstance(data, list):
            image = random.choice(data)
            return image.get("file_url", "❌ No image found.")
        return "❌ No image found."

    except requests.exceptions.RequestException as e:
        return f"❌ Error fetching data: {e}"

# Setting up Flask to run alongside the Discord bot
app = Flask(__name__)

@app.route('/')
def index():
    return "Discord Bot is running!"

# Function to run Flask in a separate thread
def run_flask():
    app.run(host='0.0.0.0', port=10000)  # Flask will run on port 10000

# Setting up intents and client for Discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!"):
        # Extract the tag from the message
        tag = message.content[1:].strip().replace(" ", "_")  # Convert command to tag format
        image_url = get_r34_image(tag)
        await message.channel.send(image_url)

# Run Flask in a separate thread so it doesn't block the bot
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Run the Discord bot
client.run(TOKEN)
