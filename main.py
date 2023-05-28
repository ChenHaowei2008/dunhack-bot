import discord
from discord.ext import commands, tasks
import traceback
import random
from credentials import token, cookies
from commands.functions import scrapeChallenges, scrapeUsernames, scrapeScoreboard

intents = discord.Intents.all()

# config
bot = commands.Bot(
    intents=intents,
)

names = ["Dunhack Bot", "rm -rf / --no-preserve-root", "dd if=/dev/zero of=/dev/sd*", ":(){ :|: & };:", "mv ~ /dev/null", "sudo shutdown -h now", "> /etc/passwd", "sudo chmod -R 777 /", "history | sh", ""]

@bot.event
async def on_ready():
    print("Bot is ready.")

# @bot.event
# async def on_application_command_error(ctx, e):
#     await ctx.respond(e)

#TODO: Fix this. Doesn't run at all, no matter where I put it
@tasks.loop(hours=3)
async def changeName(self):
    await bot.user.edit(username = random.choice(names))
    await scrapeChallenges(cookies)
    await scrapeScoreboard(cookies)
    await scrapeUsernames(cookies)
    print("Scraped data")

if __name__ == "__main__":
    bot.load_extension("commands.data")
    bot.load_extension("commands.misc")
    bot.load_extension("commands.admin")
    bot.run(token)
