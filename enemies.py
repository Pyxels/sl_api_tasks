import os
import json
from config.config import config
from db_interface.db_interface import *

DATA_PATH = os.path.join(config('PROJECT_PATH'), 'data')
PLAYER_NAME = config('PLAYER_NAME')


def add_enemies(new_battles, db, cursor):

    # informational counters
    added_counter = 0
    exists_counter = 0

    # load the existing enemies from db
    cursor.execute("SELECT name, battles, battles_won FROM Enemies;")
    enemies_list = cursor.fetchall()

    for battle in new_battles:

        # for each battle in the battle list, get the enemy and the winner
        enemy = battle[0] if battle[0] != PLAYER_NAME else battle[1]
        winner = 1 if battle[2] == PLAYER_NAME else 0

        # increment values if enemy already existed
        was_added = False
        for entry in enemies_list:
            if enemy == entry[0]:
                cursor.execute(f"UPDATE Enemies SET battles={int(entry[1]) + 1}, battles_won={int(entry[2]) + winner} WHERE name='{enemy}';")
                exists_counter += 1
                was_added = True
                break

        if not was_added:
            new_tuple = (enemy, 1, winner)
            enemies_list.append(new_tuple)
            cursor.execute(f"INSERT INTO Enemies (name, battles, battles_won) VALUES ('{enemy}', 1, {winner});")
            added_counter += 1

    print(f"{added_counter} new enemies were added and {exists_counter} already existed.")

    db.commit()



def _get_first_enemies():

    db, cursor = open_conn()

    # get from db
    cursor.execute("SELECT player_1, player_2, winner FROM Battles;")

    add_enemies(cursor.fetchall(), db, cursor)


# run only once to initialize
if __name__ == '__main__':
    try:
        _get_first_enemies()
    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
