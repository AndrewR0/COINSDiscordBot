import discord
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = ".")

@client.event #Indicates bot is online
async def on_ready():
    print("Bot is ready.")

@client.command()
async def refresh(ctx):
    sender = ctx.message.author
    owner = ctx.message.guild.owner

    #if ctx.message.author == ctx.message.guild.owner and ctx.message.content.startswith('.refresh'):
    if sender == owner and ctx.message.content.startswith('.refresh'):
        members = open("Members.txt","a+")

        for guild in client.guilds:
            print(guild)
            for member in guild.members:
                print(member)
                for role in member.roles:
                    print(role)
                    if role.name == "IRL":
                        if contains(members.name,member) == False:
                            members.write(str(member))
                            members.write("\n")
        members.close()

    #elif ctx.message.author is not ctx.message.guild.owner:
    elif sender is not owner:
        await ctx.send(f"{sender} is not owner")

def contains(file, name):
    with open(file) as f:
        if str(name) in f.read():
            return True
        return False



client.run("INSERT BOT TOKEN HERE")
