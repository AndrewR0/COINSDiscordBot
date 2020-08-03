import discord
from discord.ext import commands
import sqlite3
import os


conn = sqlite3.connect("Data.db")
c = conn.cursor()

#bank table stores the members' id, balance, and items
#store table stores items' name, cost, and quantity

class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def exit(self, ctx):
        conn.close()
        await self.client.logout()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def refresh(self, ctx, roleName, startAm=1000):
        sender = ctx.message.author
        owner = ctx.message.guild.owner
        if sender == owner:

            c.execute("SELECT count(*) FROM bank")
            count = c.fetchall()
            if count[0][0] == 0:
                for guild in self.client.guilds:
                    for member in guild.members:
                        for role in member.roles:
                            if role.name == roleName:
                                c.execute("INSERT INTO bank VALUES (?,?,?)", (member.id, startAm, '{}',))
                                conn.commit()

            else: #if not empty
                c.execute("DELETE FROM bank")
                for guild in self.client.guilds:
                    for member in guild.members:
                        for role in member.roles:
                            if role.name == roleName:
                                c.execute("INSERT INTO bank VALUES (?,?,?)", (member.id, startAm, '{}',))
                                conn.commit()

        c.execute("SELECT * FROM bank")
        print(c.fetchall())

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stock(self, ctx, item, cost, quantity):
        itemL = item.lower()
        #print(type(item), type(cost), type(int(quantity)))

        c.execute("SELECT * FROM store WHERE name=?", (itemL,))
        result = c.fetchone()
        if result != None: #if the item exists
            change = result[2]+int(quantity)
            c.execute("UPDATE store SET price=?,amount=? WHERE name=?", (cost, change, itemL,))
            conn.commit()
            await ctx.send(f"{quantity} {item.upper()} has been added for Å{cost} each")
            c.execute("INSERT INTO store VALUES (?, ?, ?)", (itemL, cost, quantity,))
            conn.commit()
            await ctx.send(f"{quantity} {item.upper()} has been added for Å{cost} each")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unstock(self, ctx, item):
        itemL = item.lower()

        c.execute("SELECT * FROM store WHERE name=?", (itemL,))
        result = c.fetchone()
        if result != None: #if the item exists
            c.execute("DELETE FROM store WHERE name=?", (itemL,))
            conn.commit()
            await ctx.send(f"{item.upper()} has been removed")
        else:
            await ctx.send("No such item is stocked")

def setup(client):
    client.add_cog(AdminCommands(client))
