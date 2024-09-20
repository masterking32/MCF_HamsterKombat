# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import os
import json
import signal
import sys
import os

MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../../"))
)
sys.path.append(MasterCryptoFarmBot_Dir)

from utils.database import Database


# Get the value of a key from the bot_settings.json file
def getConfig(key, default=None):
    if not os.path.exists("bot_settings.json"):
        return default

    with open("bot_settings.json", "r") as f:
        data = json.load(f)
        if key in data:
            return data[key]
        else:
            return default


def IsModuleDisabled(bot_globals, log):
    db = Database(bot_globals["mcf_dir"] + "/database.db", log)
    module_name = bot_globals["module_name"]
    is_disabled = db.getSettings(f"{module_name}_disabled", "0") == "1"
    db.Close()
    return is_disabled == True or is_disabled == "1"


def KillProcess():
    try:
        os.kill(os.getpid(), signal.SIGINT)
    except Exception as e:
        pass
    try:
        os.kill(os.getpid(), signal.SIGTERM)
    except Exception as e:
        pass
    exit(0)
