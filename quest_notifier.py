import time
import requests
import json
from datetime import datetime
from decouple import config


PLAYER_NAME = config('PLAYER_NAME')
HOOK_URL = config('QUEST_HOOK_URL')
DISCORD_ID = config('DISCORD_ID')


def check_quest():

    response = requests.get(
        f"https://api.splinterlands.io/players/quests?username={PLAYER_NAME}")

    # Loading the JSON string data into a dictionary
    quest_data = json.loads(response.text)[0]

    print(quest_data)

    # if the quest is finished, break
    if int(quest_data['completed_items']) != 0:
        return

    # extract the time out of the iso format datetime
    quest_time = datetime.fromisoformat(
        quest_data['created_date'].replace('Z', '')).time()

    requests.post(
        HOOK_URL, data={'content': f"{DISCORD_ID} Sir, a new Quest awaits you.\n`Type: {quest_data['name']}`\n*{quest_time}*"})


starting_time = time.perf_counter()
if __name__ == "__main__":
    check_quest()
    print(f"Task took {time.perf_counter() - starting_time:0.4f} seconds")
