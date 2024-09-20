# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot
import sys
import os

import utilities.utilities as utilities

MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../../"))
)
sys.path.append(MasterCryptoFarmBot_Dir)


import utils.logColors as lc


class FarmBot:
    def __init__(
        self,
        log,
        bot_globals,
        account_name,
        web_app_url,
        proxy=None,
        user_agent=None,
        tg=None,
    ):
        self.log = log
        self.bot_globals = bot_globals
        self.account_name = account_name
        self.web_app_url = web_app_url
        self.proxy = proxy
        self.tg = tg
        self.user_agent = user_agent

    async def run(self):
        if utilities.IsModuleDisabled(self.bot_globals, self.log):
            self.log.info(
                f"{lc.y}🚫 {self.bot_globals['module_name']} module is disabled!{lc.rs}"
            )
            utilities.KillProcess()

        self.log.info(
            f"{lc.g}🤖 Farming is starting for account {lc.rs + lc.c + self.account_name + lc.rs + lc.g}...{lc.rs}"
        )

        # If self.tg is not None, it means you can use Pyrogram...
        self.log.info(f"{lc.b}[Development Only] URL: {self.web_app_url}{lc.rs}")

        # Login and other codes here ...
