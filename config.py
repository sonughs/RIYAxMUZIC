import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", "")

#Youtube Api Url
API_URL = getenv("API_URL", "")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", "")

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 5256000))
# ~10 years in minutes (practically unlimited)

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", ""))

# Get this value from @Hot_Girl_Robot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", "5960968099"))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/TeamOpus/Lv2",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "mainr")
GIT_TOKEN = getenv(
    "GIT_TOKEN"
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL") or "https://t.me/GirlsSwappingIndia"
SUPPORT_CHAT = getenv("SUPPORT_CHAT") or "https://t.me/gsiking"

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "2d3fd5ccdd3d43dda6f17864d8eb7281")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "48d311d8910a4531ae81205e1f754d27")


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 450))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 53687091200))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 53687091200))
# 50 GB = 53,687,091,200 bytes

# Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = getenv(
    "START_IMG_URL", "https://envs.sh/vsN.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://graph.org/file/9077cd2ba5818efef2d28.jpg"
)
PLAYLIST_IMG_URL = "https://graph.org/file/eb1e2b58e17964083db73.jpg"
STATS_IMG_URL = "https://graph.org/file/3e1a29249c83104c035af.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org/file/ebc1cd4853f51d4fd7cdb.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/948c175c8bfb3d96080ad.jpg"
STREAM_IMG_URL = "https://graph.org/file/e8311d4fff8527c550185.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/e8311d4fff8527c550185.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/e8311d4fff8527c550185.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://graph.org/file/e8311d4fff8527c550185.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://graph.org/file/e8311d4fff8527c550185.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://graph.org/file/e8311d4fff8527c550185.jpg"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
