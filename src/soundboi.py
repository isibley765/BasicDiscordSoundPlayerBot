import logging
import os

import discord
from dotenv import load_dotenv
import traceback

from src.message_utils import join_channel, upload_attachments, show_mp3_list

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
        
        elif words[0].startswith('!play') and len(words) > 1:
            voice_connection = await join_channel(client, tchannel, vchannel)

            print("Voice connection?")
            print(f"Connected? {voice_connection.is_connected()}")

            if voice_connection and voice_connection.is_connected():
                soundfile = os.path.join(sound_files_dir, words[1]+".mp3")
                
                soundLoaded = None 
                if os.path.exists(soundfile):
                    soundLoaded = discord.FFmpegPCMAudio(soundfile)
                
                else:
                    files = [thing for thing in os.listdir(sound_files_dir)
                                if words[1] in thing and thing.lower().endswith(".mp3")]
                    files.sort()
                    if len(files) == 0:
                        await tchannel.send(
                            "I couldn't find any files containing that string? :/")
                    elif len(files) > 2:
                        files_str = "  - ".join(files)
                        await tchannel.send(
                            f"I found multiple files containing '{words[1]}', "
                            "could you be more specific?\n"
                            f"  - {files_str}")
                    else:
                        file = files[0]
                        soundLoaded = discord.FFmpegPCMAudio(os.path.join(sound_files_dir, file))
                
                # now play the sound if we found one
                if soundLoaded:
                    if voice_connection.is_playing():
                        voice_connection.stop()

                    voice_connection.play(soundLoaded)
    except Exception as e:
        await tchannel.send(f"An error occured... :/\n{e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    client.run(
        os.getenv("TOKEN"), log_handler=handler,
        log_level=logging.DEBUG)