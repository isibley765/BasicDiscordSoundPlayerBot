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
        
        if words[0].startswith('!play') and len(words) > 1:
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
                                await message.channel.send("File {}.mp3 not found, or corrupted file".format(words[1]))
                                return
                                
                            if not soundLoaded is None:
                                if self.vchannel.is_playing():
                                    self.vchannel.stop()

                                self.vchannel.play(soundLoaded)
                else:
                    await message.channel.send("You told me to play _`{}`_ for the _`{}`_ chat, once I'm upgraded I can!".format(words[1], user.voice.channel))


if __name__ == "__main__":
    load_dotenv()
    client = Client(command_prefix="!")
    client.run(os.getenv("TOKEN"))