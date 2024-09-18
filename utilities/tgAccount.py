# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import os
from pyrogram import Client
from pyrogram.raw.types import InputBotAppShortName
from pyrogram.raw.functions.messages import RequestWebView, RequestAppWebView
from urllib.parse import unquote
import utilities.utilities as ut


class tgAccount:
    def __init__(self, bot_globals, log, accountName):
        self.bot_globals = bot_globals
        self.log = log
        self.accountName = accountName

    async def run(self):
        try:
            self.log.info(f"🤖 Running {self.accountName} account ...")
            if not os.path.exists(
                self.bot_globals["mcf_dir"]
                + f"/telegram_accounts/{self.accountName}.session"
            ):
                self.log.error(f"❌ Account {self.accountName} session is not found!")
                return None

            self.log.info(f"└─ 🔑 Loading {self.accountName} session ...")
            tgClient = Client(
                name=self.accountName,
                api_id=self.bot_globals["telegram_api_id"],
                api_hash=self.bot_globals["telegram_api_hash"],
                workdir=self.bot_globals["mcf_dir"] + "/telegram_accounts",
                plugins=dict(root="bot/plugins"),
            )

            self.log.info(f"└─ 🌍 Connecting {self.accountName} session ...")
            try:
                isConnected = await tgClient.connect()
                if isConnected:
                    self.log.info(
                        f"└─ 🔑 {self.accountName} session is loaded successfully!"
                    )
                else:
                    self.log.error(
                        f"└─ ❌ {self.accountName} session is not authorized!"
                    )
                    return None
            except Exception as e:
                self.log.error(f"└─ ❌ {self.accountName} session failed to load!")
                self.log.error(f"└─ ❌ {e}")
                return None

            peer = await tgClient.resolve_peer("myuseragent_bot")
            referral = ut.getConfig("referral_token", "masterking32")
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

            self.log.info(f"└─ 🔑 {self.accountName} session is authorized!")

            if tgClient.is_connected:
                self.log.info(f"└─ 💻 Disconnecting {self.accountName} session ...")
                await tgClient.disconnect()
                self.log.info(
                    f"└─── ❌ {self.accountName} session has been disconnected successfully!"
                )

            return web_data
        except Exception as e:
            self.log.error(f"└─ ❌ {self.accountName} session failed to authorize!")
            self.log.error(f"└─ ❌ {e}")
            return None
