import re
import urllib.parse
from telethon import TelegramClient, events
from telegram import Bot
import os

API_ID = int(os.environ["39570210"])
API_HASH = os.environ["cc28889230dfeb396cb141df9746857f"]
BOT_TOKEN = os.environ["8473133144:AAEiYJ4dInu_p2AcW8o6_NlcplkT9DFRVh0"]

AMAZON_TAG = "pranay0d82-21"
CUELINKS_ID = "257401"

SOURCE_CHANNELS = [
    "iamprasadtech",
    "TeluguTechworld",
    "Offerzone_deals",
    "rapiddeals_unlimited",
    "techglaredeals",
    "idoffers"
]

TARGET_CHANNEL = "@PremierOfferZone"

client = TelegramClient("session", API_ID, API_HASH)
bot = Bot(BOT_TOKEN)

def convert_links(text):
    urls = re.findall(r'https?://\S+', text)
    for url in urls:
        if "amazon." in url:
            if "tag=" not in url:
                join = "&" if "?" in url else "?"
                url_new = url + join + "tag=" + AMAZON_TAG
                text = text.replace(url, url_new)

        elif any(x in url for x in ["flipkart.", "myntra.", "ajio."]):
            encoded = urllib.parse.quote(url, safe="")
            cuelink = f"https://links.cuelinks.com/c/a?u={encoded}&id={CUELINKS_ID}"
            text = text.replace(url, cuelink)

    return text

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    if not event.text:
        return

    new_text = convert_links(event.text)
    bot.send_message(chat_id=TARGET_CHANNEL, text=new_text)

client.start()
client.run_until_disconnected()
