import discord
from discord.ext import commands
import sqlite3
import os

conn = sqlite3.connect("Data.db")
c = conn.cursor()

class MemberCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def buy(self, ctx, item, quantity=1):
        senderID = ctx.message.author.id
        #print(senderID)
        c.execute("SELECT id FROM bank WHERE id=?", (senderID,))
        member = c.fetchone() #member id in database

        if member != None: #check if the user sending the message is a member that can use the commands
            c.execute("SELECT name FROM store WHERE name=?", (item,))
            itemName = c.fetchone() #item name in database

            if itemName != None: #check if the store contains the item they wish to buy
                c.execute("SELECT quantity FROM store WHERE name=?", (item,))
                quant = c.fetchone() #quantity of item in database

                if quantity <= quant[0] and quantity > 0: #check if the quantity of the item is >0
                    c.execute("SELECT balance FROM bank WHERE id=?", (senderID,))
                    bal = c.fetchone() #balance of member trying to buy item
                    c.execute("SELECT price FROM store WHERE name=?", (item,))
                    cost = c.fetchone() #cost of individual item member is trying to buy
                    c.execute("SELECT items FROM bank WHERE id=?", (senderID,))
                    itemStr = c.fetchone() #string of item dictionary
                    itemDict = eval(itemStr[0]) #dictionary of items member owns

                    if quantity*cost[0] <= bal[0]: #check if the user has the necessary money
                        if item in itemDict:
                            itemDict[item] += quantity
                        else:
                            itemDict.update({item:quantity})

                        balChange = bal[0]-(quantity*cost[0])
                        quantChange = quant[0]-quantity
                        c.execute("UPDATE bank SET balance=?,items=?  WHERE id=?", (balChange,str(itemDict),senderID,))
                        conn.commit()
                        c.execute("UPDATE store SET quantity=? WHERE name=?", (quantChange, item,))
                        conn.commit()
                        print("Updated")
                    else:
                        await ctx.send("Insufficient funds")
                else:
                    await ctx.send("Invalid number of item")
            else:
                await ctx.send(f"{item.upper()} is not stocked")
        else:
            await ctx.send(f"{ctx.message.author} is not a member")


    ##Allow a user to sell items from their iventory
    @commands.command()
    async def sell(self, ctx, item, quantity=1):
        pass

    #Allows a user to print the contents of the store, the price, and quantity
    @commands.command()
    async def store(self):
        pass

def setup(client):
    client.add_cog(MemberCommands(client))
