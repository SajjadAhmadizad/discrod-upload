import os
import json
import requests
import discord
import pika
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client:discord.Client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


def send_to_discord(data:dict):
    channel_id = os.getenv("CHANNEL_ID")
    bot_token = os.getenv("DISCORD_TOKEN")
    headers = {
        'Authorization': f'Bot {bot_token}',
        'Content-Type': 'application/json'
    }
    url = f'https://discord.com/api/v10/channels/{channel_id}/messages'


    data = {'content': f"```json\n{json.dumps(data)}\n```"}
    
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200
    # channel = client.get_channel(channel_id)

    # json_str = json.dumps(data)

    # THIS is a async function :(
    
    # channel.send(f"```json\n{data}\n```")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message)

    await message.channel.send('Hello!')

async def send_file_to_discord(json_data):
    print(f"client : {client}")
    channel_id = int(os.getenv("CHANNEL_ID"))
    channel = await client.fetch_channel(channel_id)

    
    json_str = json.dumps(json_data, indent=4)
    await channel.send(f"```json\n{json_str}\n```") 
