# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import sys
import os

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
    log = lc.getLogger()
    Modules = modules.Module(log)
    module_name = Modules.get_ModuleName()
    log.info(f"{lc.g}🔧 {module_name} module is running ...{lc.rs}")
    bot_globals = {"module_name": module_name, "mcf_dir": MasterCryptoFarmBot_Dir}

    db = Database(MasterCryptoFarmBot_Dir + "/database.db", log)
    is_module_disabled = Modules.is_module_disabled(db, module_name)
    db.Close()
    if is_module_disabled:
        log.info(f"{lc.y}🚫 {module_name} module is disabled!{lc.rs}")
        return


if __name__ == "__main__":
    main()
