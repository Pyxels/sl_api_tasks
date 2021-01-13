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

    # if the quest is finished, break
    if int(quest_data['total_items']) == int(quest_data['completed_items']):
        return

    # extract the time out of the iso format datetime
    time = datetime.fromisoformat(
        quest_data['created_date'].replace('Z', '')).time()

    requests.post(
        HOOK_URL, data={'content': f"{DISCORD_ID} Sir, a new Quest awaits you.\n`Type: {quest_data['name']}`\n*{time}*"})


if __name__ == "__main__":
    check_quest()
