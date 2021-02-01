import os
import json

# gets the given environment variable saved in the .env file
def config(variable):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'), "r") as f:
        env_vars = json.load(f)

    return env_vars[variable]
