import requests
import json
from decouple import config
from get_enemies import add_enemies

PATH = config('BATTLES_PATH')
HOOK_URL = config('API_HOOK_URL')
PLAYER_NAME = config('PLAYER_NAME')
DISCORD_ID = config('DISCORD_ID')


def update_json():

    newCount = 0
    battles_to_add = []

    # Getting the last 50 battles
    response = requests.get(
        f"https://api.splinterlands.io/battle/history?player={PLAYER_NAME}")

    # Printing the response of the api server
    print(response)

    # Loading the JSON string data into a dictionary containing player and battles, which contains a list of dictionaries
    new_data = json.loads(response.text)

    # Getting the historic data saved so far as old_data
    with open(PATH, "r") as f:
        old_data = json.load(f)

    # checking if the new data from the api already
    # exists in the data file
    for new_battle in new_data["battles"]:
        for old_battle in old_data["battles"]:
            if new_battle["battle_queue_id_1"] == old_battle["battle_queue_id_1"]:
                new = False
                break
            else:
                new = True
        # check if new game is ranked, nothing but ranked is to be added
        if new and new_battle["match_type"] == "Ranked":
            print("New from {} added".format(new_battle["created_date"]))
            # old_data["battles"].append(new_battle)
            battles_to_add.append(new_battle)
            newCount += 1

    # add the new battles to the old data and extend enemies list
    old_data["battles"].extend(battles_to_add)
    add_enemies(battles_to_add)

    # removing non ranked battles (unrepresentative)
    """ for battle in old_data["battles"]:
        if battle["match_type"] != "Ranked":
            print("Removed non Ranked from {}".format(battle["created_date"]))
            old_data["battles"].remove(battle)
            newCount -= 1 """

    print("{} Battles added".format(newCount))
    print("{} Battles in total".format(len(old_data["battles"])))

    # if any battles were added, send a discord notification using web hooks
    if (newCount > 0):
        print("Sending Notification to Discord")
        requests.post(
            HOOK_URL, data={"content": f"{DISCORD_ID} Sir, there were *{newCount}* new Battles added. That makes **{len(old_data['battles'])}** in total."})
    # sorting by date, newest at the top
    old_data["battles"].sort(
        key=lambda item: item.get("created_date"), reverse=True)

    # overwriting the history file
    with open(PATH, "w") as f:
        f.write(json.dumps(old_data))


if __name__ == '__main__':
    try:
        update_json()
    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
