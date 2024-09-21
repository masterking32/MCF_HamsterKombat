# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import sys
import os
import json
import asyncio

import utilities.utilities as utilities
from FarmBot.FarmBot import FarmBot

MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../"))
)

sys.path.append(MasterCryptoFarmBot_Dir)

try:
    import utils.logColors as lc
    import utils.modules as modules
    from utils.tgAccount import tgAccount
    import config as cfg
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

async def CheckCD(log):
    log.info(f"{lc.y}🔄 Checking again in {utilities.getConfig('check_interval', 3600)} seconds ...{lc.rs}")
    await asyncio.sleep(utilities.getConfig("check_interval", 3600))

async def main():
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

    if utilities.IsModuleDisabled(bot_globals, log):
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

    if cfg.config["telegram_api"]["api_id"] == 1234 or cfg.config["telegram_api"]["api_hash"] == "":
        log.error(f"{lc.r}🔴 Please add your Telegram API ID and API Hash to the config.py file!{lc.rs}")
        exit(1)

    bot_globals["telegram_api_id"] = cfg.config["telegram_api"]["api_id"]
    bot_globals["telegram_api_hash"] = cfg.config["telegram_api"]["api_hash"]

    while True:
        if utilities.IsModuleDisabled(bot_globals, log):
            log.info(f"{lc.y}🚫 {module_name} module is disabled!{lc.rs}")
            utilities.KillProcess()

        for account in Accounts:
            if "disabled" in account and account["disabled"]:
                log.info(f"{lc.y}❌ Account {account['session_name']} is disabled!{lc.rs}")
                continue

            tg = tgAccount(bot_globals, log, account['session_name'], account['proxy'], "myuseragent_bot", "ref_masterking32", None, "https://api.masterking32.com/telegram_useragent.php")
            tgRunStatus = await tg.run()
            if not tgRunStatus:
                log.error(f"{lc.r}❌ Account {account['session_name']} is not ready!{lc.rs}")
                continue

            # Your checks here before getting the webview data, if needed

            web_app_data = await tg.getWebViewData()
            if not web_app_data:
                log.error(f"{lc.r}❌ Account {account['session_name']} is not ready!{lc.rs}")
                await tg.DisconnectClient()
                continue

            log.info(f"{lc.g}└─ ✅ Account {account['session_name']} is ready!{lc.rs}")
            FB = FarmBot(log, bot_globals, account['session_name'], web_app_data, account['proxy'], account['user_agent'], tg)
            await FB.run()

            await tg.DisconnectClient()

        if not os.path.exists("accounts.json"):
            await CheckCD(log)
            continue

        log.info(f"{lc.g}👤 Checking for accounts without PyroGram ...")
        JSON_Accounts = None
        with open("accounts.json", "r") as f:
            JSON_Accounts = json.load(f)

        if not JSON_Accounts or len(JSON_Accounts) == 0:
            log.info(f"{lc.y}└─ 🔄 No accounts found!{lc.rs}")
            await CheckCD(log)
            continue

        for account in JSON_Accounts:
            proxy = None if "proxy" not in account else account["proxy"]
            account_name = account["session_name"] if "session_name" in account else account["phone_number"]
            web_app_data = account["web_app_data"] if "web_app_data" in account else None
            user_agent = account["user_agent"] if "user_agent" in account else None
            if "disabled" in account and account["disabled"]:
                log.info(f"{lc.y}❌ Account {account_name} is disabled!{lc.rs}")
                continue

            FB = FarmBot(log, bot_globals, account_name, web_app_data, proxy, user_agent, None)
            await FB.run()

        await CheckCD(log)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
        print("Exiting ...")
        exit(0)
    except Exception as e:
        print(e)
        exit(1)
