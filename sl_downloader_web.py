import os
import requests
import json
from config.config import config
from time_functions.timer_function import time_function
from notification.discord import send_notification
from db_interface.db_interface import open_conn, close_conn

PLAYER_NAME = config('PLAYER_NAME')


@time_function("request_data")
def request_data():
    return requests.get(f"https://api.splinterlands.io/battle/history?player={PLAYER_NAME}"), requests.get(f"https://api.splinterlands.io/players/details?name={PLAYER_NAME}")


@time_function("as a whole")
def update_json():

    db, cursor = open_conn()

    # Getting the last 50 battles
    battles_response, power_response = request_data()

    # Printing the response of the api server
    print(battles_response, power_response)

    # Loading the JSON string data into a dictionary containing player and battles, which contains a list of dictionaries
    new_data = json.loads(battles_response.text)
    current_power = json.loads(power_response.text)["collection_power"]


    # add the new battles
    for new_battle in new_data["battles"]:
        
        if new_battle["match_type"] != "Ranked":
            break

        command = "INSERT IGNORE INTO Battles VALUES ("
        command += ", ".join([str(item) for item in new_battle])
        command += f", {current_power});"


        cursor.execute(command)

    db.commit()

    close_conn(db, cursor)


if __name__ == '__main__':
    try:
        update_json()
    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())

        send_notification("Downloader encountered an Error.", 'error')
