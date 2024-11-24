import logging
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("darkenedlink.log"),
        logging.StreamHandler()
    ]
)

# Environment Variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_API_URL = os.getenv("DISCORD_API_URL", "https://discord.com/api/v10")
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
BOT_ACTIVITY = os.getenv("BOT_ACTIVITY", "DarkenedLink Bot is live and monitoring!")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Validate DISCORD_TOKEN
if not DISCORD_TOKEN:
    logging.error("DISCORD_TOKEN is missing from .env file!")
    raise ValueError("DISCORD_TOKEN is missing from .env file!")

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# ---- Discord API Command ----
@bot.command(name="discord_info")
async def discord_info(ctx):
    """Fetch and display bot information from the Discord API."""
    headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}
    response = requests.get(f"{DISCORD_API_URL}/users/@me", headers=headers)
    if response.status_code == 200:
        bot_info = response.json()
        await ctx.send(f"Logged in as {bot_info['username']}#{bot_info['discriminator']}")
        logging.info(f"Discord API: Successfully fetched bot info for {bot_info['username']}.")
    else:
        await ctx.send(f"Failed to fetch bot info (Status Code: {response.status_code}).")
        logging.error(f"Discord API Error: Status Code {response.status_code} - {response.text}")

# ---- YouTube Integration ----
@bot.command(name="notify_youtube")
async def notify_youtube(ctx, channel_id: str):
    """Fetch the latest video from a YouTube channel."""
    if not YOUTUBE_API_KEY:
        await ctx.send("YouTube API key is missing in the configuration.")
        logging.error("YouTube API Error: Missing API key.")
        return

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&order=date&type=video&maxResults=1&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            video = data["items"][0]
            video_title = video["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
            await ctx.send(f"Latest video: {video_title}\n{video_url}")
            logging.info(f"YouTube API: Fetched latest video - {video_title}.")
        else:
            await ctx.send("No videos found for this channel.")
            logging.warning("YouTube API: No videos found for the given channel.")
    else:
        await ctx.send(f"Failed to fetch YouTube data (Status Code: {response.status_code}).")
        logging.error(f"YouTube API Error: Status Code {response.status_code} - {response.text}")

# ---- Bot Events ----
@bot.event
async def on_ready():
    """Event triggered when the bot logs in."""
    logging.info(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(BOT_ACTIVITY))

# ---- Run the Bot ----
if __name__ == "__main__":
    logging.info("=== Starting DarkenedLink Bot ===")
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logging.critical(f"Bot failed to start: {e}")



