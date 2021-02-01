import os
import json
from config.config import config
from db_interface.db_interface import open_conn, close_conn
from notification.discord import send_notification

PLAYER_NAME = config('PLAYER_NAME')

def add_enemies(new_battles, db, cursor):

    for battle in new_battles:

        # for each battle in the battle list, get the enemy and the winner
        enemy = battle[0] if battle[0] != PLAYER_NAME else battle[1]
        winner = 1 if battle[2] == PLAYER_NAME else 0

        cursor.execute(f"INSERT INTO Enemies (name, battles, battles_won) VALUES ('{enemy}', 1, {winner}) \
                       ON DUPLICATE KEY UPDATE battles=battles+1, battles_won=battles_won+{winner};")

    print("commiting ...")
    db.commit()



def _get_first_enemies():

    db, cursor = open_conn()

    # get from db
    cursor.execute("SELECT player_1, player_2, winner FROM Battles;")

    add_enemies(cursor.fetchall(), db, cursor)

    close_conn(db, cursor)


# run only once to initialize
if __name__ == '__main__':
    try:
        _get_first_enemies()
    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())

        send_notification("An Error occured in enemies.", 'error')
