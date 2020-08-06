import discord
from discord.ext import commands
import sqlite3
import os

conn = sqlite3.connect("Data.db")
c = conn.cursor()

class MemberCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def help(self, ctx):
        sender = ctx.author
        if sender.top_role.permissions.administrator:
            embed = discord.Embed()
            embed.set_author(name="Help")
            embed.add_field(name="Calling commands", value="Call commands with the \'.\' prefix (ex: .help)")
            embed.add_field(name="buy", value="Allows user to buy available items from the store; put the name of the item after the command (optional: amount of that item) ex: .buy bread 3", inline=False)
            embed.add_field(name="sell", value="Allows user to sell items from their inventory; ex: .sell bread 2", inline=False)
            embed.add_field(name="store", value="Shows the items available in the store along with their price and quantity", inline=False)
            embed.add_field(name="balance", value="Shows the message author\'s balance (if they are a member)", inline=False)
            embed.add_field(name="items", value="Show the message author\'s items (if they are a member)", inline=False)
            embed.add_field(name="clear", value="Allows admin to clear a number of messages (including this command) from the channel it was called in; ex: .clear 5, will clear 5 messages including the command", inline=False)
            embed.add_field(name="refresh", value="Only owner can do this; resets database with server members that have a certain role (optional: starting money amount); ex: .refresh IRL 1000, adds everyone in server with the role IRL to the database and sets their balance to 1000 (default is 1000)", inline=False)
            embed.add_field(name="addMember", value="Manually add member to database to access commands; ex: .addMember @someone 1000 (money is optional)", inline=False)
            embed.add_field(name="removeMember", value="Manually remove member from database; ex: .removeMember @someone", inline=False)
            #embed.add_field(name="addMoney", value="Manually add money to a member in the database; ex: .addMoney @someone 1000", inline=False)
            embed.add_field(name="stock", value="Add or update items in the database (name price quantity); ex: .stock bread 20 3", inline=False)
            embed.add_field(name="unstock", value="Remove item from database")
            await sender.send(embed=embed)

        else:
            embed = discord.Embed()
            embed.set_author(name="Help")
            embed.add_field(name="Calling commands", value="Call commands with the \'.\' prefix (ex: .help)")
            embed.add_field(name="buy", value="Allows user to buy available items from the store; put the name of the item after the command (optional: amount of that item) ex: .buy bread 3", inline=False)
            #embed.add_field(name="sell", value="Allows user to sell items from their inventory; ex: .sell bread 2", inline=False)
            #embed.add_field(name="store", value="Shows the items available in the store along with their price and quantity", inline=False)
            embed.add_field(name="balance", value="Shows the message author\'s balance (if they are a member)", inline=False)
            #embed.add_field(name="items", value="Show the message author\'s items (if they are a member)", inline=False)
            await sender.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item, quantity=1):
        senderID = ctx.message.author.id
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
                    await ctx.send("Invalid quantity")
            else:
                await ctx.send(f"{item.upper()} is not stocked")
        else:
            await ctx.send(f"{ctx.message.author} is not a member")


    #Allow a user to sell items from their iventory
    @commands.command()
    async def sell(self, ctx, item, quantity=1):
        senderID = ctx.message.author.id
        c.execute("SELECT id FROM bank WHERE id=?", (senderID,))
        member = c.fetchone()

        if member != None:
            c.execute("SELECT items FROM bank WHERE id=?", (senderID,))
            itemStr = c.fetchone()
            itemDict = eval(itemStr[0])

            if bool(itemDict):
                itemL = item.lower()
                if itemL in itemDict and quantity <= itemDict[itemL]:
                    itemDict[itemL] -= quantity

                    if itemDict[itemL] == 0:
                        itemDict.pop(itemL)
                    c.execute("SELECT quantity FROM store WHERE name=?", (itemL,))
                    quant = c.fetchone()
                    c.execute("SELECT balance FROM bank WHERE id=?", (senderID,))
                    bal = c.fetchone() #balance of member trying to buy item
                    c.execute("SELECT price FROM store WHERE name=?", (itemL,))
                    cost = c.fetchone()

                    balChange = bal[0] + (cost[0]*quantity)
                    quantChange = quant[0] + quantity
                    c.execute("UPDATE bank SET balance=?,items=?  WHERE id=?", (balChange,str(itemDict),senderID,))
                    conn.commit()
                    c.execute("UPDATE store SET quantity=? WHERE name=?", (quantChange, itemL,))
                    conn.commit()
                    print("Updated")

                else:
                    await ctx.send(f"{ctx.message.author} does not own {quantity}x {item.upper()}")
            else:
                await ctx.send(f"{ctx.message.author} owns no items")
        else:
            await ctx.send(f"{ctx.message.author} is not a member")

    #Allows a user to print the contents of the store, the price, and quantity
    @commands.command()
    async def store(self):
        pass

    #Allows a user to see their balance
    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        senderID = ctx.author.id
        c.execute("SELECT balance FROM bank WHERE id=?", (senderID,))
        bal = c.fetchone()

        embed = discord.Embed(colour=discord.Color.blue())
        embed.add_field(name="Balance", value=f"Å{bal[0]}")
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

        print("balance embed")
        await ctx.send(embed=embed)

    #Allows a user to see the items they own
    @commands.command()
    async def items(self, ctx): #looks gross but it works for now. Dont know what to do to make it look nice (will work on)
        senderID = ctx.author.id
        c.execute("SELECT items FROM bank WHERE id=?", (senderID,))
        itemStr = c.fetchone()
        itemDict = eval(itemStr[0])

        itemNames = list(itemDict.keys())
        itemQuant = list(itemDict.values())

        embed = discord.Embed(colour=discord.Color.red())
        #embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

        for i in range(len(itemNames)):
            embed.add_field(name=itemQuant[i], value=itemNames[i], inline=False)

        await ctx.author.send(embed=embed)

def setup(client):
    client.add_cog(MemberCommands(client))
