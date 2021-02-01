import requests
import json
from datetime import datetime, timedelta
from config.config import config
from time_functions.timer_function import time_function
from notification.discord import send_notification


PLAYER_NAME = config('PLAYER_NAME')
DISCORD_ID = config('DISCORD_ID')


@time_function("check_quest")
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
        send_notification(
            f"{DISCORD_ID} Sir, a new Quest awaits you.\n*{(quest_time + timedelta(hours=24)).time()}*", 'quest')
        # `Type: {quest_data['name']}`\n


if __name__ == "__main__":
    try:
        check_quest()
    except:
        send_notification("Quest Notifier encountered an error.", 'error')
