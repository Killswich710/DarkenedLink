import logging
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import cloudscraper  # For bypassing Cloudflare challenges

# Load environment variables
load_dotenv()

# Logging configuration (ensure UTF-8 encoding for emojis)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Environment Variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DISCORD_API_URL = os.getenv("DISCORD_API_URL", "https://discord.com/api/v10")
KICK_TEST_USERNAME = os.getenv("KICK_TEST_USERNAME", "example_username")  # Replace with a valid Kick username

# Validate environment variables
def validate_env_vars():
    errors = []
    if not DISCORD_TOKEN:
        errors.append("❌ DISCORD_TOKEN is missing.")
    else:
        logging.info("✅ DISCORD_TOKEN loaded successfully.")
    
    if not YOUTUBE_API_KEY:
        errors.append("❌ YOUTUBE_API_KEY is missing.")
    else:
        logging.info("✅ YOUTUBE_API_KEY loaded successfully.")

    if not errors:
        logging.info("✅ All environment variables are set.")
    else:
        for error in errors:
            logging.error(error)

# Test Discord API
def test_discord_oauth():
    logging.info("Testing Discord OAuth2...")
    logging.info(f"Requesting URL: {DISCORD_API_URL}/users/@me")
    logging.info(f"DISCORD_TOKEN: {DISCORD_TOKEN}")
    headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}
    try:
        response = requests.get(f"{DISCORD_API_URL}/users/@me", headers=headers)
        if response.status_code == 200:
            bot_info = response.json()
            logging.info(f"✅ Logged in as {bot_info['username']}#{bot_info['discriminator']}.")
        else:
            logging.error(f"❌ Discord OAuth2 Test Failed (Status Code: {response.status_code}).")
    except Exception as e:
        logging.error(f"❌ Discord OAuth2 Test encountered an error: {e}")

# Test YouTube API
def test_youtube_api():
    logging.info("Testing YouTube API...")
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Replace with a valid channel ID
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&order=date&type=video&maxResults=1&key={YOUTUBE_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "items" in data and len(data["items"]) > 0:
                video = data["items"][0]
                video_title = video["snippet"]["title"]
                logging.info(f"✅ YouTube API Test Passed. Latest video: {video_title}.")
            else:
                logging.info("✅ YouTube API Test Passed. No videos found.")
        else:
            logging.error(f"❌ Failed to fetch YouTube data (Status Code: {response.status_code}).")
    except Exception as e:
        logging.error(f"❌ YouTube API Test encountered an error: {e}")

# Test Kick Web Scraping
def test_kick_scraping():
    logging.info("Testing Kick Web Scraping...")
    url = f"https://kick.com/{KICK_TEST_USERNAME}"
    logging.info(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://kick.com/",
    }
    scraper = cloudscraper.create_scraper()

    try:
        response = scraper.get(url, headers=headers)
        logging.info(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            live_indicator = soup.find("span", text="LIVE")
            if live_indicator:
                logging.info(f"✅ {KICK_TEST_USERNAME} is live on Kick.")
                print(f"✅ {KICK_TEST_USERNAME} is live on Kick.")
            else:
                logging.info(f"✅ {KICK_TEST_USERNAME} is not live on Kick.")
                print(f"✅ {KICK_TEST_USERNAME} is not live on Kick.")
        else:
            logging.error(f"❌ Failed to fetch Kick data (Status Code: {response.status_code}).")
            print(f"❌ Failed to fetch Kick data (Status Code: {response.status_code}).")
            if response.status_code == 403:
                logging.error(f"❌ Failed to fetch Kick data (Status Code: {response.status_code}).")
            logging.info(f"Response Headers: {response.headers}")
            logging.info(f"Response Text: {response.text[:500]}")  # Log the first 500 characters of the response

    except Exception as e:
        logging.error(f"❌ An error occurred: {e}")
        print(f"❌ An error occurred: {e}")
        
# Run all tests
if __name__ == "__main__":
    print("=== Starting Tests ===")
    logging.info("=== Starting Tests ===")
    validate_env_vars()
    test_discord_oauth()
    test_youtube_api()
    # test_kick_scraping()
    print("=== All Tests Completed ===")
    logging.info("=== All Tests Completed ===")







    

