from discord.ext import commands
import acdb_module as db
import time


class Fish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fish',
                      help='Get fish with name. "!fish tuna"')
    async def get_fish(self, ctx, fish):
        comment = db.long_mobile_comment_fish(db.fish_with_precise_name(fish))
        if len(comment) == 0:
            comment = db.long_mobile_comment_fish(db.fish_with_name(fish))
        if len(comment) > 2000:
            comment = comment[:1990] + '...'
        if len(comment) != 0:
            await ctx.send(f'```{comment}```')

    @commands.command(name='currentfish',
                      help='Get list of fish currently available.')
    async def current_fish(self, ctx):
        now = time.localtime()
        comment = db.mobile_comment_fish(db.fish_in_hour(now.tm_mon,
                                                         now.tm_hour))
        if len(comment) > 2000:
            comment = comment[:1990] + '...'
        await ctx.send(f'```{comment}```')

    @commands.command(name='fishleaving',
                    help='Get all fish leaving after this month.')
    async def bug_last_chance(self, ctx):
        now = time.localtime()
        comment = db.long_mobile_comment_fish(db.get_last_chance('fish', 
                                                                    now.tm_mon))
        if len(comment) > 2000:
            comment = db.mobile_comment_fish(db.get_last_chance('fish', 
                                                                    now.tm_mon))
            if len(comment) > 2000:
                comment = comment[:1990] + '...'
        if len(comment) == 0:
            comment = 'No fish leaving after this month.'
        await ctx.send(f'```{comment}```')


def setup(bot):
    bot.add_cog(Fish(bot))
