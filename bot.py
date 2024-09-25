# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import signal
import sys
import os
import json
import asyncio
from pathlib import Path

import utilities.utilities as utilities
from FarmBot.FarmBot import FarmBot

# Constants
CHECK_INTERVAL = utilities.getConfig("check_interval", 3600)
MASTER_CRYPTO_FARM_BOT_DIR = Path(__file__).resolve().parents[2]
ACCOUNTS_FILE = MASTER_CRYPTO_FARM_BOT_DIR / "telegram_accounts/accounts.json"
CONFIG_ERROR_MSG = (
    "\033[31mThis module is designed for MasterCryptoFarmBot.\033[0m\n"
    "\033[31mYou cannot run this module as a standalone application.\033[0m\n"
    "\033[31mPlease install MasterCryptoFarmBot first, then place this module inside the modules directory.\033[0m\n"
    "\033[31mGitHub: \033[0m\033[32mhttps://github.com/masterking32/MasterCryptoFarmBot\033[0m"
)

sys.path.append(str(MASTER_CRYPTO_FARM_BOT_DIR))

try:
    import utils.logColors as lc
    from utils.tgAccount import tgAccount
    import config as cfg
except Exception as e:
    print(CONFIG_ERROR_MSG)
    exit(1)


async def check_cd(log):
    log.info(f"<y>💤 Checking again in </y><c>{CHECK_INTERVAL}</c><y> seconds ...</y>")
    await asyncio.sleep(CHECK_INTERVAL)


async def load_accounts(log):
    if not ACCOUNTS_FILE.exists():
        log.info("<y>└─ 🟠 No Pyrogram account found.</y>")
        return []

    with open(ACCOUNTS_FILE, "r") as f:
        accounts = json.load(f)

    if not accounts:
        log.info("<y>└─ 🟠 No Pyrogram account found.</y>")
        return []

    log.info(
        "<g>└─ 👤</g><c>"
        + str(len(accounts))
        + "</c><g> Pyrogram account(s) found!</g>"
    )
    return accounts


async def process_pg_account(account, bot_globals, log):
    if "disabled" in account and account["disabled"]:
        log.info(f"<y>❌ Account {account['session_name']} is disabled!</y>")
        return

    tg = tgAccount(
        bot_globals,
        log,
        account["session_name"],
        account["proxy"],
        "myuseragent_bot",
        "ref_masterking32",
        None,
        "https://api.masterking32.com/telegram_useragent.php",
    )
    tg_run_status = await tg.run()
    if not tg_run_status:
        log.error(f"<r>└─ ❌ Account {account['session_name']} is not ready!</r>")
        return

    web_app_data = await tg.getWebViewData()
    if not web_app_data:
        log.error(f"<r>└─ ❌ Account {account['session_name']} is not ready!<r>")
        await tg.DisconnectClient()
        return

    web_app_query = tg.getTGWebQuery(web_app_data)
    if not web_app_query:
        log.error(
            f"<r>└─ ❌ Account {account['session_name']} WebApp query is not valid!</r>"
        )
        await tg.DisconnectClient()
        return

    log.info(f"<g>└─ ✅ Account {account['session_name']} is ready!</g>")
    fb = FarmBot(
        log,
        bot_globals,
        account["session_name"],
        web_app_query,
        account["proxy"],
        account["user_agent"],
        tg,
    )
    await fb.run()
    await tg.DisconnectClient()


async def main():
    module_dir = Path(__file__).resolve().parent
    module_name = module_dir.name
    log = lc.getLogger(str(module_dir / "bot.log"), module_name)
    log.info(f"<g>🔧 {module_name} module is starting ...</g>")

    bot_globals = {
        "module_name": module_name,
        "mcf_dir": str(MASTER_CRYPTO_FARM_BOT_DIR),
        "module_dir": str(module_dir),
    }

    if utilities.is_module_disabled(bot_globals, log):
        log.info(f"<r>🚫 {module_name} module is disabled!</r>")
        exit(0)

    log.info("<g>👤 Checking for Pyrogram accounts ...</g>")
    accounts = await load_accounts(log)

    if (
        accounts
        and cfg.config["telegram_api"]["api_id"] == 1234
        or not cfg.config["telegram_api"]["api_hash"]
    ):
        log.error(
            f"<r>🔴 Please add your Telegram API ID and API Hash to the config.py file!</r>"
        )
        exit(1)

    bot_globals["telegram_api_id"] = cfg.config["telegram_api"]["api_id"]
    bot_globals["telegram_api_hash"] = cfg.config["telegram_api"]["api_hash"]

    while True:
        log.info("<g>🖥️ Start processing Pyrogram accounts ...</g>")
        for account in accounts:
            await process_pg_account(account, bot_globals, log)

        if not Path("accounts.json").exists():
            await check_cd(log)
            continue

        log.info("<g>👤 Checking for module accounts ...</g>")
        with open("accounts.json", "r") as f:
            json_accounts = json.load(f)

        if not json_accounts:
            log.info("<y>└─ 🟠 No module accounts found!</y>")
            await check_cd(log)
            continue

        tg_tmp = tgAccount()
        for account in json_accounts:
            proxy = account.get("proxy")
            account_name = account.get("session_name", account.get("phone_number"))
            web_app_data = account.get("web_app_data")

            user_agent = account.get("user_agent")
            if account.get("disabled"):
                log.info(f"<y>❌ Account {account_name} is disabled!</y>")
                continue

            if not web_app_data:
                log.error(f"<r>❌ Account {account_name} WebApp data is empty!</r>")
                continue

            web_app_query = tg_tmp.getTGWebQuery(web_app_data)
            if not web_app_query:
                log.error(
                    f"<r>❌ Account {account_name} WebApp query is not valid!</r>"
                )
                continue

            fb = FarmBot(
                log, bot_globals, account_name, web_app_data, proxy, user_agent, None
            )
            await fb.run()

        await check_cd(log)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{lc.r}🛑 Bot Module interrupted by user ...{lc.rs}")
        os.kill(os.getpid(), signal.SIGINT)
    except Exception as e:
        print(f"{lc.r}🛑 Bot Module stopped with an error: {e} ...{lc.rs}")
        os.kill(os.getpid(), signal.SIGINT)
