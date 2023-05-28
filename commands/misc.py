import discord
from discord.commands import SlashCommandGroup, OptionChoice, Option
from discord.ext import commands
from discord import File, ButtonStyle
from commands.functions import processUsername, calculateWeightage
import json
import random
from discord.ui import Button

class DefaultView(discord.ui.View):
    def __init__(self):
        super().__init__()

class DefaultButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class misc(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    misc = SlashCommandGroup("misc", "Other commands", guild_ids=[1104414951730335907])

    difficultyChoices = [
        OptionChoice(name="easy", value="easy"),
        OptionChoice(name="medium", value="medium"),
        OptionChoice(name="hard", value="hard")
    ]
    # There is probably a more efficient way to do this...
    categoryChoices = [
        OptionChoice(name="Pwn", value=0),
        OptionChoice(name="Forensics", value=1),
        OptionChoice(name="Crypto", value=2),
        OptionChoice(name="Web", value=3),
        OptionChoice(name="Misc", value=4),
        OptionChoice(name="RE", value=5),
        OptionChoice(name="Steganography", value=6),
        OptionChoice(name="SIGINT", value=7),
        OptionChoice(name="OSINT", value=8),
        OptionChoice(name="Mobile", value=9),
        OptionChoice(name="Scripting", value=10),
        OptionChoice(name="Baby", value=11)
    ]

    @misc.command(description="Chooses a challenge based on paramters you have selected.")
    async def choose_chall( 
                            self,
                            ctx, 
                            category: Option(int, "What category of challenges", choices = categoryChoices) = None,
                            username: Option(str, "Your username") = None, 
                            difficulty: Option(str, "Basically how many people have already solved.", choices = difficultyChoices) = None
                           ):
        with open("data/challenges.json", "r") as file:
            data = file.read().strip()

        data = json.loads(data)["props"]["pageProps"]["challengeData"]
        if(category != None):
            challenges = data[category]["challenges"]
        else:
            challenges = [chall for cat in data for chall in cat["challenges"]]


        if(username != None):
            username, output = processUsername(username)
            if(output != None):
                await ctx.respond(output)
                return
            
            with open(f"data/users/{username}.json") as file:
                challengesSolved = [chall["title"] for chall in json.loads(file.read().strip())["props"]["pageProps"]["challengeSolved"]]
            challenges = [challenge  for challenge in challenges if challenge["title"] not in challengesSolved]
        else:
            challenges = [challenge for challenge in challenges]
            
        if(len(challenges) == 0):
            await ctx.respond("There are no challenges with the paramaters you supplied!")
            return

        weightages = {chall["title"]: calculateWeightage(chall["solves"], chall["points"]) for chall in challenges}
        weightages = [k for k, _ in sorted(weightages.items(), key=lambda item: item[1])]

        if(difficulty == None):
            challenge = random.choice(challenges)
        else:
            if(difficulty == "easy"):
                weightages = weightages[:len(weightages) // 3 + 1]
            elif(difficulty == "medium"):
                weightages = weightages[len(weightages)//3 + 1:len(weightages)* 2 // 3]
            else:
                weightages = weightages[len(weightages) * 2 //3:]
            challenge = random.choice(weightages)
            for chall in challenges:
                if(chall["title"] == challenge):
                    challenge = chall
                    break
        
        embed = discord.Embed(
            title = f"{challenge['title']} ({challenge['category']['name']})",
            description = challenge["description"],
            color = discord.Colour.random()
        )

        embed.add_field(name = "Points", value = challenge["points"])
        embed.add_field(name = "Solves", value = challenge["solves"])
        
        view = DefaultView()
        for i, f in enumerate(challenge["files"]):
            view.add_item(DefaultButton(label=f["title"], style=discord.ButtonStyle.link, url=f["url"].replace(' ', '%20')))

        await ctx.respond(embed = embed, view = view)
        

def setup(bot):
    bot.add_cog(misc(bot))
