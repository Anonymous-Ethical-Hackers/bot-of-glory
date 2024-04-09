#imports
# collapse = ctrl + k, ctrl + 0
# expand =   ctrl +k, ctrl + j
import os
import discord
import sqlite3
import datetime
from discord.ext import commands
import random
import json
import os
from time import sleep
import asyncio

#config file

# Get the directory path of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up two directories to reach the parent directory
parent_dir = os.path.dirname(os.path.dirname(script_dir))

# Construct the absolute path to the JSON file with forward slashes
json_file_path = os.path.join(parent_dir, "bot-of-glory", "bin", "db", "json", "config.json").replace("\\", "/")

# Open the JSON file using the constructed absolute path
with open(json_file_path) as f:
    configData = json.load(f)
        
token = configData["Token"]
prefix = configData["Prefix"]
codeOwner = "GamerGalore"


#bot prefix(!)
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

@client.event
async def on_ready():
    try:
        # Sync the tree
        await client.tree.sync()

        # Start bankfee() as a task
        print('Starting bankfee loop...')
        client.loop.create_task(bankfee())
        await asyncio.sleep(2)
        print("Bankfee loop running!")

        # Database setup
        print("Setting up databases.")
        await asyncio.sleep(1)
        print("Setting up databases..")
        await asyncio.sleep(1)
        print("Setting up databases...")
        await asyncio.sleep(1)
        print("Setting up databases.")
        await asyncio.sleep(1)
        print("Setting up databases..")
        await asyncio.sleep(1)
        print("Setting up databases...")

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS eco (user_name STRING, user_id INTEGER, balance INTEGER, deposited INTEGER, bankrupt STRING, deposit_limit INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS bank (user_name STRING, user_id INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS welcome_settings (guild_id INTEGER, channel TEXT, Message TEXT, ImageURL TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS shop_items (item_id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, item_description TEXT, item_price INTEGER, command_name
        )''')

        db.commit()
        db.close()

        print("Successfully made the database and tables.")
        await asyncio.sleep(0.5)
        print(f"Success!! We have logged in as {client.user}.")
        await client.change_presence(activity=discord.Streaming(name="Gamer Game", url="https://twitch.tv/gamer_galore66"))

    except Exception as e:
        print(f"Error during setup: {e}")
        # Log the error and continue running
        exit


#removes premade help command
@client.remove_command("help")

#events _______________________________________________________________________

#error management
@client.event
async def on_command_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = error.retry_after
        retry_after = error.retry_after
        remaining_time = datetime.timedelta(seconds=retry_after)
        days = remaining_time.days
        hours = remaining_time.seconds // 3600
        minutes = (remaining_time.seconds % 3600) // 60
        seconds = remaining_time.seconds % 60
        cooldown_embed = discord.Embed(title="❌Command on Cooldown", description=f"This command is on cooldown. Please try again in {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.", color=discord.Color.red())
        await interaction.send(embed=cooldown_embed)

    if isinstance(error, commands.CommandNotFound):
        error_embed = discord.Embed(title="❌Command Not Found", description="That command doesn't exist!", color=discord.Color.red())
        await interaction.send(embed=error_embed)

    if isinstance(error, commands.MissingRequiredArgument):
        missArg_embed = discord.Embed(title="❌Argument Missing", description="Please make sure you have entered all the required arguments", color=discord.Color.red())
        await interaction.send(embed=missArg_embed)

#shutdown______________________________________________________________________

#/shutdown
@client.tree.command(name="shutdown", description="Shuts down the bot")
async def in_shutdown(interaction: discord.Interaction):
    if interaction.user.id != 974327261060821053:
        await interaction.response.send_message("no", ephemeral=True)
    else:
        await interaction.response.send_message("Bot of Glory is Shutting Down...", ephemeral=False)
        sleep(3)
        await client.close()

#shutdown
@client.command()
async def pr_shutdown(ctx):
    if ctx.author.id != 974327261060821053:
        await ctx.send("no")
    else:
        await ctx.send("Bot of Glory is Shutting Down...")
        sleep(3)
        await client.close()


#economy commands_____________________________________________________________


#balance
@client.hybrid_command(name="balance", description="Checks yours or someone elses balance.", aliases=["bal"])
async def balance(ctx, member: discord.Member=None):

    if member is None:
        member = ctx.author
    elif member is not None:
        member = member

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {member.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO eco(user_name, user_id, balance, deposited, bankrupt, deposit_limit) VALUES (?, ?, ?, ?, ?, ?)")
        val = (f"{member.global_name}", member.id, 100, 0, "Not Bankrupt", 100)
        cursor.execute(sql, val)
    db.commit()
    

    cursor.execute(f"SELECT balance, deposited, bankrupt, deposit_limit FROM eco WHERE user_id = {member.id}")
    eco = cursor.fetchone()
    try:
        user_bal = eco[0]
        user_dp = eco[1]
        user_bankrupt = eco[2]
        user_dp_limit  = eco[3]
    except:
        user_bal = 0
        user_dp = 0
        user_bankrupt = 0
        user_dp_limit  = 0

    if user_bankrupt == "Bankrupt":
        eco_red_embed = discord.Embed(title=f"{member.name}'s Current Balance", description="The current balance of this user.", color=discord.Color.red())
        eco_red_embed.add_field(name="Current Balance:", value=f"${user_bal}.")
        eco_red_embed.add_field(name="Deposited:", value=f"${user_dp}")
        eco_red_embed.add_field(name="Bankrupt status:", value=user_bankrupt)
        eco_red_embed.add_field(name="Deposit Limit:", value=f"${user_dp_limit}")
        eco_red_embed.set_footer(text="Want to increase balance? Try running some economy based commands!", icon_url=None)
        await ctx.send(embed=eco_red_embed)
       

    else:
        eco_embed = discord.Embed(title=f"{member.name}'s Current Balance", description="The current balance of this user.", color=discord.Color.green())
        eco_embed.add_field(name="Current Balance:", value=f"{user_bal}.")
        eco_embed.add_field(name="Deposited:", value=f"${user_dp}")
        eco_embed.add_field(name="Bankrupt status:", value=user_bankrupt)
        eco_embed.add_field(name="Deposit Limit:", value=f"${user_dp_limit}")
        eco_embed.set_footer(text="Want to increase balance? Try running some economy based commands!", icon_url=None)
        await ctx.send(embed=eco_embed)

    cursor.close()
    db.close()

#beg
@commands.cooldown(4, 60, commands.BucketType.user)
@client.hybrid_command(name="beg", description="You beg for money. but you may loss money instead.")
async def beg(ctx):

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {ctx.author.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO eco(user_name, user_id, balance, deposited, bankrupt, deposit_limit) VALUES (?, ?, ?, ?, ?, ?)")
        val = (f"{ctx.author.display_name}", ctx.author.id, 100, 0, "Not Bankrupt", 100)
        cursor.execute(sql, val)
        db.commit()


    cursor.execute(f"SELECT balance, deposited, bankrupt, deposit_limit FROM eco WHERE user_id = {ctx.author.id}")
    eco = cursor.fetchone()
    try:
        user_bal = eco[0]
        user_dp = eco[1]
        user_bankrupt = eco[2]
        user_dp_limit  = eco[3]
    except:
        user_bal = 0
        user_dp = 0
        user_bankrupt = 0
        user_dp_limit  = 0


    if user_bankrupt == "Bankrupt":
        no_beg_embed = discord.Embed(title="🏦 Sorry you are bankrupted", description="Try and withdrawing some money or get MOD to reset you.", color=discord.Color.red())
        return await ctx.send(embed=no_beg_embed)    
    
    amount = random.choice(list(range(-10, 100)))  # Limit amount to 100

    sql = (f"UPDATE eco SET balance=? WHERE user_id=?")
    new_bal = (user_bal + int(amount))
    cursor.execute(sql, (new_bal, ctx.author.id))
    db.commit()


    if new_bal < -99:
        sql = ("INSERT INTO bank(user_name, user_id) VALUES (?, ?)")
        val = (ctx.author.display_name, ctx.author.id)
        cursor.execute(sql, val)
        db.commit()

        sql = ("UPDATE eco SET bankrupt = 'Bankrupt' WHERE user_id = ?")
        val = (ctx.author.id,)
        cursor.execute(sql, val)
        db.commit()

    if user_bankrupt == "Bankrupt":
        no_beg_em = discord.Embed(title="🏦 Sorry you have gone bankrupt", description="Try withdrawing some money or get gamer galore to reset you.", color=discord.Color.red())
        no_beg_em.add_field(name="Your deposited is:", value=f"Deposited: ${user_dp}")
        await ctx.send(embed=no_beg_em)
        return



    if user_bal > new_bal:
        eco_embed = discord.Embed(title="Oh No! - You've been robbed!", description="A group of robbers saw an opportunity to take advantage of you.", color=discord.Color.red())
        eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)
        eco_embed.set_footer(text="You should probably beg in a nicer part of town...")
        await ctx.send(embed=eco_embed)

    elif user_bal < new_bal:
        eco_embed = discord.Embed(title="Oh Sweet Green!", description="Some kind souls out there have given you what they could.", color=discord.Color.green())
        eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)
        eco_embed.set_footer(text="Want more? Wait 1 hour to run this command again, or try some others!")
        await ctx.send(embed=eco_embed)

    else:
        eco_embed = discord.Embed(title="Awh That Sucks!", description="Looks like begging didn't get you anywhere today.", color=discord.Color.green())
        eco_embed.set_footer(text="Want more? Wait 1 hour to run this command again, or try some others!")
        await ctx.send(embed=eco_embed)
    
    db.close()


#work
@commands.cooldown(1, 1800, commands.BucketType.user)
@client.hybrid_command(name="work", description="work some some hard earn money!")
async def work(ctx):    
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {ctx.author.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO eco(user_name, user_id, balance, deposited, bankrupt, deposit_limit) VALUES (?, ?, ?, ?, ?, ?)")
        val = (f"{ctx.author.display}", ctx.author.id, 100, 0, "Not Bankrupt", 100)
        cursor.execute(sql, val)
    db.commit()

    cursor.execute(f"SELECT balance, deposited, bankrupt, deposit_limit FROM eco WHERE user_id = {ctx.author.id}")
    eco = cursor.fetchone()
    try:
        user_bal = eco[0]
        user_dp = eco[1]
        user_bankrupt = eco[2]
        user_dp_limit  = eco[3]
    except:
        user_bal = 0
        user_dp = 0
        user_bankrupt = 0
        user_dp_limit  = 0

    if user_bankrupt == "Bankrupt":   
        no_beg_embed = discord.Embed(title="🏦Sorry you are bankrupted", description="Try and withdrawing some money or get gamer galore to reset you.", color=discord.Color.red())
        return await ctx.send(embed=no_beg_embed)    

    amount = random.randint(60,300)
    sql = (f"UPDATE eco SET balance=? WHERE user_id=?")
    new_bal = (user_bal + int(amount))
    cursor.execute(sql, (new_bal, ctx.author.id))
    db.commit()


    eco_embed = discord.Embed(title="Phew!", description="After a tiring shift, heres what you earned!", color=discord.Color.green())
    eco_embed.add_field(name="Earnings:", value=f"${amount}", inline=False)
    eco_embed.add_field(name="New Balance:", value=f"${user_bal}", inline=False)
    eco_embed.set_footer(text="Want more? Wait 1 days to run this command again, or try some others!")
    await ctx.send(embed=eco_embed)
    
    cursor.close()
    db.close()

#steal
@commands.cooldown(3, 3600, commands.BucketType.user)
@client.hybrid_command(name="steal", description="steal from your fellow server mates. But be wary!")
async def steal(ctx, member: discord.Member):

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {member.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO eco(user_name, user_id, balance, deposited, bankrupt, deposit_limit) VALUES (?, ?, ?, ?, ?, ?)")
        val = (f"{member.global_name}", member.id, 100, 0, "Not Bankrupt", 100)
        cursor.execute(sql, val)
    db.commit()
    cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {ctx.author.id}")
    results = cursor.fetchone()
    if results is None:
        sql = ("INSERT INTO eco(user_name, user_id, balance, deposited, bankrupt, deposit_limit) VALUES (?, ?, ?, ?, ?, ?)")
        val = (f"{ctx.author.display_name}", ctx.author.id, 100, 0, "Not Bankrupt", 100)
        cursor.execute(sql, val)
    db.commit()  

    cursor.execute(f"SELECT balance, deposited, bankrupt, deposit_limit FROM eco WHERE user_id = {member.id}")
    eco = cursor.fetchone()
    try:
        user_bal = eco[0]
        user_dp = eco[1]
        user_bankrupt = eco[2]
        user_dp_limit  = eco[3]
    except:
        user_bal = 0
        user_dp = 0
        user_bankrupt = 0
        user_dp_limit  = 0

      
    if user_bankrupt == "Bankrupt":   
        no_beg_embed = discord.Embed(title="🏦Sorry you are bankrupted", description="Try and withdrawing some money or get gamer galore to reset you.", color=discord.Color.red())
        return await ctx.send(embed=no_beg_embed)    

    steal_probability = random.randint(0,1)

    if steal_probability == 1: #user gets steal
        amount = random.randint(1, 100)


        if user_bal < amount:      
            steal_fail_embed = discord.Embed(title=f"Steal by {ctx.author.display_name}", description=f"Uh oh.. You did not steal from this user, better luck next time...😈", color=discord.Color.dark_red())
            await ctx.send(embed=steal_fail_embed)
            return
        
        elif user_bal > amount:
            sql = (f"UPDATE eco SET balance=? WHERE user_id=?")
            new_bal = (user_bal - int(amount))
            cursor.execute(sql, (new_bal, member.id))  # subtract amount from member's balance
            db.commit()  # commit changes to the database

            sql = (f"UPDATE eco SET balance=? WHERE user_id=?")
            new_bal = (user_bal + int(amount))
            cursor.execute(sql, (new_bal, ctx.author.id))  # add amount to author's balance
            db.commit()  # commit changes to the database


            steal_embed = discord.Embed(title=f"Steal by {ctx.author.display_name}", description=f"You have stolen ${amount} from {member.mention}! Be sure to keep it safe as they may be looking for revenge...", color=discord.Color.gold())
            await ctx.send(embed=steal_embed)

    elif steal_probability == 0: #steal has failed, user gets nothing
        steal_fail_embed = discord.Embed(title=f"Steal by {ctx.author.display_name}", description=f"Uh oh.. You did not steal from this user, better luck next time...😈", color=discord.Color.dark_red())
        await ctx.send(embed=steal_fail_embed)

    db.close()

#deposit
@commands.cooldown(1, 10, commands.BucketType.user)
@client.hybrid_command(name="deposit", description="deposit your current balance to a safer location.", aliases=["dep", "bank", "dp"])
async def deposit(ctx, amount: int):
    
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {ctx.author.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO eco(user_name, user_id, balance, deposited, bankrupt, deposit_limit) VALUES (?, ?, ?, ?, ?, ?)")
        val = (f"{ctx.author.display_name}", ctx.author.id, 100, 0, "Not Bankrupt", 100)
        cursor.execute(sql, val)
    db.commit()
    
    cursor.execute(f"SELECT balance, deposited, bankrupt, deposit_limit FROM eco WHERE user_id = {ctx.author.id}")
    eco = cursor.fetchone()
    try:
        user_bal = eco[0]
        user_dp = eco[1]
        user_bankrupt = eco[2]
        user_dp_limit  = eco[3]
    except:
        user_bal = 0
        user_dp = 0
        user_bankrupt = 0
        user_dp_limit  = 0

    if user_bankrupt == "Bankrupt":
        no_beg_embed = discord.Embed(title="🏦Sorry you are bankrupted", description="Try and withdrawing some money or get gamer galore to reset you.", color=discord.Color.red())
        return await ctx.send(embed=no_beg_embed)    

    if amount <= 500:    
        if amount > user_bal:
            depo_fail_embed = discord.Embed(title="⚠️You do not have sufficient funds to deposit this amount", description=None, color=discord.Color.red())
            await ctx.send(embed=depo_fail_embed)
        else:
            sql = (f"UPDATE eco SET balance=?, deposited=? WHERE user_id=?")
            new_bal = (user_bal - int(amount))
            new_dp = (user_dp + int(amount))
            cursor.execute(sql, (new_bal, new_dp, ctx.author.id))  # changes amount to author's balance & deposited
            db.commit()  # commit changes to the database

        depo_successful_embed = discord.Embed(title=f"You have deposited ${amount} into your bank", description="This money is now safe and only you can touch it", color=discord.Color.gold())
        await ctx.send(embed=depo_successful_embed)
    else:
        amount_fail_embed = discord.Embed(title="⚠️Deposit limit Reached!", description="Please enter a deposit amount lower than 500!", color=discord.Color.red())
        await ctx.send(embed=amount_fail_embed)

    cursor.close()
    db.close()

#withdraw
@client.hybrid_command(name="withdraw", description="withdraw some money to your current balance.", aliases=["wd"])
async def withdraw(ctx, amount: int):

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {ctx.author.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO eco(user_name, user_id, balance, deposited, bankrupt, deposit_limit) VALUES (?, ?, ?, ?, ?, ?)")
        val = (f"{ctx.author.display_name}", ctx.author.id, 100, 0, "Not Bankrupt", 100)
        cursor.execute(sql, val)
    db.commit()
    

    cursor.execute(f"SELECT balance, deposited, bankrupt, deposit_limit FROM eco WHERE user_id = {ctx.author.id}")
    eco = cursor.fetchone()
    try:
        user_bal = eco[0]
        user_dp = eco[1]
        user_bankrupt = eco[2]
        user_dp_limit  = eco[3]
    except:
        user_bal = 0
        user_dp = 0
        user_bankrupt = 0
        user_dp_limit  = 0
    if amount < 1:
        withdraw_fail_embed = discord.Embed(title="⚠️ You can not withdraw this amount (Minimum = 1)", description=None, color=discord.Color.red())
        return await ctx.send(embed=withdraw_fail_embed)
    
    if amount > user_dp:
        withdraw_fail_embed2 = discord.Embed(title="⚠️ You do not have sufficient funds in your bank to withdraw this amount", description=None, color=discord.Color.red())
        await ctx.send(embed=withdraw_fail_embed2)
    else:
        sql = (f"UPDATE eco SET balance=?, deposited=? WHERE user_id=?")
        new_bal = (user_bal + int(amount))
        new_dp = (user_dp - int(amount))
        cursor.execute(sql, (new_bal, new_dp, ctx.author.id))  # changes amount to author's balance & deposited
        db.commit()  # commit changes to the database

        withdraw_success_embed = discord.Embed(title=f"You have withdrawn ${amount}", description="This money is now no longer safe, so people can steal from you.", color=discord.Color.gold())
        await ctx.send(embed=withdraw_success_embed)

    if user_bankrupt == "Bankrupt":
        if user_bal >= 0:
            sql = (f"UPDATE eco SET bankrupt=? WHERE user_id=?")
            user_bankrupt == "Not Bankrupt"
            cursor.execute(sql, (user_bankrupt, ctx.author.id)) #"Not Bankrupt"
            db.commit()  # commit changes to the database 

            cursor.execute("DELETE FROM bank WHERE user_id=?", (ctx.author.id))
            db.commit

            unbankrupt_embed = discord.Embed(title="🥳 You are no longer bankrupt", description="All the economy commands will work again!", color=discord.Color.green())
            await ctx.send(embed=unbankrupt_embed)

    cursor.close()
    db.close()

#reset
@client.hybrid_command(name="reset_bank_account", description="resets a user's bank account to a value", aliases=["rb"])
async def resetbank(ctx, member: discord.Member, current_bal: int):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    # Check if the mentioned member is None or a bot
    if member is None or member.bot:
        await ctx.send("Please mention a valid user.")
        return

    cursor.execute("SELECT * FROM eco WHERE user_id = ?", (member.id,))
    member_row = cursor.fetchone()

    if member_row is None:
        # If the member doesn't exist, create a new row with user_name
        cursor.execute("INSERT INTO eco (user_id, user_name, balance, deposited, bankrupt, deposit_limit) VALUES (?, ?, ?, ?, ?, ?)",
                       (member.id, member.name, 100, 0, "Not Bankrupt", 100))
    else:
        # Remove the member from the 'bank' table
        cursor.execute("DELETE FROM bank WHERE user_id = ?", (member.id,))

    # Update the member's balance in the 'eco' table
    cursor.execute("UPDATE eco SET balance = ?, deposited = ?, bankrupt = ?, deposit_limit = ? WHERE user_id = ?",
                   (current_bal, 0, "Not Bankrupt", 100, member.id))

    db.commit()
    db.close()

    await member.send("Your bank account for the Gamers of Glory server has been reset.")
    await ctx.send("Reset successful!")

#give/transfer
@client.hybrid_command(name="transfer", description="You give some of your money to another member")
async def transfer(ctx, recipient: discord.Member, amount: int):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    # Validate amount
    if amount <= 0:
        embed_value = discord.Embed(title="Invalid Amount", description="Please enter a positive amount to transfer.", color=discord.Color.red())
        await ctx.send(embed=embed_value)
        return

    # Check if the author has a bank account, create one if not
    cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {ctx.author.id}")
    result = cursor.fetchone()
    if result is None:
        sql = "INSERT INTO eco(user_name, user_id, balance, deposited, bankrupt, deposit_limit) VALUES (?, ?, ?, ?, ?, ?)"
        val = (ctx.author.name, ctx.author.id, 100, 0, "Not Bankrupt", 100)
        cursor.execute(sql, val)
        db.commit()

    # Check if the recipient has a bank account, create one if not
    cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {recipient.id}")
    result = cursor.fetchone()
    if result is None:
        sql = "INSERT INTO eco(user_name, user_id, balance, deposited, bankrupt, deposit_limit) VALUES (?, ?, ?, ?, ?, ?)"
        val = (recipient.name, recipient.id, 100, 0, "Not Bankrupt", 100)
        cursor.execute(sql, val)
        db.commit()

    # Retrieve the balance of the author
    cursor.execute(f"SELECT balance FROM eco WHERE user_id = {ctx.author.id}")
    author_balance = cursor.fetchone()[0]

    # Check if the author has sufficient balance for the transfer
    if author_balance >= amount:
        # Update author's balance
        new_author_balance = author_balance - amount
        cursor.execute("UPDATE eco SET balance = ? WHERE user_id = ?", (new_author_balance, ctx.author.id))
        db.commit()

        # Retrieve the balance of the recipient
        cursor.execute(f"SELECT balance FROM eco WHERE user_id = {recipient.id}")
        recipient_balance = cursor.fetchone()[0]

        # Update recipient's balance
        new_recipient_balance = recipient_balance + amount
        cursor.execute("UPDATE eco SET balance = ? WHERE user_id = ?", (new_recipient_balance, recipient.id))
        db.commit()

        # Send embed with transfer details
        embed = discord.Embed(
            title="Money Transfer",
            description=f"You have successfully transferred ${amount} from {ctx.author.name} to {recipient.name}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        # Send embed with insufficient balance message
        embed = discord.Embed(
            title="Insufficient Balance",
            description="You don't have enough balance to make this transfer.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    cursor.close()
    db.close()


# Deposit fee
async def bankfee():
    while True:
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM eco")
        all_users = cursor.fetchall()

        for user_row in all_users:
            user_id = user_row[0]
            cursor.execute("SELECT user_id, balance, deposited, bankrupt, deposit_limit FROM eco WHERE user_id = ?", (user_id,))
            eco = cursor.fetchone()

            if eco:
                user_bal = eco[1]
                user_dp = eco[2]
                user_bankrupt = eco[3]
                user_dp_limit = eco[4]

                user = await client.fetch_user(user_id)

                cb_value = user_bal

                if user_dp > user_dp_limit:
                    # DM the user only once when deposit limit breached
                    dp_limit_embed = discord.Embed(title="⚠️ Deposit Limit Breach ⚠️", description="Your current balance has been deducted by $10", color=discord.Color.red())
                    dp_limit_embed.add_field(name="Because your deposited money is greater than your deposit limit", value="Try withdrawing some funds", inline=False)
                    dp_limit_embed.add_field(name="You can increase your deposit limit by using", value="=shop dp_limit", inline=False)
                    dp_limit_embed.add_field(name="Your current deposit limit is", value=user_dp_limit, inline=False)
                    await user.send(embed=dp_limit_embed)

                    # Deduct $10 from balance
                    cb_value -= 10

                    # Ensure balance doesn't go below -100
                    cb_value = max(cb_value, -100)

                    # Update database with new balance
                    cursor.execute("UPDATE eco SET balance = ? WHERE user_id = ?", (cb_value, user_id))
                    db.commit()

                    # Check if user went bankrupt
                    if cb_value <= -100:
                        sql = ("INSERT INTO bank(user_name, user_id) VALUES (?, ?)")
                        val = (user.display_name, user.id)
                        cursor.execute(sql, val)
                        
                        sql = ("UPDATE eco SET bankrupt = 'Bankrupt' WHERE user_id = ?")
                        val = (user.id,)
                        cursor.execute(sql, val)

        db.close()
        await asyncio.sleep(60)  # Sleep for 1min before checking again


#add shop item
@client.hybrid_command(name="add_shop_item", description="Add an item to the shop")
@commands.has_permissions(administrator=True)
async def add_shop_item(ctx, item_name: str, item_description: str, item_price: int, command_name: str):
    try:
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute('''INSERT INTO shop_items (item_name, item_description, item_price, command_name)
            VALUES (?, ?, ?, ?)''', (item_name, item_description, item_price, command_name))
        db.commit()
        db.close()
        await ctx.send("Item added to the shop successfully!")
    except sqlite3.Error as e:
        await ctx.send(f"An error occurred while adding the item: {e}")

#show shop
@client.hybrid_command(name="shop", description="Display items available in the shop")
async def shop(ctx):
    try:
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute('''SELECT item_name, item_description, item_price FROM shop_items''')
        items = cursor.fetchall()
        db.close()

        if items:
            shop_embed = discord.Embed(title="Shop Items", color=discord.Color.blurple())
            for item in items:
                shop_embed.add_field(name=item[0], value=f"Description: {item[1]}\nPrice: ${item[2]}\n Command: =buy_dp_limit", inline=False)
            await ctx.send(embed=shop_embed)
        else:
            await ctx.send("No items available in the shop.")
    except sqlite3.Error as e:
        await ctx.send(f"An error occurred while fetching shop items: {e}")

@client.hybrid_command(name="buy_dp_limit")
async def buy_dp_limit(ctx):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    cursor.execute("SELECT item_price FROM shop_items WHERE item_name = ?", ("Deposit Limit",))
    price = cursor.fetchone()

    if not price:
        await ctx.send("The price for this item is not available.")
        db.close()
        return

    price = price[0]

    # Fetch user's balance from the eco table
    cursor.execute("SELECT balance FROM eco WHERE user_id = ?", (ctx.author.id,))
    user_balance = cursor.fetchone()

    if not user_balance:
        await ctx.send("You need to create an account first.")
        db.close()
        return

    user_balance = user_balance[0]

    if user_balance < price:
        await ctx.send("Insufficient balance.")
        db.close()
        return

    # Deduct the price from the user's balance
    new_balance = user_balance - price
    cursor.execute("UPDATE eco SET balance = ? WHERE user_id = ?", (new_balance, ctx.author.id))

    # Increase deposit limit by 50
    cursor.execute("UPDATE eco SET deposit_limit = deposit_limit + 50 WHERE user_id = ?", (ctx.author.id,))

    await ctx.send("Deposit Limit Extension purchased successfully!")
    db.commit()
    db.close()



#economy commands end__________________________________________________________
#welcome commands______________________________________________________________

#sending the welcome message
@client.event
async def on_member_join(member):
    try:
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute('''SELECT channel, message, imageURL FROM welcome_settings WHERE guild_id = ?''', (member.guild.id,))
        settings = cursor.fetchone()

        if settings:
            channel, message, imageURL = settings
            welcome_channel = member.guild.get_channel(channel)
            
            if welcome_channel:
                welcome_embed = discord.Embed(
                    title=f"Welcome to {member.guild.name}, {member.display_name}!",
                    description=message,
                    color=discord.Color.green()
                )
                welcome_embed.set_thumbnail(url=member.guild.icon_url)
                welcome_embed.set_image(url=imageURL)
                welcome_embed.set_footer(text="Enjoy your stay!")

                await welcome_channel.send(embed=welcome_embed)
            else:
                owner = member.guild.owner
                await owner.send(f"Welcome channel is not set. Please configure welcome settings for the server.")
    except sqlite3.Error as e:
        print(f"Error retrieving welcome settings: {e}")

#welcome settings
@client.hybrid_command(name="welcome_information")
@commands.has_permissions(administrator=True)
async def welcome_info(ctx):
    info_embed = discord.Embed(title="Welcome System Setup", description="Create a unique welcome system for your server", color=discord.Color.teal())
    info_embed.add_field(name="channel", value="Set a channel for your welcome card to be sent in.", inline=False)
    info_embed.add_field(name="message", value="Set a message to be included in your welcome card.", inline=False)
    info_embed.add_field(name="img", value="Set a image or gif url to be sent with the welcome card.", inline=False)
    await ctx.send(embed=info_embed)

@client.hybrid_command(name="welcome_config", description="Setup the welcome system for the server")
@commands.has_permissions(administrator=True)
async def welcome_config(ctx, channel: discord.TextChannel, message: str, image_url: str):
    print(f"Received parameters: {channel}, {message}, {image_url}")

    if not (channel and message and image_url):
        await ctx.send("Please provide the required arguments for setting up the welcome system.")
        return

    try:
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS welcome_settings (
            guild_id INTEGER,
            channel INTEGER,
            message TEXT,
            imageURL TEXT
        )''')

        cursor.execute('''INSERT INTO welcome_settings (guild_id, channel, message, imageURL)
            VALUES (?, ?, ?, ?)''', (ctx.guild.id, channel.id, message, image_url))

        db.commit()
        db.close()

        await ctx.send("Welcome system configured successfully!")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        await ctx.send(f"An error occurred while configuring the welcome system: {e}")


# main commands _______________________________________________________________

    
#calculator
@client.tree.command(name="calculator", description="This command does simple calculations")
async def cal(interaction: discord.Interaction, operation: str, number1: int, number2: int):
    if operation == "x":
        await interaction.response.send_message(number1*number2)
    elif operation == "/":
        await interaction.response.send_message(number1/number2)
    elif operation == "-":
        await interaction.response.send_message(number1-number2)
    elif operation == "+":
        await interaction.response.send_message(number1+number2)
    else:
        op_embed = discord.Embed(title="Available Operations are:", color=discord.Color.blue())
        op_embed.add_field(name="x", value="Multiply", inline=False)
        op_embed.add_field(name="/", value="division", inline=False)
        op_embed.add_field(name="+", value="addition", inline=False)
        op_embed.add_field(name="-", value="minus")
        await interaction.response.send_message(embed=op_embed, ephemeral=True)

#welcome
@client.tree.command(name="welcome_user", description="Welcome a user to the server with a custom message")
async def welcome_user(interaction: discord.Interaction, member: discord.Member, message: str):
    welcome_embed = discord.Embed(title=f"{member.name} Welcome To {interaction.guild.name}", description=f"{interaction.user.mention} wants to welcome {member.mention} to {interaction.guild.name}", color=discord.Color.random())
    welcome_embed.add_field(name="Welcome", value=member.name, inline=False)
    welcome_embed.add_field(name=f"Custom Message From {interaction.user.display_name}", value=message, inline=False)
    welcome_embed.add_field(name=f"The Owner of the serer is:", value=interaction.guild.owner.mention)
    welcome_embed.set_image(url="https://media.tenor.com/BwFlKOfK0EQAAAAd/welcome-welcome-to-hell.gif")

    await interaction.response.send_message(embed=welcome_embed, ephemeral=False)

# context menu ban
@client.tree.context_menu(name="Ban User")
async def cm_ban_user(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.guild_permissions.ban_members:
        await interaction.guild.ban(member)
        await interaction.response.send_message(f"{member.mention} has been banned.", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have the required permissions to ban members.", ephemeral=True)

#context menu kick
@client.tree.context_menu(name="Quick Info")
async def info(interaction: discord.Interaction, member: discord.Member):
    info_embed = discord.Embed(title=f"{member.name}'s Quick Information", description="All the quick information about this Discord user.", color=member.color)
    info_embed.add_field(name="Name:", value=member.name, inline=False)
    info_embed.add_field(name="ID:", value=member.id, inline=False)
    info_embed.add_field(name="Activity:", value=member.activity, inline=False)
    info_embed.add_field(name="Created At:", value=member.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
    info_embed.set_thumbnail(url=member.avatar)

    await interaction.response.send_message(embed=info_embed, ephemeral=True)

@client.tree.context_menu(name="Kick Member")
async def menukick(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.guild_permissions.kick_members:
        await interaction.guild.kick(member)
        await interaction.response.send_message(content=f"Successfully kicked {member.mention} from the sever!", ephemeral=True)
    else:
        await interaction.response.send_message(f"You do not have the required permissions to change the prefix", ephemeral=True)

#/vote
@client.tree.command(name="vote", description="vote for this server to help it grow (●'◡'●)")
async def vote(interaction: discord.Interaction):
    user_mention = interaction.user.mention
    await interaction.response.send_message(f"Thank you for voting us.||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ https://top.gg/servers/974352349663461456")

#server info
@client.tree.command(name="serverinfo", description="Shows you all the public information about the server/guild")
async def server_info(interaction: discord.Interaction):
    author_avatar = interaction.user.avatar
    author_name = interaction.user.name
    info_embed = discord.Embed(title=f"Information about {interaction.guild.name}", description="All public information about this guild/server", colour=discord.Colour.green())
    info_embed.set_thumbnail(url=interaction.guild.icon)
    info_embed.add_field(name="Name:", value=interaction.guild.name, inline=False)
    info_embed.add_field(name="ID:", value=interaction.guild.id, inline=True)
    info_embed.add_field(name="Owner:", value=interaction.guild.owner.mention, inline=True)
    info_embed.add_field(name="Member Count:", value=interaction.guild.member_count, inline=True)
    info_embed.add_field(name="Text Channel Count:", value=len(interaction.guild.text_channels), inline=True)
    info_embed.add_field(name="Voice Channel Count:", value=len(interaction.guild.voice_channels), inline=True)
    info_embed.add_field(name="Channel Count:", value=len(interaction.guild.channels), inline=True)
    info_embed.add_field(name="role Count:", value=len(interaction.guild.roles), inline=True)
    info_embed.add_field(name="Rules Channel:", value=interaction.guild.rules_channel.mention, inline=True)
    info_embed.add_field(name="Booster Count:", value=interaction.guild.premium_subscription_count, inline=True)
    info_embed.add_field(name="Booster Tier:", value=interaction.guild.premium_tier, inline=True)
    info_embed.add_field(name="Booster Role:", value=interaction.guild.premium_subscriber_role, inline=True)
    info_embed.add_field(name="Category Count:", value=len(interaction.guild.categories), inline=True)
    info_embed.add_field(name="Emoji Count:", value=len(interaction.guild.emojis), inline=True)
    info_embed.add_field(name="Sticker Count:", value=len(interaction.guild.stickers), inline=True)
    info_embed.add_field(name="Created At:", value=interaction.guild.created_at.__format__("%A, %d. %B %Y at %H:%M:%S"), inline=False)
    info_embed.set_footer(text=f"Requested by {author_name}", icon_url=author_avatar)

    await interaction.response.send_message(embed=info_embed, ephemeral=True)

#prints a user enter message into the terminal hosting the bot
@client.tree.command(name="direct-support", description="A command that prints a message to the terminal hosting the bot.")
async def my_command(interaction: discord.Interaction, message: str, server_invite_link: str):
    print(message, server_invite_link)
    await interaction.response.send_message(f"Your message `{message}` has been sent to the terminal.", ephemeral=True)

#latency 
@client.hybrid_command(name="latency", description="shows bot's latency in ms.", aliases=["ping", "lat"])
async def latency(ctx):
    bot_latency = round(client.latency * 10000)
    await ctx.send(f"bot's latency is {bot_latency} ms.")

#8ball ($magic_eightball),($8ball),($eightball),($8Ball)
@client.hybrid_command(name="eightball", description="Simulates the classic 8ball", aliases=["8ball", "8Ball" ])
async def magic_eightball(ctx, *, question):
    # Get the directory path of the current Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    ball_txt_path = os.path.join(parent_dir, "bin", "db", "txt", "ball.txt").replace("\\", "/")

    try:
        with open(ball_txt_path, "r") as f:
            random_responses = f.readlines()
    except FileNotFoundError:
        await ctx.send("Error: Could not find the ball.txt file.")
        return
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        return
        
    if not random_responses:
        await ctx.send("Error: The ball.txt file is empty.")
        return

    response = random.choice(random_responses)
    await ctx.send(response)

  
#purge
@client.hybrid_command(name="purge", description="clears a specify number of messages", aliases=["clear", "cls"])
async def purge(ctx, count: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=count+1)
    else:
        await ctx.channel.purge(limit=1)
        await ctx.message.author("You don't have permission to manage messages")

#/kick
@client.tree.command(name="kick", description="kicks a selected user/bot")
async def kick_user(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.guild_permissions.kick_members:
        await member.kick()
        await interaction.response.send_message(f"{member.mention} has been kicked.", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have the required permissions to kick members.", ephemeral=True)

#/ban
@client.tree.command(name="ban", description="bans a selected user/bot with a reason")
async def ban_user(interaction: discord.Interaction, member: discord.Member, modreason: str):
    if interaction.user.guild_permissions.ban_members:
        await member.ban(reason=modreason)
        channel = client.get_channel(974366529787404348)
        await channel.send(f"{member.mention} has been banned. Reason: {modreason}")
    else:
        await interaction.response.send_message("You do not have the required permissions to ban members.")

#help
@client.hybrid_command(name="help", description="shows you a list of commands and more.")
async def help(ctx):
    await ctx.channel.purge(limit=1)

    user_embed = discord.Embed(title="Main User Commands (/) = slash only", description="All the user commands available. Any thing in [] is an optional argument", color=discord.Color.random())
    user_embed.add_field(name="8ball", value="These commands simulates the classic 8-Ball", inline=False)
    user_embed.add_field(name="calculator", value="this command is a basic calculator. (+  -  /  x)", inline=False)
    user_embed.add_field(name="/server info", value="This command tells all available information of the server you are in.", inline=False)
    user_embed.add_field(name="/Welcome user @member", value="this command lets you welcome come a user to the server with a custom message (manually)", inline=False)
    user_embed.add_field(name="/vote", value="This command gives you a link to vote the Gamers of Glory server on top.gg", inline=False)
    user_embed.add_field(name="Quick info (in context menu)", value="this give you all the quick info about a user", inline=False)
    user_embed.set_footer(text="Need extra Help send me a DM on discord")

    mod_embed = discord.Embed(title="Moderation commands (/) = slash only", description="All moderation commands available. Any thing in [] is an optional argument", color=discord.Color.og_blurple())
    mod_embed.add_field(name="purge amount", value="clears a specified amount of messages in the channel the command is run in", inline=False)
    mod_embed.add_field(name="/kick @member", value="Kick user from guild/server", inline=False)
    mod_embed.add_field(name="/ban @member", value="bans user from guild/server", inline=False)
    mod_embed.set_footer(text="Need extra Help send me a DM on discord")

    eco_cmd_embed = discord.Embed(title="Economy Commands (all slash and prefix)", description="Your current balance can be used to buy stuff. but it is vulnerable. So you store your funds in the bank. Any thing in [] is an optional argument.", color=discord.Color.green())
    eco_cmd_embed.add_field(name="Balance [@member]", value="This command lets you see yours or some else's balance", inline=False)
    eco_cmd_embed.add_field(name="Beg", value="This command gives you at random $-50 to $50.", inline=False)
    eco_cmd_embed.add_field(name="Work", value="This command give you at random $60 to $300 for working hard.", inline=False)
    eco_cmd_embed.add_field(name="Steal @member", value="This command at random $1 to $100 from the chosen person.", inline=False)
    eco_cmd_embed.add_field(name="Deposit amount", value="This command lets you deposit your money in to your bank, so it is safe from people stealing it. Max deposit at a time is 500.", inline=False)
    eco_cmd_embed.add_field(name="Withdraw amount", value="This command lets you withdraw the money from your bank to current balance. So you can you the funds to buy stuff with", inline=False)
    eco_cmd_embed.add_field(name="Transfer", value="This command lets you transfer your money (balance) to another member", inline=False)
    eco_cmd_embed.set_footer(text="Need extra Help send me a DM on discord")

    info_embed = discord.Embed(title="Information", color=discord.Color.magenta())
    info_embed.set_image(url="https://cdn.discordapp.com/attachments/1096441468111028254/1227086050137210951/Dragon-Gamer_Galore.PNG?ex=66271ff0&is=6614aaf0&hm=008c0f9a37394d51ecb9a09dba6ece7f1d810e767a543e3226fc031a5c3e38d4&")
    info_embed.add_field(name="Prefix: ", value=prefix)

    await ctx.send(embed=info_embed)
    await ctx.send(embed=mod_embed)
    await ctx.send(embed=user_embed)
    await ctx.send(embed=eco_cmd_embed)
    
    
#runs scrip
client.run(token)
