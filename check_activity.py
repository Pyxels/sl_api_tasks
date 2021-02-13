from datetime import date
from db_interface.db_interface import open_conn, close_conn
from notification.discord import send_notification
from time_functions.timer_function import time_function


@time_function("'check_activity'")
def check_activity():
    db, cursor = open_conn()

    cursor.execute(
        "SELECT created_date FROM Battles ORDER BY created_date DESC LIMIT 1;")

    last_played = cursor.fetchone()[0]

    db_date = last_played.split("T")[0]

    if db_date != date.today().isoformat():
        send_notification("No new games were added today", 'error')
        print("Have you been playing? Last game: ", last_played)

    close_conn(db, cursor)


if __name__ == '__main__':
    try:
        check_activity()
    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())

        send_notification("Downloader encountered an Error.", 'error')
