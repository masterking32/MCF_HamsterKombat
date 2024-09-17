# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import sys
import os
import json

from utilities.utilities import getConfig

MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../"))
)

sys.path.append(MasterCryptoFarmBot_Dir)

try:
    import utils.logColors as lc
    from utils.database import Database
    import utils.modules as modules
except Exception as e:
    print(f"\033[31mThis module is designed for MasterCryptoFarmBot.\033[0m")
    print(f"\033[31mYou cannot run this module as a standalone application.\033[0m")
    print(
        f"\033[31mPlease install MasterCryptoFarmBot first, then place this module inside the modules directory.\033[0m"
    )
    print(
        "\033[31mGitHub: \033[0m\033[32mhttps://github.com/masterking32/MasterCryptoFarmBot\033[0m"
    )
    exit(1)


def main():
    module_dir = os.path.dirname(os.path.abspath(__file__))
    log = lc.getLogger(module_dir + "/bot.log")
    Modules = modules.Module(log)
    module_name = Modules.get_ModuleName()
    log.info(f"{lc.g}🔧 {module_name} module is running ...{lc.rs}")

    bot_globals = {
        "module_name": module_name,
        "mcf_dir": MasterCryptoFarmBot_Dir,
        "module_dir": module_dir,
    }

    db = Database(MasterCryptoFarmBot_Dir + "/database.db", log)
    is_module_disabled = Modules.is_module_disabled(db, module_name)
    db.Close()
    if is_module_disabled:
        log.info(f"{lc.y}🚫 {module_name} module is disabled!{lc.rs}")
        exit(0)

    log.info(f"{lc.g}👤 Checking for Telegram accounts ...{lc.rs}")

    if not os.path.exists(MasterCryptoFarmBot_Dir + "/telegram_accounts/accounts.json"):
        log.error(f"{lc.r}└─ 🔴 Please add your telegram accounts first!{lc.rs}")
        exit(1)

    with open(MasterCryptoFarmBot_Dir + "/telegram_accounts/accounts.json", "r") as f:
        Accounts = json.load(f)

    if not Accounts or len(Accounts) == 0:
        log.error(f"{lc.r}└─ 🔴 Please add your telegram accounts first!{lc.rs}")
        exit(1)

    log.info(
        f"{lc.g}└─ 👤 {lc.rs + lc.c + "[" + str(len(Accounts)) + "]" + lc.rs + lc.g } Telegram account(s) found!{lc.rs}"
    )



if __name__ == "__main__":
    main()
