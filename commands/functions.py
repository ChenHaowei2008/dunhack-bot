import time
from bs4 import BeautifulSoup
import json
import requests
from PIL import Image
from fuzzywuzzy import fuzz

async def scrapeChallenges(cookies):
    r = requests.get("https://dunhack.me/challenges", cookies=cookies, verify=False)

    soup = BeautifulSoup(r.text, "html.parser")
    data = soup.find(id="__NEXT_DATA__").string
    with open("data/challenges.json", "w") as file:
        file.write(str(data))

async def scrapeScoreboard(cookies):
    r = requests.get("https://dunhack.me/scoreboard", cookies=cookies, verify=False)
    
    soup = BeautifulSoup(r.text, "html.parser")
    data = soup.find(id="__NEXT_DATA__").string
    with open("data/users.json", "w") as file:
        file.write(str(data))

async def scrapeUsernames(cookies, usernames=None):
    session = requests.Session()
    if(usernames == None):
        with open("data/scoreboard.json", "r") as file:
            contents = file.read().strip()
        contents = json.loads(contents)
        usernames = [entry['username'] for entry in contents["props"]["pageProps"]["scores"]]

    for user in usernames:
        # Prevent accidentally ddosing the dunhack servers.
        time.sleep(0.5)
        url = "https://dunhack.me/users/" + user 
        r = session.get(url, cookies=cookies, verify=False)
        if(r.status_code != 200):
            return user + " not found!"
        soup = BeautifulSoup(r.text, "html.parser")
        data = soup.find(id="__NEXT_DATA__").string
        with open("data/users/" + user + ".json", "w") as file:
            file.write(str(data))

def getUsernames():
    with open("data/scoreboard.json", "r") as file:
        contents = file.read().strip()
    contents = json.loads(contents)
    usernames = [entry['username'] for entry in contents["props"]["pageProps"]["scores"]]

    return usernames


#copied this from https://stackoverflow.com/questions/29726148/finding-average-color-using-python#29726183
def getAverageColour(image):
    h = image.histogram()
    r = h[0:256]
    g = h[256:256*2]
    b = h[256*2: 256*3]
    #added one to all denominators to prevent divide by zero error
    return sum( i*w for i, w in enumerate(r) ) // (sum(r) + 1), sum( i*w for i, w in enumerate(g) ) // (sum(g) + 1), sum( i*w for i, w in enumerate(b) ) // (sum(b) +  1)

# For some reason, in dunhack the usernames are case sensitive, which is frankly stupid
def unsensitizeUsername(username, usernames):
    for user in usernames:
        if(user.lower() == username.lower()):
            return user

def processUsername(username: str):
    usernames = getUsernames()
    if(username.lower() in [a.lower() for a in usernames]):
        username = unsensitizeUsername(username, usernames)
        return username, None
    else:
        similar = []
        for user in usernames:
            if(fuzz.ratio(username, user) > 60):
                similar.append(user)
        
        output = "That username doesn't exist boss!"
        if(similar != []):
            output += f"\nDid you mean `{'` or `'.join(similar)}`?"
        return None, output

def calculateWeightage(solves, points):
    # some arbitrary function
    return ((20 - solves) * 4 + points * 2)