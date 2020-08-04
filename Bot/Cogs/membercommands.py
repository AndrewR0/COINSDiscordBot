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
        member = c.fetchone()
        if member != None: #check if the user sending the message is a member that can use the commands
            c.execute("SELECT name FROM store WHERE name=?", (item,))
            result = c.fetchone()
            #print(result[0])
            #2) check if the store contains the item they wish to buy
            #3) check if the quantity of the item is >0
            #4) check if the user has the necessary money
            #5) idk something else probably
        else:
            await ctx.send(f"{ctx.message.author} is not a member")


        """dict = eval(result[0])
        if not bool(dict):
            await ctx.send("There are no items in the store")

        else:
            try:
                if bool(dict[item]) and dict[item] == 0:
                    ctx.send(f"{item.upper()} is out of stock")
            except KeyError:
                ctx.send(f"{item.upper()} does not exist")
        """

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
