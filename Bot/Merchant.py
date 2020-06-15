import discord
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = ".")

@client.event #Indicates bot is online
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_message(message):
    members = open("Members","w")
    if message.content.startswith('.refresh'):
        for guild in client.guilds:
            #print(guild)
            for member in guild.members:
                #print(member)
                for role in member.roles:
                    #print(role)
                    if role.name == "IRL":
                        if contains("Members",member) == False:
                            members.write(str(member))
                            members.write("\n")
                            #print(members)
def contains(file, name):
    with open(file) as f:
        if str(name) in f.read():
            return True
        return False

client.run("NzEwNTc1NzQ0MTk0OTY5NzEx.Xr2dvw.49hzjCcIh2ye9kIoJc2kQxxRO-k")
