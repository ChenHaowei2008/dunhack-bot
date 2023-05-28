import discord
from discord.commands import SlashCommandGroup, Option, OptionChoice
from discord.ext import commands
from discord import File
import json
from commands.functions import getAverageColour, processUsername
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta
import random

class data(commands.Cog):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot


    data = SlashCommandGroup("data", "For your statistical needs", guild_ids=[1104414951730335907])

    @data.command(description="Get raw data of all challenges")
    async def challenges_raw(self, ctx):
        await ctx.respond("Sure boss, here is your raw challenges json data!", file=File("data/challenges.json"))

    @data.command(description="Get raw data of all scoreboard")
    async def scoreboard_raw(self, ctx):
        await ctx.respond("Sure boss, here is your raw scoreboard json data!", file=File("data/scoreboard.json"))
    
    @data.command(description="Get raw data of usernames")
    async def username_raw(self, ctx):
        await ctx.respond("Apologies boss, I still have no idea how to upload more than ten files at once")

    @data.command(description="Get info on a username")
    async def username(self, ctx, username: str, pretty: bool = True, challs: int = 10):
        if(challs > 25):
            challs = 25
        
        username, output = processUsername(username)
        
        if(output != None):
            await ctx.respond(output)
            return

        if(pretty):
            with open(f"data/users/{username}.json") as file:
                data = json.loads(file.read().strip())["props"]["pageProps"]
            
            with open("data/scoreboard.json") as file:
                scoreboard = json.loads(file.read().strip())["props"]["pageProps"]["scores"]

            for i, score in enumerate(scoreboard):
                if(score["username"] == username):
                    index = i
                    break

            response = requests.get(data["userData"]["image"])
            img = Image.open(BytesIO(response.content))
            
            embed = discord.Embed(
                title = username,
                color = discord.Color.from_rgb(*getAverageColour(img)),
                url = f"https://dunhack.me/users/{username}",
                description = f"{username} is {i + 1} place with {scoreboard[i]['score']} points!\nHere are his last {challs} solves:"
            )

            embed.set_footer(text = datetime.today().strftime('%B %d - %I:%M:%S %p'))

            for i, challenge in enumerate(data["challengeSolved"]):
                if(i > challs - 1):
                    break
                embed.add_field(
                    name = f"{i + 1}) {challenge['title']}",
                    value = f"Solved on {(datetime.strptime(challenge['added'], '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=8)).strftime('%B %d - %I:%M:%S %p')}",
                )

            embed.set_thumbnail(url = data["userData"]["image"])

            await ctx.respond(embed = embed)
        else:
            await ctx.respond(f"Sure boss, here the data I have on `{username}`!", file = File(f"data/users/{username}.json"))


    @data.command(description = "Displays current scoreboard")
    async def scoreboard(self, ctx, people: int = 10):
        if(people > 25):
            people = 25
        with open("data/scoreboard.json") as file:
            scoreboard = json.loads(file.read().strip())["props"]["pageProps"]["scores"]
        
        embed = discord.Embed(
            title = "SCOREBOARD",
            color = discord.Color.gold(),
            url = "https://dunhack.me/scoreboard",
            description = f"Here are the top {people} on dunhack.me!"
        )

        embed.set_footer(text = datetime.today().strftime('%B %d - %I:%M:%S %p'))

        for i in range(people):
            embed.add_field(
                name = f"{i + 1}) {scoreboard[i]['username']}",
                value = f"Score: {scoreboard[i]['score']}",
                inline = False
            )
        
        # Place holder
        embed.set_thumbnail(url = f"https://placekitten.com/{random.randint(500,1000)}/{random.randint(500,1000)}")

        # with open(f"data/users/{scoreboard[0]['username']}.json") as file:
        #     img = json.loads(file.read().strip())["props"]["pageProps"]["userData"]["image"]

        # response = requests.get(img)
        # img = Image.open(BytesIO(response.content))
        # img2 = Image.open("data/crown.png")

        # img2.paste(img, (0, 0), img)

        await ctx.respond(embed = embed)

def setup(bot):
    bot.add_cog(data(bot))

