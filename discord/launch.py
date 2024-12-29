import os
from discord_manager import client
from queue_listener import MessageListener
from dotenv import load_dotenv
# ==========
import time
time.sleep(15)
# ==========

# load_dotenv()
bot_token = os.getenv("DISCORD_TOKEN")

td = MessageListener()
td.start()

client.run(bot_token)
