import requests
from decouple import config

PLAYER_NAME = config('PLAYER_NAME')
HOOK_URL = config('QUEST_HOOK_URL')

def check_quest():
    pass



if __name__ == "__main__":
    check_quest()
