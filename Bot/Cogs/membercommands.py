import discord
from discord.ext import commands
import os

class MemberCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def buy(self, ctx, item):
        pass

    ##Allow a user to sell items from their iventory
    @commands.command()
    async def sell(self, ctx, item):
        pass

    #Allows a user to print the contents of the store, the price, and quantity
    @commands.command()
    async def store(self):
        pass

def setup(client):
    client.add_cog(MemberCommands(client))
