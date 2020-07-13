import discord
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = ".")
storeContents = open("Store.txt", "w")

@client.event #Indicates bot is online
async def on_ready():
    print("Bot is ready.")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
'''
@client.event
async def on_command_error(ctx, error):
    await ctx.send("Some error occured.")
    print(error)
'''
#resets the txt file that stores the members and their balance
@client.command()
async def refresh(ctx):
    sender = ctx.message.author
    owner = ctx.message.guild.owner

    #if ctx.message.author == ctx.message.guild.owner and ctx.message.content.startswith('.refresh'):
    if sender == owner:
        members = open("Members.txt","w")
        print(members.name)

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

#Allows an admin to add an item(s) to the store
@client.command()
@commands.has_permissions(administrator=True)
async def stock(ctx, item, cost, quantity):
    if contains(storeContents.name,item) == False:
        storeContents.write(f"{str(item)};{str(cost)};{str(quantity)}")
    storeContents.close()
    await ctx.send(f"{quantity} {item} has been added to the store for {cost} currency")

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


client.run("NzEwNTc1NzQ0MTk0OTY5NzEx.XwvVGw.JGGcUS4qRlYc3N_YX9ySUTwu7m4")
