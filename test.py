import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Test environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BOT_PREFIX = os.getenv("BOT_PREFIX")
BOT_ACTIVITY = os.getenv("BOT_ACTIVITY")

# Print environment variable statuses for testing
print("=== Environment Variable Test ===")
if DISCORD_TOKEN:
    print("DISCORD_TOKEN loaded successfully.")
else:
    print("ERROR: DISCORD_TOKEN is missing.")

if YOUTUBE_API_KEY:
    print("YOUTUBE_API_KEY loaded successfully.")
else:
    print("WARNING: YOUTUBE_API_KEY is missing. YouTube notifications may not work.")

if BOT_PREFIX:
    print(f"BOT_PREFIX: {BOT_PREFIX}")
else:
    print("WARNING: BOT_PREFIX is missing. Using default (!).")

if BOT_ACTIVITY:
    print(f"BOT_ACTIVITY: {BOT_ACTIVITY}")
else:
    print("WARNING: BOT_ACTIVITY is missing. Using default activity.")
    

