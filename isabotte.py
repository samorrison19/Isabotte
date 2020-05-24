# IT'S ALIVE!
# Environment vars in .env file - loaded by python-dotenv
# DO NOT DISTRIBUTE .env ALONGSIDE SOURCE.

from dotenv import load_dotenv
import os
# import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('ISABOTTE_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intro = "Hello! I'm Isabotte! As Mr. Nook said, I'm part of the "\
                    "Resident Services staff here on Discord."

bot = commands.Bot(command_prefix='!', description=intro)


cogs = ['cogs.owner',
        'cogs.misc',
        'cogs.bugs',
        'cogs.fish',
        'cogs.villagers']


if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(cog)


@bot.event
async def on_ready():
    guilds = bot.guilds
    print(f'{bot.user.name} is connected to the following guilds:')
    for guild in guilds:
        print(f'{guild.name}(id: {guild.id})')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Wowzers we really don't want to respond to ourselves

    if 'good bot' in message.content.lower():
        await message.add_reaction('🥰')

    # Without the following line, no commands are ever run.
    await bot.process_commands(message)


bot.run(TOKEN)
