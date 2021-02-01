import requests
from config.config import config

DOWNLOAD_URL = config("API_HOOK_URL")
QUEST_URL = config("QUEST_HOOK_URL")
ERROR_URL = config("ERROR_HOOK_URL")


def send_notification(message, destination='download'):

    if destination == "download":
        url = DOWNLOAD_URL
    elif destination == 'quest':
        url = QUEST_URL
    elif destination == "error":
        url = ERROR_URL

    requests.post(url, data={"content": message})
