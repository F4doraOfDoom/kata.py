from argparse import ArgumentParser
import requests
import asyncio
import aiohttp
import json
import sys

# Global CodeWars API URLs 
USAGE = "Usage: python kata.py <codewars_username> (NOTE: Case sensitive)"
USER_FORMAT = "https://www.codewars.com/api/v1/users/{}/code-challenges/completed?page=0"
CHALLENGES_FORMAT = "https://www.codewars.com/api/v1/code-challenges/{}"
OUTPUT = "{}: {} white, {} yellow, {} blue, {} purple. TOTAL: {}"

def parse_args():
    parser = ArgumentParser(description="Python program to extract a user's CodeWars points according to Beta")
    parser.add_argument("-u", "--user", help="CodeWar's username", required=True)
    parser.add_argument("-l", "--lang", "--language", help="Programming language (Example: Python, Javascript)", required=True)
    parser.add_argument("-v", "--verbose", help="Print the challenges as the script aquires their data", action="store_true")
    args = parser.parse_args()

    return str(args.user), str(args.lang).lower(), args.verbose

# Global Parameters
USERNAME, LANGUAGE, VERBOSE = parse_args()

# Global data structure
total_points = 0

point_def = {
    "white" : 1,
    "yellow": 2,
    "blue" : 3,
    "purple" : 4
}

solved = {
    "white" : 0,
    "yellow" : 0,
    "blue" : 0,
    "purple" : 0
}

async def get_challenge_info(session, challenge_id, challenge_name):
    """
        This async function uses the CodeWar's API to get challenges info to update database
    """
    global total_points
    async with session.get(CHALLENGES_FORMAT.format(challenge_id)) as response:
        challenge_data = json.loads(await response.text())
        total_points += point_def.get(challenge_data["rank"]["color"], 0)
        solved[challenge_data["rank"]["color"]] += 1
        if VERBOSE:
            print("Recieved {} points for {} ({})".format(point_def.get(challenge_data["rank"]["color"], 0), challenge_name, challenge_id))

async def main():
    """
        This is the main loop.
        Acquire information about the user, update information about each completed challenge
    """
    user_data = requests.get(USER_FORMAT.format(USERNAME)).json()
    async with aiohttp.ClientSession() as session:
        for challenge in user_data["data"]:
            if LANGUAGE in [x.lower() for x in challenge["completedLanguages"]]:
                await get_challenge_info(session, challenge["id"], challenge["name"])

if __name__ == "__main__":
    try:
        if not VERBOSE:
            print("Please wait")

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        COMPLETE = True
        print(OUTPUT.format(USERNAME, solved["white"], solved["yellow"], solved["blue"], solved["purple"], total_points))
    except:
        print(f"FATAL: {USERNAME} does not exist. (Note: names are case sensitive)")
