import discord
from discord.ext import commands, tasks
import itertools
import json

client = commands.Bot(command_prefix = ".")

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
    storeContents = open("Store.json", "a+")
    storeList = []
    with open(storeContents.name, "a+") as f:
        jsonObject = json.dumps({"Item": item, "Cost": cost, "Quantity": quantity}, indent=3)
        f.write(jsonObject)
        #json.dump({"Item": item, "Cost": cost, "Quantity": quantity}, f)
        f.write("\n")
        '''
        #appends the data from the json file into a list
        for line in f:
            storeList.append(json.loads(line))

        #checks for already exisiting items in the store
        for index in range(len(storeList)):
            if storeList[index].get("Item") == item.lower():
                storeList[index].update({"Cost": cost})
                storeList[index].update({"Quantity": str(int(storeList[index].get("Quantity"))+int(quantity))})
                print(storeList[index])
        '''
        storeContents.close()

    '''
    storeContents = open("Store.txt", "a+")

    with open(storeContents.name, "r") as f:
        check = False
        for line in f:
            spliting = line.split(";")
            print(spliting)

            if line[0] != item:
                check = False
            else:
                line[1] = str(cost)
                line[2] = str(int(line[2]) + quantity)
                check == True
        if check == False:
            storeContents.write(f"{str(item)};{str(cost)};{str(quantity)}\n")

    storeContents.close()
    await ctx.send(f"{quantity} {item} has been added to the store for ☭{cost}")
    '''
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


client.run("NzEwNTc1NzQ0MTk0OTY5NzEx.Xw0B5Q.2aF8CXKAaQMmS52UsBQlS3KXC0s")
