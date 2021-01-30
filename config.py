import os
import sys
import json

# gets the given environment variable saved in the .env file
def config(variable):
    with open(os.path.join(sys.path[0], '.env'), "r") as f:
        env_vars = json.load(f)

    return env_vars[variable]
