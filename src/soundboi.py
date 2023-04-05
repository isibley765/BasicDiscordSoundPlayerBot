import logging
import os

import discord
from dotenv import load_dotenv
import traceback

from src.message_utils import (
    join_channel,
    leave_channels,
    upload_attachments,
    show_mp3_list,
    play_sound,
)

load_dotenv()
sound_files_dir = os.path.join(os.getcwd(), os.getenv("SOUND_FILE_PATH"))
os.makedirs(sound_files_dir, exist_ok=True)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(
    intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    
    user = message.author
    vchannel = user.voice.channel
    tchannel = message.channel
    text = message.content
    attachments = message.attachments
    words = text.lower().split(" ", 1)

    try:
        if words[0].startswith('!hello'):
            await tchannel.send('Hello!')

        elif words[0].startswith('!upload'):
            await upload_attachments(tchannel, attachments)

        elif words[0].startswith('!list'):
            await show_mp3_list(tchannel)
        
        elif words[0].startswith('!join'):
            await join_channel(client, tchannel, vchannel)
        
        elif words[0].startswith('!leave') or words[0].startswith('!bye'):
            await leave_channels(client)
        
        elif words[0].startswith('!play') and len(words) > 1:
            await play_sound(client, words[1], tchannel, vchannel)
        
    except Exception as e:
        await tchannel.send(f"An error occured... :/\n{e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    client.run(
        os.getenv("TOKEN"), log_handler=handler,
        log_level=logging.DEBUG)