import time
import requests
import json
from datetime import datetime, timedelta
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

    # if the quest is not finished, break
    if int(quest_data['completed_items']) != int(quest_data["total_items"]):
        return

    # extract datetime object our of the string
    quest_time = datetime.fromisoformat(
        quest_data['created_date'].replace('Z', ''))

    # checks to see if 23 hours have passed after last quest was created
    if datetime.now() > (quest_time + timedelta(hours=23)):
        # send discord notification; + 24 is due to easy fix of timezone +1 for me
        requests.post(
            HOOK_URL, data={'content': f"{DISCORD_ID} Sir, a new Quest awaits you.\n*{(quest_time + timedelta(hours=24)).time()}*"})
        # `Type: {quest_data['name']}`\n


starting_time = time.perf_counter()
if __name__ == "__main__":
    check_quest()
    print(f"Task took {time.perf_counter() - starting_time:0.4f} seconds")
