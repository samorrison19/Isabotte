from discord.ext import commands
import acdb_module as db
import time


class Villagers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='villager',
                      help='Get villager with name. "!villager raymond"')
    async def get_fish(self, ctx, villager):
        comment = db.villager_comment(villager)
        await ctx.send(comment)


def setup(bot):
    bot.add_cog(Villagers(bot))
