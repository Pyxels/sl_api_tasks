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
    print(
        f"Battle history: {battles_response} \Player details: {power_response}")

    # Loading the JSON string data into a dictionary containing player and battles, which contains a list of dictionaries
    new_data = json.loads(battles_response.text)
    current_power = json.loads(power_response.text)["collection_power"]

    # add the new battles
    for battle in new_data["battles"]:

        if battle["match_type"] != "Ranked":
            break

        command = 'INSERT IGNORE INTO Battles'
        command += f' VALUES ("{battle["battle_queue_id_1"]}", "{battle["battle_queue_id_2"]}", {battle["player_1_rating_initial"]}, {battle["player_2_rating_initial"]}, "{battle["winner"]}", {battle["player_1_rating_final"]}, {battle["player_2_rating_final"]}, {json.dumps(battle["details"])}, "{battle["player_1"]}", "{battle["player_2"]}", "{battle["created_date"]}", "{battle["match_type"]}", {battle["mana_cap"]}, {battle["current_streak"]}, "{battle["ruleset"]}", "{battle["inactive"]}", {json.dumps(battle["settings"])}, {battle["block_num"]}, {battle["rshares"]}, {json.dumps(battle["dec_info"])}, {battle["leaderboard"]}'
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
