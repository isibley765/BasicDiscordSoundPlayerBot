import logging
import os

import discord
from dotenv import load_dotenv
import traceback

load_dotenv()
sound_files_dir = os.path.join(os.getcwd(), os.getenv("SOUND_FILE_PATH"))

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(
    intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    user = message.author
    text = message.content
    attachments = message.attachments
    words = message.content.lower().split(" ", 1)

    try:
        if words[0].startswith('!hello'):
            await message.channel.send('Hello!')

        elif words[0].startswith('!upload'):
            print("Uploading...")
            if len(attachments) == 0:
                await message.channel.send("Your nothing upload has been saved to '/dev/null'!\nRude...")
            else:
                for attachment in attachments:
                    filename = attachment.filename.lower().replace(" ", "_")
                    if filename.endswith(".mp3"):
                        filepath = os.path.join(sound_files_dir, filename)
                        with open(filepath, "wb") as fp:
                            fp.write(await attachment.read())
                        await message.channel.send(
                            f"'{attachment.filename}' was hopefully uploaded?")
                    else:
                        await message.channel.send(
                            f"Uh oh... '{attachment.filename}' wasn't an MP3? I'm picky :/\npls convert?")

        elif words[0].startswith('!list'):
            files = [file for file in os.listdir(sound_files_dir)
                if file.lower().endswith(".mp3")]
            if len(files):
                files_list = "\n  - ".join(files)
                await message.channel.send(
                    f"I see these files:\n  - {files_list}")
            else:
                await message.channel.send(
                    f"Head empty... no thoughts... :(")
        
        elif words[0].startswith('!join'):
            try:
                await message.author.voice.channel.connect(reconnect=True)
            except discord.errors.ClientException:
                await message.channel.send("Unable to join your channel :(")

        elif words[0].startswith('!play') and len(words) > 1:
            if user.voice == None or user.voice.channel == None:
                await message.channel.send("I would play {}, but it seems you're not in a channel for me to play for :(".format(words[1]))
            else:
                vchannel = user.voice.channel
                if (vchannel):
                    soundfile = os.path.join(sound_files_dir, words[1]+".mp3")
                    
                    try:
                        voice_connection = await vchannel.connect(reconnect=True)
                    except discord.errors.ClientException:
                        await message.channel.send("Unable to join your channel :(")

                    finally:
                        if voice_connection.is_connected():
                            
                            soundLoaded = None 
                            if os.path.exists(soundfile):
                                soundLoaded = discord.FFmpegPCMAudio(soundfile)
                            else:
                                files = [thing for thing in os.listdir(sound_files_dir)
                                         if words[1] in thing and thing.lower().endswith(".mp3")]
                                files.sort()
                                if len(files) == 0:
                                    await message.channel.send(
                                        "I couldn't find any files containing that string? :/")
                                elif len(files) > 2:
                                    files_str = "  - ".join(files)
                                    await message.channel.send(
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
                else:
                    await message.channel.send("You told me to play _`{}.mp3`_ for the chat, but you don't seem to be in one :/".format(words[1], user.voice.channel))
    except Exception as e:
        await message.channel.send(f"An error occured... :/\n{e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    client.run(
        os.getenv("TOKEN"), log_handler=handler,
        log_level=logging.DEBUG)