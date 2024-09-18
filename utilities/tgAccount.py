# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import os
import sys
import random
import string
import time

MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../../"))
)
sys.path.append(MasterCryptoFarmBot_Dir)
from pyrogram import Client
from pyrogram.raw.types import InputBotAppShortName
from pyrogram.raw import functions
from pyrogram.raw.functions.messages import RequestWebView, RequestAppWebView
from urllib.parse import unquote
import utilities.utilities as ut
import utils.logColors as lc


class tgAccount:
    def __init__(self, bot_globals, log, accountName):
        self.bot_globals = bot_globals
        self.log = log
        self.accountName = accountName
        self.tgClient = None

    async def Connect(self):
        if self.tgClient is not None and self.tgClient.is_connected:
            return self.tgClient

        self.tgClient = Client(
            name=self.accountName,
            api_id=self.bot_globals["telegram_api_id"],
            api_hash=self.bot_globals["telegram_api_hash"],
            workdir=self.bot_globals["mcf_dir"] + "/telegram_accounts",
            plugins=dict(root="bot/plugins"),
        )

        self.log.info(f"{lc.g}└─ 🌍 Connecting {self.accountName} session ...{lc.rs}")
        try:
            isConnected = await self.tgClient.connect()
            if isConnected:
                return self.tgClient
            else:
                return None
        except Exception as e:
            self.log.error(f"└─ ❌ {e}")
            return None

    async def run(self):
        try:
            self.log.info(f"{lc.g}🤖 Running {self.accountName} account ...{lc.rs}")
            if not os.path.exists(
                self.bot_globals["mcf_dir"]
                + f"/telegram_accounts/{self.accountName}.session"
            ):
                self.log.error(
                    f"{lc.r}❌ Account {self.accountName} session is not found!{lc.rs}"
                )
                return None

            self.log.info(f"{lc.g}└─ 🔑 Loading {self.accountName} session ...{lc.rs}")

            tgClient = await self.Connect()
            if tgClient is None:
                self.log.error(
                    f"{lc.r}└─ ❌ Account {self.accountName} session is not connected!{lc.rs}"
                )
                return None
            else:
                self.log.info(
                    f"{lc.g}└─ 🔑 {self.accountName} session is loaded successfully!{lc.rs}"
                )

            await self.accountSetup()

            referral = ut.getConfig("referral_token", "masterking32")
            BotID = "myuseragent_bot"

            bot_started = False
            try:
                async for message in self.tgClient.get_chat_history(BotID):
                    if "/start" in message.text:
                        bot_started = True
                        break
            except Exception as e:
                pass

            if not bot_started:
                peer = await self.tgClient.resolve_peer(BotID)
                await self.tgClient.invoke(
                    functions.messages.StartBot(
                        bot=peer,
                        peer=peer,
                        random_id=random.randint(100000, 999999),
                        start_param=referral,
                    )
                )

            peer = await tgClient.resolve_peer(BotID)
            # bot_app = InputBotAppShortName(bot_id=peer, short_name="app")
            web_view = await tgClient.invoke(
                # RequestAppWebView(
                #     peer=peer,
                #     app=bot_app,
                #     platform="android",
                #     write_allowed=True,
                #     start_param=referral,
                # )
                RequestWebView(
                    peer=peer,
                    bot=peer,
                    platform="android",
                    from_bot_menu=False,
                    url="https://api.masterking32.com/telegram_useragent.php",
                )
            )

            auth_url = web_view.url
            web_data = unquote(
                string=auth_url.split("tgWebAppData=", maxsplit=1)[1].split(
                    "&tgWebAppVersion", maxsplit=1
                )[0]
            )

            self.log.info(
                f"{lc.g}└─ 🔑 {self.accountName} session is authorized!{lc.rs}"
            )

            return web_data
        except Exception as e:
            self.log.error(
                f"{lc.r}└─ ❌ {self.accountName} session failed to authorize!{lc.rs}"
            )
            self.log.error(f"{lc.r}└─ ❌ {e}{lc.rs}")
            return None

    async def accountSetup(self):
        tgClient = await self.Connect()
        if tgClient is None:
            self.log.error(
                f"{lc.r}└─ ❌ Account {self.accountName} session is not connected!{lc.rs}"
            )
            return None

        try:
            UserAccount = await tgClient.get_me()
            if not UserAccount.username:
                self.log.info(
                    f"{lc.g}└─ 🗿 Account username is empty. Setting a username for the account...{lc.rs}"
                )
                setUsername = False
                maxTries = 5
                while not setUsername and maxTries > 0:
                    RandomUsername = "".join(
                        random.choices(string.ascii_lowercase, k=random.randint(15, 30))
                    )
                    self.log.info(
                        f"{lc.g}└─ 🗿 Setting username for {self.accountName} session, New username {lc.rs + lc.c + RandomUsername + lc.rs}"
                    )
                    setUsername = await tgClient.set_username(RandomUsername)
                    maxTries -= 1
                    await time.sleep(5)
            await self.joinChat("MasterCryptoFarmBot", True)
            self.log.info(
                f"{lc.g}└─ ✅ Account {self.accountName} session is setup successfully!{lc.rs}"
            )

        except Exception as e:
            self.log.error(
                f"{lc.r}└─ ❌ Account {self.accountName} session is not setup!{lc.rs}"
            )
            self.log.error(f"{lc.r}└─ ❌ {e}{lc.rs}")
            return None

    async def joinChat(self, url, noLog=False):
        if not noLog:
            self.log.info(
                f"{lc.g}└─ 📰 Joining {lc.rs + lc.c + url + lc.rs + lc.g} ...{lc.rs}"
            )
        tgClient = await self.Connect()
        if tgClient is None:
            if noLog:
                return None
            self.log.error(
                f"{lc.r}└─ ❌ Account {self.accountName} session is not connected!{lc.rs}"
            )
            return None

        try:
            await tgClient.join_chat(url)

            if noLog:
                return None

            self.log.info(
                f"{lc.g}└─ ✅ {lc.rs + lc.c + url + lc.rs + lc.g} has been joined successfully!{lc.rs}"
            )
            return True
        except Exception as e:
            if noLog:
                return None

            self.log.error(
                f"{lc.r}└─ ❌ {lc.rs + lc.c + url + lc.rs + lc.r} failed to join!{lc.rs}"
            )
            self.log.error(f"{lc.r}❌ {e}{lc.rs}")
            return False

    async def DisconnectClient(self):
        if self.tgClient is not None and self.tgClient.is_connected:
            self.log.info(f"└─ 💻 Disconnecting {self.accountName} session ...")
            await self.tgClient.disconnect()
            self.log.info(
                f"{lc.g}└─── ❌ {self.accountName} session has been disconnected successfully!{lc.rs}"
            )
        return True
