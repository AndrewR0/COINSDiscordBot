#Database help: https://www.youtube.com/watch?v=pd-0G0MigUA&t=0s


import discord
from discord.ext import commands, tasks
import json
import os

client = commands.Bot(command_prefix = ".")

"""@client.event #Indicates bot is online
async def on_ready():
    if os.path.isfile("Store.json") == False:
        store = open("Store.json", "w")
        print(os.stat("Store.json").st_size)
        print(f"{store.name} created")
    print("Bot is ready.")"""

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

"""@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)"""

'''
@client.event
async def on_command_error(ctx, error):
    await ctx.send("Some error occured.")
    print(error)
'''

"""@client.command()
async def exit(ctx):
    await client.logout()"""

#resets the txt file that stores the members and their balance
"""@client.command()
async def refresh(ctx):
    sender = ctx.message.author
    owner = ctx.message.guild.owner
    if sender == owner:
        members = open("Members.json","w")
        #print(members.name)

        for guild in client.guilds:
            for member in guild.members:
                for role in member.roles:
                    if role.name == "IRL":
                        with open(members.name, "a+") as f:
                            jsonObject = json.dumps({"Name": str(member), "Wallet": "1000"}, indent=2)
                            f.write(jsonObject)
                            f.write("\n")
                            members.close()
    elif sender is not owner:
        await ctx.send(f"{sender} is not owner")"""

#THIS ENTIRE FUCKING METHOD DOESNT WORK HOW IT SHOULD, TEST FORMATTING THE FILE ON START AND FIRST ITEM INPUT IS CORRECT, FIGURE OUT
#HOW TO WRITE BACK INTO THE JSON FILE AFTER CHANGES ARE MADE TO THE LOCAL DICT THAT STORES THE CONTENTS, AND THEN BE ABLE TO INPUT
#NEW ITEMS
"""@client.command()
@commands.has_permissions(administrator=True)
async def stock(ctx, item, cost, quantity):

    print(os.stat("Store.json").st_size)

    if os.stat("Store.json").st_size == 0:
        print("check")

        store = open("Store.json", "w")
        jsonObject = json.dumps({item:[{"Cost": cost, "Quantity": quantity}]}, indent=3)
        store.write(jsonObject)
        store.close()
    else:
        store = open("Store.json", "r+")
        data = json.load(store)
        if item in data:
            #val = data.get(item)[0].get("Cost")
            #quant = data.get(item)[0].get("Quantity")
            #print(val, quant)

            with open("Store.json", "w") as f:
                print(f"old {data}")
                dict = data.get(item)[0]
                dict2 = {"Cost": cost, "Quantity": str(int(data.get(item)[0].get("Quantity")) + int(quantity))}
                print(data.get(item)[0])
                z = dict.update(dict2)
                print(f"new {data}")
                json.dumps(data)
                store.close()
        else:
            data[item] = [{"Cost": cost, "Quantity": quantity}]
            json.dumps(data)
            store.close()"""


"""#Allow a user to buy items from the store
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
    pass"""


client.run("NzEwNTc1NzQ0MTk0OTY5NzEx.Xr2dOw.SDKP0Cjvc1rUXavHdIBFBicUFsQ")
