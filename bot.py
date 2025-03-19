import discord
import requests
import random
import os
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv("TOKEN")
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

# Setting up intents and client
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

# Run the bot
client.run(TOKEN)
