from sys import path

path.insert(0, "./src")

import discord
from config import Config
from time import sleep


class Client(discord.Client):
    async def on_ready(self):
        print("Ready!")

    async def on_message(self, message):

        if message.content == ".start":
            Config.reload()
            await message.channel.send("Testing all commands...")

            commands = Config.COMMANDS["commands"]
            for cmd in commands:
                if "command" in cmd:
                    text = f'{Config.PREFIX}{cmd["command"]}'
                    if "args" in cmd:
                        text += f' {" ".join(cmd["args"])}'

                    await message.channel.send(text)

                if "say" in cmd:
                    await message.channel.send(cmd["say"])

                if "delay" in cmd:
                    sleep(cmd["delay"])

            await message.channel.send("Done.")


bot = Client()
bot.run(Config.DISCORD_TOKEN)
