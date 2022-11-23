import discord
import os
from dotenv import load_dotenv

# TOKEN = os.environ['TOKEN']
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# --------------------------------------------variable
prefix = '$'
text_error = "Sorry, no command found. Try $help to see the list of command"
command_info = ("$help - list of commands and how to type.\n $help *command* - to get help for only one command",
                "$hello - I will say hi.",
                "$stats - see your stats in this server.")
error_desc = "Sorry, no command found. Try $help to see the list of command"
list_of_command = ["help", "hello", "stats"]


# --------------------------------------------embeds
def get_help():
    embed = discord.Embed(title='no command found :(', description=error_desc, color=0xffcc00)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
    return embed


def help_embed():
    # make text for the embed
    text = ""
    for command in command_info:
        text = text + command + '\n'
    embed = discord.Embed(title="", description="", color=0xffcc00)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
    embed.add_field(name="how to type commands?", value=f'Type the prefix \'{prefix}\' before the name of commands')
    embed.add_field(name="list of commands", value=text, inline=False)
    return embed


def one_help_embed(arg):
    text = ""
    i = 0
    for command in list_of_command:
        if command == arg:
            break
        i += 1
    text += command_info[i]
    embed = discord.Embed(title="", description="", color=0xffcc00)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
    embed.add_field(name="how to type this command?", value=f'Type {prefix + arg}')
    embed.add_field(name="what this command does:", value=text, inline=False)
    return embed


def stat_embed():
    embed = discord.Embed(title="Your rank:", description="No ranks yet", color=0xffcc00)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
    return embed


# --------------------------------------------events
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # no command found near prefix
    if message.content.startswith(prefix):
        # split from prefix and set the command as msg variable
        msg = message.content.split(prefix)
        msg = msg[1]
        msg = msg.split(" ")
        found = 0
        # search if the command does exist
        for command in list_of_command:
            if command == msg[0]:
                found = 1
        if found == 0:
            await message.channel.send(embed=get_help())

    # what to do for each command
    if message.content.startswith(prefix + 'hello'):
        await message.channel.send('Hello!')

    if message.content.startswith(prefix + 'help'):
        msg = message.content.split()
        # basic help command
        if len(msg) == 1:
            await message.channel.send(embed=help_embed())
        # help for one command
        if len(msg) == 2:
            msg = message.content.split(prefix)
            msg = msg[1]
            msg = msg.split(" ")
            found = 0
            # search if the command does exist
            for command in list_of_command:
                if msg[1] == command:
                    found = 1
            if found == 1:
                await message.channel.send(embed=one_help_embed(msg[1]))
            else:
                await message.channel.send(embed=get_help())

        # too many arguments
        if len(msg) > 2:
            await message.channel.send(embed=get_help())

    if message.content.startswith(prefix + 'stats'):
        await message.channel.send(embed=stat_embed())


load_dotenv()
client.run(os.getenv('TOKEN'))

# by theoTDS
