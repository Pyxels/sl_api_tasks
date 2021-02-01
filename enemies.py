import os
import json
from config.config import config

DATA_PATH = os.path.join(config('PROJECT_PATH'), 'data')
PLAYER_NAME = config('PLAYER_NAME')


def add_enemies(new_battles, first_time=False):

    enemies_dict = {}

    # informational counters
    added_counter = 0
    exists_counter = 0

    # dont load a non existant file if this is the first time loading
    if not first_time:
        with open(os.path.join(DATA_PATH, 'enemies_list.json'), "r") as f:
            enemies_dict = json.load(f)

    # for each battle in the battle list, get the enemy and the winner
    for battle in new_battles:
        enemy = battle["player_1"] if battle["player_1"] != PLAYER_NAME else battle["player_2"]
        winner = 1 if battle["winner"] == PLAYER_NAME else 0

        # if the enemy already has an entry, increment values
        if enemy in enemies_dict:
            exists_counter += 1
            enemies_dict[enemy]["battles_won"] += winner
            enemies_dict[enemy]["battles"] += 1
        else:
            added_counter += 1
            enemies_dict[enemy] = {
                "battles_won": winner,
                "battles": 1}

    print(f"{added_counter} new enemies were added and {exists_counter} already existed.")

    # save this updated dict
    _save_to_file(enemies_dict)


def _save_to_file(new_dict):
    # sort the dict by number of battles
    sorted_dict = dict(
        sorted(new_dict.items(), key=lambda item: item[1]["battles"], reverse=True))

    # save
    with open(os.path.join(DATA_PATH, 'enemies_list.json'), "w") as f:
        f.write(json.dumps(sorted_dict))


def _get_first_enemies():

    # get all the battles
    with open(os.path.join(DATA_PATH, 'sl_battle_hist.json'), "r") as f:
        battle_data = json.load(f)

    add_enemies(battle_data["battles"], first_time=True)


# run only once to initialize
if __name__ == '__main__':
    try:
        _get_first_enemies()
    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())