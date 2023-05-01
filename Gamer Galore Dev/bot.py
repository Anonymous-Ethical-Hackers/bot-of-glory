#imports
from discord import Webhook
import aiohttp
import asyncio
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import json


#custom prifix code file
def get_server_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

    return prefix[str(message.guild.id)]


def get_server_logfile(client, message):
    with open("log.json", "r") as f:
        prefix = json.load(f)

    return prefix[str(message.channel.id)]



#bot prefix($)
client = commands.Bot(command_prefix=get_server_prefix, intents=discord.Intents.all())



#bot status
bot_status = cycle(["!help", "/help"])
@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

#start indicator
@client.event
async def on_ready():
    await client.tree.sync()
    print("Success!!: Bot is connected to Discord.")
    change_status.start()

@client.remove_command("help")


#prefix on server add
@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)


    prefix[str(guild.id)] = "!"

    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

#remove custom prefix on server leave
@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)



#commands _____________________________________________________________________

# @client.tree.command(name="", description="")
# async def test(interaction: discord.Interaction):
#    if interaction.user.guild_permissions.administrator:
#        await interaction.response.send_message("", ephemeral=True)
#    else:
#        await interaction.response.send_message(f"You do not have the required permissions to change the prefix", ephemeral=True)



#giveaway

@commands.command()
async def giveaway(self, ctx, minutes: int, *, prize: str):
    await ctx.send(f"React with :tada: to enter the giveaway for **{prize}**!")
    new_msg = await ctx.channel.history(limit=1).flatten()[0]
    await new_msg.add_reaction("🎉")

    await asyncio.sleep(minutes*60)

    new_msg = await ctx.fetch_message(new_msg.id)
    users = []
    async for user in new_msg.reactions[0].users():
        users.append(user)
    winner = random.choice(users)

    await ctx.send(f"Congratulations {winner.mention}! You won **{prize}**!")






class ReportModal(discord.ui.Modal, title="Report User"):
    user_name = discord.ui.TextInput(label="User's Discord Name", placeholder="eg. bob#0000", required=True, max_length=1000, style=discord.TextStyle.short)
    user_id = discord.ui.TextInput(label="Discord ID", placeholder="To Grab a users ID make sure Developer Mode is on", required=True, max_length=1000, style=discord.TextStyle.short)
    description = discord.ui.TextInput(label="Infomation", placeholder="eg. boke rule #9", required=True, min_length=50 , max_length=2500, style=discord.TextStyle.paragraph)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} Thank you for sending the report, the moderation team will see it momentarily", ephemeral=True)

        channel = discord.utils.get(interaction.guild.channels, name="log")

        await channel.send(f"Report Submitted by {interaction.user.mention} \n Name: {self.user_name} \n ID: {self.user_id} \n Reported for: {self.description}")


@client.tree.command(name="report_user", description="reports a user to server/guild admin & owner")
async def report(interaction: discord.Interaction):
    await interaction.response.send_modal(ReportModal())


 

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



#coustom prefix command 
@client.command()
async def setprefix(ctx, *, newprefix: str):
    if ctx.author.guild_permissions.administrator:
        with open("prefixes.json", "r") as f:
            prefix = json.load(f)

        prefix[str(ctx.guild.id)] = newprefix

        with open("prefixes.json", "w") as f:
            json.dump(prefix, f, indent=4)

        await ctx.send(f"Success!!")
    else:
        await ctx.send(" you do not have the required permissions to change the prefix", ephemeral=True)

#/set-new-prefix
@client.tree.command(name="set-new-prefix", description="sets you a custom prefix")
async def setprefix(interaction: discord.interactions, *, newprefix: str):
    if interaction.user.guild_permissions.administrator:
        with open("prefixes.json", "r") as f:
            prefix = json.load(f)

        prefix[str(interaction.guild.id)] = newprefix

        with open("prefixes.json", "w") as f:
            json.dump(prefix, f, indent=4)
        user_mention = interaction.user.mention
        await interaction.response.send_message(f"Success!!{user_mention}", ephemeral=True)
    else:
        await interaction.response.send_message(f"You do not have the required permissions to change the prefix", ephemeral=True)

#latency 
@client.command()
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
    help_embed = discord.Embed(title="Help Desk For Bot of Glory", description="Alll commands for the bot", color=discord.Color.random())
    help_embed.set_author(name="Bot of Glory")
    help_embed.add_field(name="/purge & [prefix]purge", value="clears a specified amount of messages in the channel the command is run in", inline=False)
    help_embed.add_field(name="/set-new-prefix & [prefix]setprefix", value="The default prefix is '!' these commands let u change the default prefix to any prefix you want", inline=False)
    help_embed.add_field(name="/8ball & [prefix]8ball", value="These commands simulate the classic 8-Ball", inline=False)
    help_embed.add_field(name="/kick", value="Kick user from guild/server", inline=False)
    help_embed.add_field(name="/ban", value="bans user from guild/server", inline=False)
    help_embed.add_field(name="/unban", value="unbans user from guild/server", inline=False)
    help_embed.add_field(name="Need extra Help", value="[Join our Server](https://discord.gg/r6DhXRJpmm)", inline=False)

    await ctx.send(embed=help_embed)

#/help
@client.tree.command(name="help", description="shows you a list of commands and more.")
async def help(interaction: discord.Interaction):
    await interaction.channel.purge(limit=1)
    await interaction.response.defer(ephemeral=True)
    help_embed2 = discord.Embed(title="Help Desk For Bot of Glory", description="Alll commands for the bot", color=discord.Color.random())
    help_embed2.set_author(name="Bot of Glory")
    help_embed2.add_field(name="/purge & [prefix]purge", value="clears a specified amount of messages in the channel the command is run in", inline=False)
    help_embed2.add_field(name="/set-new-prefix & [prefix]setprefix", value="The default prefix is '!' these commands let u change the default prefix to any prefix you want", inline=False)
    help_embed2.add_field(name="/8ball & [prefix]8ball", value="These commands simulate the classic 8-Ball", inline=False)
    help_embed2.add_field(name="/kick", value="Kick user from guild/server", inline=False)
    help_embed2.add_field(name="/ban", value="bans user from guild/server", inline=False)
    help_embed2.add_field(name="/unban", value="unbans user from guild/server", inline=False)
    help_embed2.add_field(name="/direct-help", value="sends a message the terminal hosting the bot. Giveing the owner to join the server and help", inline=False)
    help_embed2.add_field(name="Need extra Help", value="[Join our Server](https://discord.gg/r6DhXRJpmm)", inline=False)

    await interaction.followup.send(embed=help_embed2)
    

# imports the file witch holds the token
import bot_token

#bot token & runs script
client.run(bot_token.bot_token)
