import os

import discord
from dotenv import load_dotenv
from typing import List, Union

load_dotenv()
sound_files_dir = os.path.join(os.getcwd(), os.getenv("SOUND_FILE_PATH"))
os.makedirs(sound_files_dir, exist_ok=True)


async def upload_attachments(tchannel: discord.TextChannel, attachments: List[discord.Attachment]) -> None:
    if len(attachments) == 0:
        await tchannel.send("Your nothing upload has been saved to '/dev/null'!\nRude...")
    else:
        for attachment in attachments:
            filename = attachment.filename.lower().replace(" ", "_")
            if filename.endswith(".mp3"):
                filepath = os.path.join(sound_files_dir, filename)
                with open(filepath, "wb") as fp:
                    fp.write(await attachment.read())
                await tchannel.send(
                    f"'{attachment.filename}' was hopefully uploaded?")
            else:
                await tchannel.send(
                    f"Uh oh... '{attachment.filename}' wasn't an MP3? I'm picky :/\npls convert?")

async def show_mp3_list(tchannel: discord.TextChannel) -> None:
    files = [file for file in os.listdir(sound_files_dir)
        if file.lower().endswith(".mp3")]
    if len(files):
        files_list = "\n  - ".join(files)
        await tchannel.send(
            f"I see these files:\n  - {files_list}")
    else:
        await tchannel.send(
            f"Head empty... no thoughts... :(")

async def join_channel(client: discord.Client, tchannel: discord.TextChannel, vchannel: discord.VoiceChannel) -> Union[None, discord.VoiceClient]:
    voice_client = None
    if vchannel is not None:
        for vclient in client.voice_clients:
            if vclient.channel != vchannel and vclient.is_connected():
                vclient.disconnect()
        
            elif vclient.channel == vchannel:
                voice_client = vclient

        # if we're still None, we're not connected already -- try to connect anew
        if voice_client is None:
            try:
                voice_client = await vchannel.connect(reconnect=True)
            except discord.errors.ClientException:
                await tchannel.send("Unable to join your channel :(")
                raise
            except Exception as e:
                await tchannel.send("Issue joining your channel? ヽ(ຈل͜ຈ)ﾉ︵ ┻━┻")
                raise
        
    else:
        await tchannel.send("Unable to join your channel! You're not in one?")

    return voice_client