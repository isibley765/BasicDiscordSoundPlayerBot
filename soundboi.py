import os
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

class Client(Bot):
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(client))

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        words = message.content.lower().split(" ", 1)

        if words[0].startswith('!hello'):
            await message.channel.send('Hello!')
        
        elif words[0].startswith('!play') and len(words) > 1:
            user = message.author

            if user.voice == None or user.voice.channel == None:
                await message.channel.send("I would play {}, but it seems you're not in a channel for me to play for :(".format(words[1]))
            else:
                vchannel = user.voice.channel
                if (vchannel):
                    soundfile = os.path.join(os.getcwd(), os.getenv("SOUND_FILE_PATH"), words[1]+".mp3")
                   
                    try:
                        self.vchannel = await vchannel.connect()
                    except discord.errors.ClientException:
                        pass

                    finally:
                        if self.vchannel.is_connected():
                            
                            soundLoaded = None 
                            if os.path.exists(soundfile):
                                soundLoaded = discord.FFmpegPCMAudio(soundfile)
                            else:
                                for thing in os.listdir(os.path.join(os.getcwd(), os.getenv("SOUND_FILE_PATH"))):
                                    if thing.lower().startswith(words[1]) and thing.lower().endswith(".mp3"):
                                        soundLoaded = discord.FFmpegPCMAudio(os.path.join(os.getcwd(), os.getenv("SOUND_FILE_PATH"), thing))
                                        break
                            
                            if soundLoaded is None:
                                return
                                
                            if self.vchannel.is_playing():
                                self.vchannel.stop()

                            self.vchannel.play(soundLoaded)
                else:
                    await message.channel.send("You told me to play _`{}.mp3`_ for the chat, but you don't seem to be in one :/".format(words[1], user.voice.channel))

        elif words[0].startswith('!join'):
            try:
                self.vchannel = await message.author.voice.channel.connect()
            except discord.errors.ClientException:
                await message.channel.send("Unable to join your channel :(")


if __name__ == "__main__":
    load_dotenv()
    client = Client(command_prefix="!")
    client.run(os.getenv("TOKEN"))