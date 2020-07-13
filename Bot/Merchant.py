import discord
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = ".")

@client.event #Indicates bot is online
async def on_ready():
    print("Bot is ready.")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Missing permissions.")

#resets the txt file that stores the members and their balance
@client.command()
async def refresh(ctx):
    sender = ctx.message.author
    owner = ctx.message.guild.owner

    #if ctx.message.author == ctx.message.guild.owner and ctx.message.content.startswith('.refresh'):
    if sender == owner:
        members = open("Members.txt","w")

        for guild in client.guilds:
            #print(guild)
            for member in guild.members:
                #print(member)
                for role in member.roles:
                    #print(role)

                    if role.name == "IRL":
                        if contains(members.name,member) == False:
                            members.write(str(member)+";1000;")
                            members.write("\n")
        members.close()

    #elif ctx.message.author is not ctx.message.guild.owner:
    elif sender is not owner:
        await ctx.send(f"{sender} is not owner")

#checks file for name
def contains(file, name):
    with open(file) as f:
        if str(name) in f.read():
            return True
        return False

@client.command()
@commands.has_permissions(administrator=True)
async def stock(ctx, item, cost):
    store = open("Store.txt", "a+")

#Allow a user to buy items from the store
@client.command()
async def buy(ctx, item):
    pass

##Allow a user to sell items from their iventory
@client.command()
async def sell(ctx, item):
    pass

#Allows a user to print the contents of the store, the price, and quantity
@client.command()
async def store():
    pass



client.run("NzEwNTc1NzQ0MTk0OTY5NzEx.Xua_jA.oEez1Hdn-2iiOXdspMVX10zsOs4")
