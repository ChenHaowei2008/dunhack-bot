import discord
from discord.commands import SlashCommandGroup, OptionChoice, Option
from discord.ext import commands
from commands.functions import scrapeChallenges, scrapeUsernames, scrapeScoreboard
from credentials import cookies

class admin(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    admin = SlashCommandGroup("admin", "Some admin stuff", guild_ids=[1104414951730335907])

    @admin.command()
    async def scrape_challenges(self, ctx):
        if(ctx.author.id != 387169595544305674):
            await ctx.respond("This command isn't for u.")
            return
        await ctx.respond("Yes daddy! Scraping challenge data now!")
        await scrapeChallenges(cookies)

    @admin.command()
    async def scrape_scoreboard(self, ctx):
        if(ctx.author.id != 387169595544305674):
            await ctx.respond("This command isn't for u.")
            return
        await ctx.respond("Yes daddy! Scraping scoreboard data now!")
        await scrapeScoreboard(cookies)

    @admin.command()
    async def scrape_usernames(self, ctx):
        if(ctx.author.id != 387169595544305674):
            await ctx.respond("This command isn't for u.")
            return
        await ctx.respond("Yes daddy! Scraping username data now!")
        await scrapeUsernames(cookies)

def setup(bot):
    bot.add_cog(admin(bot))

