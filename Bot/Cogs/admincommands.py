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

    @commands.command(aliases=['add'])
    @commands.has_permissions(administrator=True)
    async def addMember(self, ctx, id, startAm=1000):
        member = id[3:-1]

        c.execute("SELECT id FROM bank WHERE id=?", (member,))
        check = c.fetchone()

        if check == None:
            c.execute("INSERT INTO bank VALUES (?,?,?)", (member, startAm, '{}',))
            conn.commit()
            print(f"adding {id[3:-1]}")
            await ctx.send(f"{id} has been added")
        else:
            await ctx.send(f"{id} is already a member")

    @commands.command(aliases=['remove'])
    @commands.has_permissions(administrator=True)
    async def removeMember(self, ctx, id):
        member = id[3:-1]

        c.execute("SELECT id FROM bank WHERE id=?", (member,))
        check = c.fetchone()

        if check != None:
            c.execute("DELETE FROM bank WHERE id=?", (member,))
            conn.commit()
            print(f"removing {id[3:-1]}")
            await ctx.send(f"{id} has been removed")
        else:
            await ctx.send(f"{id} is not a member")

    @commands.command(aliases=['add$'])
    @commands.has_permissions(administrator=True)
    async def addMoney(self, ctx, id, amount):
        member = id[3:-1]

        c.execute("SELECT id FROM bank WHERE id=?", (member,))
        check = c.fetchone()

        if check != None:
            c.execute("SELECT balance FROM bank WHERE id=?", (member,))
            bal = c.fetchone()

            balChange = bal[0]+int(amount)
            c.execute("UPDATE bank SET balance=? WHERE id=?", (balChange,member,))
            conn.commit()
            print(f"adding money to {id[3:-1]}")
        else:
            await ctx.send(f"{id} is not a member")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stock(self, ctx, item, cost, quantity):
        itemL = item.lower()
        #print(type(item), type(cost), type(int(quantity)))

        c.execute("SELECT * FROM store WHERE name=?", (itemL,))
        result = c.fetchone()
        if result != None: #if the item exists
            change = result[2]+int(quantity)
            c.execute("UPDATE store SET price=?,quantity=? WHERE name=?", (cost, change, itemL,))
            conn.commit()
            print("updating")
            await ctx.send(f"{quantity} {item.upper()} has been added for Å{cost} each")
        else:
            c.execute("INSERT INTO store VALUES (?, ?, ?)", (itemL, cost, quantity,))
            conn.commit()
            print("adding")
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
            print("removing")
            await ctx.send(f"{item.upper()} has been removed")
        else:
            print("N/A")
            await ctx.send("No such item is stocked")

def setup(client):
    client.add_cog(AdminCommands(client))
