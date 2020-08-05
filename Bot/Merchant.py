#Database help: https://www.youtube.com/watch?v=pd-0G0MigUA&t=0s
#Cogs help: https://www.youtube.com/watch?v=vQw8cFfZPx0

import discord
from discord.ext import commands, tasks
import os
from BotToken import BotToken #file containing bot token cause I'm an idiot and keep on forgetting to not commit with the token

client = commands.Bot(command_prefix = ".")

@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    client.load_extension(f"Cogs.{extension}")

@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")

@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f"Cogs.{extension}")

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")


client.run(BotToken)
