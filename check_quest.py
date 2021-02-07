import os
import requests
import json
from datetime import datetime, timedelta
from config.config import config
from time_functions.timer_function import time_function
from notification.discord import send_notification


PLAYER_NAME = config('PLAYER_NAME')
USERNAME = os.getenv('USERNAME')
TOKEN = os.getenv('API_TOKEN')


@time_function("'update quest task time'")
def check_quest():

    sl_response = requests.get(
        f"https://api.splinterlands.io/players/quests?username={PLAYER_NAME}")

    print("Splinterlands:", sl_response)

    # Loading the JSON string data into a dictionary
    quest_data = json.loads(sl_response.text)[0]

    # extract datetime object our of the string
    quest_time = datetime.fromisoformat(
        quest_data['created_date'].replace('Z', ''))

    quest_time += timedelta(hours=23)

    # set the task to the time of next quest + 5 mins
    pa_response = requests.patch(
        f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/schedule/206141/',
        headers={'Authorization': f'Token {TOKEN}'},
        data={'hour': quest_time.hour, 'minute': (quest_time.minute + 5)}
    )

    print("PythonAnywhere:", pa_response)
    print(f"Changed times to {quest_time.hour}:{quest_time.minute +5}.")


if __name__ == "__main__":
    try:
        check_quest()
    except:
        send_notification("Quest Checker encountered an error.", 'error')
