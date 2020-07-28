import discord
from discord.ext import commands
import os
import sqlite3

conn = sqlite3.connect("Members.db") #Cahnge name from Members to like Database if easier
c = conn.cursor()

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
            c.execute("SELECT count(*) FROM members")
            result = c.fetchall()
            if result[0][0] == 0: #if the table is empty
                for guild in self.client.guilds:
                    for member in guild.members:
                        for role in member.roles:
                            if role.name == roleName:
                                c.execute("INSERT INTO members VALUES (?, ?)", (str(member), startAm,))
                                conn.commit()

            else: #if not empty
                c.execute("DELETE FROM Members")
                for guild in self.client.guilds:
                    for member in guild.members:
                        for role in member.roles:
                            if role.name == roleName:
                                c.execute("INSERT INTO members VALUES (?, ?)", (str(member), startAm,))
                                conn.commit()

        c.execute("SELECT * FROM members")
        print(c.fetchall())

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stock(self, ctx, item, cost, quantity):
        itemL = item.lower()
        print(type(item), type(cost), type(int(quantity)))

        c.execute("SELECT * FROM store WHERE name=?", (itemL,))
        result = c.fetchone()
        if result[0] == itemL: #if the item exists
            change = result[2]+int(quantity)
            c.execute("UPDATE store SET price=?,amount=? WHERE name=?", (cost, change, itemL,))
            conn.commit()
        else:
            c.execute("INSERT INTO store VALUES (?, ?, ?)", (itemL, cost, quantity,))
            conn.commit()

def setup(client):
    client.add_cog(AdminCommands(client))
