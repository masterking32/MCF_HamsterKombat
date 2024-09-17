# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import os
import json


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
