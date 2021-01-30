import json
import matplotlib.pyplot as plt
from config import config


DATA_PATH = config('DATA_PATH')

ratings = []
power_list = []


def generate_lists():

    with open(f"{DATA_PATH}sl_battle_hist.json", "r") as f:
        battles = json.load(f)["battles"]

    # get the ratings and save them to a list 
    for battle in battles:
        ratings.insert(0, int(battle["player_1_rating_final"] if battle["player_1"]
                              == "pyxels" else int(battle["player_2_rating_final"])))

        # if the battle has a power value (added 28.01.21) add that to a new key
        if "power" in battle:
            power_list.insert(0, battle["power"])
        else:
            power_list.insert(0, None)

    print(f"Number of ratings: {len(ratings)}")
    print(f"Number of powers: {len(power_list) - 1303}")


def generate_graph():

    plt.figure(figsize=(20, 10))

    ratings_plot = plt.gca()
    power_plot = ratings_plot.twinx()

    ratings_plot.plot(ratings)
    power_plot.plot(power_list, color='red')

    # ymin, ymax = ratings_plot.getylim()

    ratings_plot.axhline(y=100, color='darkgoldenrod', linestyle=':')
    ratings_plot.axhline(y=400, color='darkgoldenrod', linestyle=':')
    ratings_plot.axhline(y=700, color='darkgoldenrod', linestyle=':')

    ratings_plot.axhline(y=1000, color='gray')
    ratings_plot.axhline(y=1300, color='gray', linestyle=':')
    ratings_plot.axhline(y=1600, color='gray', linestyle=':')

    ratings_plot.axhline(y=1900, color='gold', linestyle='--')

    ratings_plot.set_xlabel('battles')
    ratings_plot.set_ylabel('rating')
    power_plot.set_ylabel('power')
    plt.title('Rating over time')

    # plt.show()
    plt.savefig(f"{DATA_PATH}ratings_graph.png")


if __name__ == "__main__":
    try:
        generate_lists()
        generate_graph()
    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
