from discord.ext import commands
import acdb_module as db
import time


class Bugs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='currentbugs',
                      help='Get list of bugs currently available.')
    async def current_bugs(self, ctx):
        now = time.localtime()
        comment = db.mobile_comment_bug(db.bugs_in_hour(now.tm_mon,
                                                        now.tm_hour))
        if len(comment) > 2000:
            comment = comment[:1990] + '...'
        await ctx.send(f'```{comment}```')

    @commands.command(name='bug',
                      help='Get bug/bugs with name. "!bug tarantula"')
    async def get_bug(self, ctx, bug):
        comment = db.long_mobile_comment_bug(db.bug_with_precise_name(bug))
        if len(comment) == 0:
            comment = db.long_mobile_comment_bug(db.bugs_with_name(bug))
        if len(comment) > 2000:
            comment = comment[:1990] + '...'
        if len(comment) != 0:
            await ctx.send(f'```{comment}```')

    @commands.command(name='bugsleaving',
                      help='Get all bugs leaving after this month.')
    async def bug_last_chance(self, ctx):
        now = time.localtime()
        comment = db.long_mobile_comment_bug(db.get_last_chance('bugs', 
                                                                    now.tm_mon))
        if len(comment) > 2000:
            comment = db.mobile_comment_bug(db.get_last_chance('bugs', 
                                                                    now.tm_mon))
            if len(comment) > 2000:
                comment = comment[:1990] + '...'
        if len(comment) == 0:
            comment = 'No bugs leaving after this month.'
        await ctx.send(f'```{comment}```')

    @commands.command(name='bugsarriving',
                    help='Get all bugs new this month.')
    async def bug_new_arrivals(self, ctx):
        now = time.localtime()
        comment = db.long_mobile_comment_bug(db.get_new_arrivals('bugs', 
                                                                    now.tm_mon))
        if len(comment) > 2000:
            comment = db.mobile_comment_bug(db.get_new_arrivals('bugs', 
                                                                    now.tm_mon))
            if len(comment) > 2000:
                comment = comment[:1990] + '...'
        if len(comment) == 0:
            comment = 'No new bugs this month.'
        await ctx.send(f'```{comment}```')


def setup(bot):
    bot.add_cog(Bugs(bot))
