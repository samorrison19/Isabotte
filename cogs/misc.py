import discord
import re
import random
import time
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello', help='Says "Hello world"')
    async def hello_world(self, ctx):  # Context - guild and channel
        response = 'Hello world! I\'m Isabotte!'
        await ctx.send(response)

    @commands.command(name='roll', help='Roll dice. Format: !roll 3d6')
    async def roll_dice(self, ctx, dice_string):
        pattern = '\d+d\d+'
        match = re.search(pattern, dice_string)
        if not match:
            return
        args = re.split('d', match.group(0))
        number = int(args[0])
        sides = int(args[1])
        answer = 0
        for die in range(0, number):
            answer = answer+random.choice(range(1, sides+1))
        await ctx.send(answer)

    # TODO Remove?
    @commands.command(name='time',
                      help="Get month and hour.")
    async def current_time(self, ctx):
        now = time.localtime()
        await ctx.send(f'Month: {now.tm_mon}, Hour: {now.tm_hour}')


def setup(bot):
    bot.add_cog(Misc(bot))
