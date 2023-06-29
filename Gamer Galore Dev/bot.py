#imports
import discord
import datetime
from discord import *
from discord.ext import commands, tasks
import random
from itertools import cycle
import json
import os
from time import sleep

#config file
if os.path.exists(os.getcwd() + "/config.json"):

    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token":"", "Prefix":"", "LogChannelID":""}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)
token = configData["Token"]
prefix = configData["Prefix"]
logChannel = configData["LogChannelID"]
codeOwner = "GamerGalore"

#eco.json file
if os.path.exists(os.getcwd() + "/eco.json"):
    pass
else:
    ecoTemplate = {}

    with open(os.getcwd() + "/eco.json", "w+") as f:
        json.dump(ecoTemplate, f)

#bot prefix(!)
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())


#bot status
bot_status = cycle(["Devloped by Gamer Galore", "/help"])
@tasks.loop(seconds=6)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

#start indicator
@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Success!!: we have login as {client.user}.")
    change_status.start()

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
        error_embed = discord.Embed(title="❌Command Not Found", description="That command doesn't exsit!", color=discord.Color.red())
        await interaction.send(embed=error_embed)

    if isinstance(error, commands.MissingRequiredArgument):
        missArg_embed = discord.Embed(title="❌Argument Missing", description="Please make sure you have entered all the required arguments", color=discord.Color.red())
        await interaction.send(embed=missArg_embed)

#shutdown______________________________________________________________________

#/shutdown
@client.tree.command(name="shutdown", description="Shuts down the bot")
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id != 974327261060821053:
        await interaction.response.send_message("no", ephemeral=True)
    else:
        await interaction.response.send_message("Bot of Glory is Shutting Down...", ephemeral=False)
        sleep(3)
        await client.close()

#shutdown
@client.command()
async def shutdown(ctx):
    if ctx.author.id != 974327261060821053:
        await ctx.send("no")
    else:
        await ctx.send("Bot of Glory is Shutting Down...")
        sleep(3)
        await client.close()


#economy commands_____________________________________________________________


#bal
@client.command(aliases=["bal"])
async def balance(ctx, member: discord.Member=None):
    with open("eco.json", "r") as f:
        user_eco = json.load(f)

    if member is None:
        member = ctx.author
    elif member is not None:
        member = member
    
    if str(member.id) not in user_eco:

        user_eco[str(member.id)] = {}
        user_eco[str(member.id)]["Balance"] = 100
        user_eco[str(member.id)]["Deposited"] = 0

        with open("eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

    eco_embed = discord.Embed(title=f"{member.name}'s Currnet Balance", description="The current balance of this user.", color=discord.Color.green())
    eco_embed.add_field(name="Current Balance:", value=f"${user_eco[str(member.id)]['Balance']}.")
    eco_embed.add_field(name="Deposited:", value=f"${user_eco[str(member.id)]['Deposited']}")
    eco_embed.set_footer(text="Want to incress balance? Try running some economy based commands!", icon_url=None)

    await ctx.send(embed=eco_embed)

#beg
@commands.cooldown(1, 600, commands.BucketType.user)
@client.command()
async def beg(ctx):
    with open("eco.json", "r") as f:
        user_eco = json.load(f)

    
    if str(ctx.author.id) not in user_eco:

        user_eco[str(ctx.author.id)] = {}
        user_eco[str(ctx.author.id)]["Balance"] = 100
        user_eco[str(ctx.author.id)]["Deposited"] = 0

        with open("eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)   

    cur_bal =  user_eco[str(ctx.author.id)]["Balance"] 
    amount = random.randint(-50, 50)
    new_bal = cur_bal + amount

    if cur_bal > new_bal:

        eco_embed = discord.Embed(title="Oh No! - You've been robbed!", description="A group of robber saw opportunity in taking atvantage of you", color=discord.Color.red())
        eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)
        eco_embed.set_footer(text="Should probaly beg in a nicer part of town...", icon_url=None)
        await ctx.send(embed=eco_embed)

        user_eco[str(ctx.author.id)]["Balance"] += amount

        with open("eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

    elif cur_bal < new_bal:
        
        eco_embed = discord.Embed(title="Oh Sweet Green!", description="Some kind souls out there have given you what they could.", color=discord.Color.green())
        eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)
        eco_embed.set_footer(text="Want more? Wait 1 hour to run this command again, or try some others!", icon_url=None)
        await ctx.send(embed=eco_embed)

        user_eco[str(ctx.author.id)]["Balance"] += amount

        with open("eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

    elif cur_bal == new_bal:
        
        eco_embed = discord.Embed(title="Awh That Sucks!", description="Looks like begging didn't get you anywhere today.", color=discord.Color.green())
        eco_embed.set_footer(text="Want more? Wait 1 hour to run this command again, or try some others!")
        await ctx.send(embed=eco_embed)

#work
@commands.cooldown(1, 432000, commands.BucketType.user)
@client.command()
async def work(ctx):    
    with open("eco.json", "r") as f:
        user_eco = json.load(f)

    
    if str(ctx.author.id) not in user_eco:

        user_eco[str(ctx.author.id)] = {}
        user_eco[str(ctx.author.id)]["Balance"] = 100
        user_eco[str(ctx.author.id)]["Deposited"] = 0

        with open("eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

    amount = random.randint(60,300)
    user_eco[str(ctx.author.id)]["Balance"] += amount


    eco_embed = discord.Embed(title="Phew!", description="After a tiring shift, heres what you earned!", color=discord.Color.green())
    eco_embed.add_field(name="Earnings:", value=f"${amount}", inline=False)
    eco_embed.add_field(name="New Balance:", value=f"{user_eco[str(ctx.author.id)]['Balance']}", inline=False)
    eco_embed.set_footer(text="Want more? Wait 5 days to run this command again, or try some others!")
    await ctx.send(embed=eco_embed)
    
    with open("eco.json", "w") as f:
        json.dump(user_eco, f, indent=4)

#steal
@commands.cooldown(1, 3600, commands.BucketType.user)
@client.command(name="steal")
async def steal(ctx, member: discord.Member):
    with open("eco.json", "r") as f:
        user_eco = json.load(f)
    
    steal_probability = random.randint(0,1)

    if steal_probability == 1: #user gets steal
        amount = random.randint(1, 100)

        if str(ctx.author.id) not in user_eco:

            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 100
            user_eco[str(ctx.author.id)]["Deposited"] = 0

            with open("eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        if str(member.id) not in user_eco:

            user_eco[str(member.id)] = {}
            user_eco[str(member.id)]["Balance"] = 100
            user_eco[str(member.id)]["Deposited"] = 0

            with open("eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)
        
        user_eco[str(ctx.author.id)]["Balance"] += amount
        user_eco[str(member.id)]["Balance"] -= amount
        with open("eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

        steal_embed = discord.Embed(title=f"Steal by {ctx.author.display_name}", description=f"You have stolen ${amount} from {member.mention}! Be sure to keep it safe as they may be lookingfor revenge...", color=discord.Color.gold())
        await ctx.send(embed=steal_embed)

    elif steal_probability == 0: #steal has failed, user gets nothing
        steal_fail_embed = discord.Embed(title=f"Steal by {ctx.author.display_name}", description=f"Uh oh.. You did not steal from this user, better luck next time...😈", color=discord.Color.dark_red())
        await ctx.send(embed=steal_fail_embed)

#deposit
@commands.cooldown(1, 300, commands.BucketType.user)
@client.command(aliases=["dep", "bank", "dp"])
async def deposit(ctx, amount: int):
    with open("eco.json", "r") as f:
        user_eco = json.load(f)

    if amount < 500:
        if str(ctx.author.id) not in user_eco:

            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 100
            user_eco[str(ctx.author.id)]["Deposited"] = 0

            with open("eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)    
        
        if amount > user_eco[str(ctx.author.id)]["Balance"]:
            depo_fail_embed = discord.Embed(title="⚠️You do not have suffecient funds to deposit this amount", description=None, color=discord.Color.red())
            await ctx.send(embed=depo_fail_embed)
        else:
            user_eco[str(ctx.author.id)]["Deposited"] += amount
            user_eco[str(ctx.author.id)]["Balance"] -= amount

            with open("eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)   
        depo_sucessful_embed = discord.Embed(title=f"You have deposited ${amount} into your bank", description="This money is now safe and only you can touch it", color=discord.Color.gold())
        await ctx.send(embed=depo_sucessful_embed)
    else:
        amount_fail_embed = discord.Embed(title="⚠️Deposit limit Reached!", description="Please enter a deposit amount lower than 500!", color=discord.Color.red())
        await ctx.send(embed=amount_fail_embed)

#withdraw
@client.command(aliases=["wd"])
async def withdraw(ctx, amount: int):
    with open("eco.json", "r") as f:
        user_eco = json.load(f)

    if str(ctx.author.id) not in user_eco:

        user_eco[str(ctx.author.id)] = {}
        user_eco[str(ctx.author.id)]["Balance"] = 100
        user_eco[str(ctx.author.id)]["Deposited"] = 0

        with open("eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)
   

    if amount > user_eco[str(ctx.author.id)]["Deposited"]:
        withdraw_fail_embed = discord.Embed(title="⚠️You do not have suffecient funds in your bank to withdraw this amount", description=None, color=discord.Color.red())
        await ctx.send(embed=withdraw_fail_embed)
    else:
        user_eco[str(ctx.author.id)]["Deposited"] -= amount
        user_eco[str(ctx.author.id)]["Balance"] += amount

        with open("eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)   
        withdraw_sucessful_embed = discord.Embed(title=f"You have withdrawed ${amount}", description="This money is now no longer safe, so people can steal from you.", color=discord.Color.gold())
        await ctx.send(embed=withdraw_sucessful_embed)


@client.command()
async def shop(ctx):

    shop_embed = discord.Embed(title="Bot of Glory Shop", color=discord.Color.magenta())
    shop_embed.add_field(name="Exclusive Chanenl", value="$2,000", inline=False)
    shop_embed.add_field(name="Exclusive Role", value="$5,00", inline=False)

    await ctx.send(embed=shop_embed, ephemeral=True)
    




#economy commands end__________________________________________________________

#commands _____________________________________________________________________







#claculator
@client.tree.command(name="calculator", description="This command does simple calculations")
async def cal(interaction: discord.Interaction, operaction: str, number1: int, number2: int):
    if operaction == "x":
        await interaction.response.send_message(number1*number2)
    elif operaction == "/":
        await interaction.response.send_message(number1/number2)
    elif operaction == "-":
        await interaction.response.send_message(number1-number2)
    elif operaction == "+":
        await interaction.response.send_message(number1+number2)
    else:
        op_embed = discord.Embed(title="Available Operations are:", color=discord.Color.blue())
        op_embed.add_field(name="x", value="Multiply", inline=False)
        op_embed.add_field(name="/", value="divition", inline=False)
        op_embed.add_field(name="+", value="addition", inline=False)
        op_embed.add_field(name="-", value="minus")
        await interaction.response.send_message(embed=op_embed, ephemeral=True)

#welcome
@client.tree.command(name="welcome_user", description="Welcome a user to the server with a custom message")
async def welcomectm(interaction: discord.Interaction, member: discord.Member, message: str):
    welcome_embed = discord.Embed(title=f"{member.name} Welcome To {interaction.guild.name}", description=f"{interaction.user.mention} wants to welcome {member.mention} to {interaction.guild.name}", color=discord.Color.random())
    welcome_embed.add_field(name="Welcome", value=member.name, inline=False)
    welcome_embed.add_field(name=f"Custom Message From {interaction.user.display_name}", value=message, inline=False)
    welcome_embed.add_field(name=f"The Owner of the serer is:", value=interaction.guild.owner.mention)
    welcome_embed.set_image(url=f"{member.avatar}")

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
    info_embed = discord.Embed(title=f"{member.name}'s Quick Infomation", description="All the quick infomation about this Discord user.", color=member.color)
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
    await interaction.response.send_message(f"Thank you for votting us. ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ https://top.gg/servers/974352349663461456")

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
@client.command(aliases=["ping", "lat"])
async def latency(ctx):
    bot_latency = round(client.latency * 10000)
    await ctx.send(f"bot's latency is {bot_latency} ms.")

# /lanteny command
@client.tree.command(name="lantency", description="shows bot's lantency in ms.")
async def latency(interaction: discord.Interaction):
    bot_lantency = round(client.latency * 1000)
    await interaction.response.send_message(f"bot's lantency is {bot_lantency} ms.", ephemeral=True)

#8ball ($magic_eightball),($8ball),($eightball),($8Ball)
@client.command(aliases=["8ball", "eightball", "8Ball" ])
async def magic_eightball(ctx, *, question):
    with open("Ball.txt", "r") as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)
    await ctx.send(response)

#/8ball
@client.tree.command(name="eightball", description="Simulates the classic 8ball")
async def eightball(interaction: discord.Interaction):
    with open("Ball.txt", "r") as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)
    await interaction.response.send_message(f"{response}")
  
#purge ($purge),($clear),(#cls)
@client.command(aliases=["clear", "cls"])
async def purge(ctx, count: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=count+1)
        await ctx.send(f"Purge was successful {ctx.author.mention}")
    else:
        await ctx.channel.purge(limit=1)
        await ctx.send(f"You don't have permission to manage messages {ctx.author.mention}")

#/purge
@client.tree.command(name="purge", description="clears a specify number of messages")
async def purge(interaction: discord.Interaction, count: int):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.guild_permissions.manage_messages:
        await interaction.channel.purge(limit=count)
        await interaction.followup.send(content=f"Purge was successful {interaction.user.mention}", ephemeral=True)
    else:
        await interaction.channel.purge(limit=1)
        
        await interaction.followup.send(content=f"You don't have permission to manage messages {interaction.user.mention}", ephemeral=True)

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
        await interaction.response.send_message(f"{member.mention} has been banned. Reason: {modreason}", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have the required permissions to ban members.", ephemeral=True)

#/unban
@client.tree.command(name="unban", description="unbans a selected user/bot")
async def unban_user(interaction: discord.Interaction, user_id: str):
    if len(user_id) != 18:
        await interaction.response.send_message("Invalid user ID.")
        return
    user = discord.Object(id=user_id)
    if interaction.user.guild_permissions.ban_members:
        await interaction.guild.unban(user)
        await interaction.response.send_message("Successful unban.")
    else:
        await interaction.response.send_message("You do not have the required permissions.")

#[prefix]help
@client.command()
async def help(ctx):
    await ctx.channel.purge(limit=1)

    user_embed = discord.Embed(title="Main User Commands", description="All the user commands available", color=discord.Color.blue())
    user_embed.add_field(name="8ball", value="These commands simulate the classic 8-Ball")
    user_embed.add_field(name="calculator", value="this command is a basic calculator. (+  -  /  x)")
    user_embed.add_field(name="server info", value="This command tells all available infomation of the server you are in.")
    user_embed.add_field(name="Welcome user", value="this command lets you welcome come a user to the server with a custom message (manually)")
    user_embed.add_field(name="vote", value="This command gives you a link to vote the Gamers of Glory server on top.gg")
    user_embed.add_field(name="Quick info", value="this give you all the quick info about a user")
    user_embed.add_field(name="Need extra Help click here https://discord.gg/r6DhXRJpmm", value=None, inline=False)

    mod_embed = discord.Embed(title="Moderation commands", description="All moderation commands available", color=discord.Color.og_blurple())
    mod_embed.set_author(name="Bot of Glory")
    mod_embed.add_field(name="purge [amount]", value="clears a specified amount of messages in the channel the command is run in", inline=False)
    mod_embed.add_field(name="kick", value="Kick user from guild/server", inline=False)
    mod_embed.add_field(name="ban", value="bans user from guild/server", inline=False)
    mod_embed.add_field(name="unban", value="unbans user from guild/server", inline=False)
    mod_embed.add_field(name="Need extra Help click here https://discord.gg/r6DhXRJpmm", value=None, inline=False)

    eco_cmd_embed = discord.Embed(title="Economy Commands", description="Your current balance can be used to buy stuff. but it is vulnerable. So you store your funds in the bank", color=discord.Color.brand_green())
    eco_cmd_embed.add_field(name="Balance [@member]", value="([@member] is optional) This command lets you see yours or some else's balance")
    eco_cmd_embed.add_field(name="Beg", value="This command gives you at random $-50 to $50. Can beg every 10mins")
    eco_cmd_embed.add_field(name="Work", value="This command give you at random $60 to $300 for working hard. Can work every 5 days")
    eco_cmd_embed.add_field(name="Steal @member", value="(@member is not optional) this command at random $1 to $100 from the chosen person. Can steal every 1hour")
    eco_cmd_embed.add_field(name="Deposit", value="This command lets you deposit your money in to your bank, so it is safe from people stealing it. Max deposit at a time is 500. can deposit every 5mins")
    eco_cmd_embed.add_field(name="Withdraw", value="This command lets you withdraw the money from your bank to current balance. So you can you the funds to buy stuff with")
    eco_cmd_embed.add_field(name="Need extra Help click here https://discord.gg/r6DhXRJpmm", value=None, inline=False)

    await ctx.send(embed=user_embed)
    await ctx.send(embed=eco_cmd_embed)
    await ctx.send(embed=mod_embed)
    
#/help
@client.tree.command(name="help", description="shows you a list of commands and more.")
async def help(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    user_embed2 = discord.Embed(title="Main User Commands", description="All the user commands available", color=discord.Color.blue())
    user_embed2.add_field(name="8ball", value="These commands simulate the classic 8-Ball")
    user_embed2.add_field(name="calculator", value="this command is a basic calculator. (+  -  /  x)")
    user_embed2.add_field(name="server info", value="This command tells all available infomation of the server you are in.")
    user_embed2.add_field(name="Welcome user", value="this command lets you welcome come a user to the server with a custom message (manually)")
    user_embed2.add_field(name="vote", value="This command gives you a link to vote the Gamers of Glory server on top.gg")
    user_embed2.add_field(name="Quick info", value="this give you all the quick info about a user")
    user_embed2.add_field(name="Need extra Help click here https://discord.gg/r6DhXRJpmm", value=None, inline=False)

    mod_embed2 = discord.Embed(title="Moderation commands", description="All moderation commands available", color=discord.Color.og_blurple())
    mod_embed2.set_author(name="Bot of Glory")
    mod_embed2.add_field(name="purge [amount]", value="clears a specified amount of messages in the channel the command is run in", inline=False)
    mod_embed2.add_field(name="/kick", value="Kick user from guild/server", inline=False)
    mod_embed2.add_field(name="/ban", value="bans user from guild/server", inline=False)
    mod_embed2.add_field(name="/unban", value="unbans user from guild/server", inline=False)
    mod_embed2.add_field(name="Need extra Help click here https://discord.gg/r6DhXRJpmm", value=None, inline=False)

    eco_cmd_embed2 = discord.Embed(title="Economy Commands", description="Your current balance can be used to buy stuff. but it is vulnerable. So you store your funds in the bank", color=discord.Color.brand_green())
    eco_cmd_embed2.add_field(name="Balance [@member]", value="([@member] is optional) This command lets you see yours or some else's balance")
    eco_cmd_embed2.add_field(name="Beg", value="This command gives you at random $-50 to $50. Can beg every 10mins")
    eco_cmd_embed2.add_field(name="Work", value="This command give you at random $60 to $300 for working hard. Can work every 5 days")
    eco_cmd_embed2.add_field(name="Steal @member", value="(@member is not optional) this command at random $1 to $100 from the chosen person. Can steal every 1hour")
    eco_cmd_embed2.add_field(name="Deposit", value="This command lets you deposit your money in to your bank, so it is safe from people stealing it. Max deposit at a time is 500. can deposit every 5mins")
    eco_cmd_embed2.add_field(name="Withdraw", value="This command lets you withdraw the money from your bank to current balance. So you can you the funds to buy stuff with")
    eco_cmd_embed2.add_field(name="Need extra Help click here https://discord.gg/r6DhXRJpmm", value=None, inline=False)

    await interaction.followup.send(embed=user_embed2, ephemeral=True)
    await interaction.followup.send(embed=eco_cmd_embed2, ephemeral=True)
    await interaction.followup.send(embed=mod_embed2, ephemeral=True)
    await interaction.followup.send(f"The Creator of the code {codeOwner} thaks you for using it", ephemeral=True)

#bot token & runs script
client.run(token)