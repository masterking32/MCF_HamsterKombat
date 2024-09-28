# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot
import sys
import os

from utilities.utilities import getConfig

MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../../"))
)
sys.path.append(MasterCryptoFarmBot_Dir)

from .core.HttpRequest import HttpRequest
from .core.Auth import Auth
from .core.Basic import Basic
from .core.Cards import Cards
from .core.Tasks import Tasks


class FarmBot:
    def __init__(
        self,
        log,
        bot_globals,
        account_name,
        web_app_query,
        proxy=None,
        user_agent=None,
        isPyrogram=False,
        tgAccount=None,
    ):
        self.log = log
        self.bot_globals = bot_globals
        self.account_name = account_name
        self.web_app_query = web_app_query
        self.proxy = proxy
        self.user_agent = user_agent
        self.isPyrogram = isPyrogram
        self.tgAccount = tgAccount
        self.authUserId = None
        self.authToken = None

    async def run(self):
        try:
            self.log.info(
                f"<g>🤖 Farming is starting for account <cyan>{self.account_name}</cyan>...</g>"
            )

            self.http = HttpRequest(self.log, self.proxy, self.user_agent)
            basic = Basic(self.log, self.http)
            ip = basic.ip()
            if ip is None:
                return

            auth = Auth(self.log, self.http)
            login_data = auth.login(self.web_app_query)
            if login_data is None:
                return

            self.authUserId = login_data["authUserId"]
            self.authToken = login_data["authToken"]

            self.http.authToken = self.authToken

            account_info, interlude_config_version = auth.get_account_info()
            if account_info is None or interlude_config_version is None:
                return

            sync = basic.get_sync()
            if sync is None:
                return

            totalDiamonds = sync["totalDiamonds"]
            balanceDiamonds = sync["balanceDiamonds"]
            earnPassivePerHour = sync["earnPassivePerHour"]
            upgrades = sync["upgrades"]
            tasks = sync["tasks"]
            referralsCount = sync["referralsCount"]
            skin = sync["skin"]
            achievements = sync["achievements"]
            promos = sync["promos"]

            totalDiamonds_short = "{:.2f}".format(totalDiamonds)
            balanceDiamonds_short = "{:.2f}".format(balanceDiamonds)
            earnPassivePerHour_short = "{:.2f}".format(earnPassivePerHour)
            self.log.info(
                f"<g>🔷 Total Diamonds: <c>{totalDiamonds_short}💎</c>, Balance Diamonds: <c>{balanceDiamonds_short}💎</c>, Earn Passive Per Hour: <c>{earnPassivePerHour_short}</c></g>"
            )

            get_promos = basic.get_promos()
            if get_promos is None:
                return

            v_config_data = basic.get_version_config(interlude_config_version)
            if v_config_data is None or "config" not in v_config_data:
                return

            get_config = basic.get_config()
            if get_config is None or "dailyKeysMiniGames" not in get_config:
                return

            upgrades_for_buy = basic.get_upgrades_for_buy()
            if upgrades_for_buy is None:
                return

            list_tasks = basic.get_list_tasks()
            if list_tasks is None:
                return

            listing = basic.get_list(ip)
            if listing is None:
                return

            get_skin = basic.get_skin()
            if get_skin is None:
                return

            self.log.info(
                "<g>✅ Sending basic request to the server was successful!</g>"
            )

            cards = Cards(self.log, self.http)
            if getConfig("auto_upgrade", True):
                cards.start_upgrades(balanceDiamonds)
            else:
                self.log.info("<y>🔔 Auto upgrade is disabled!</y>")

            tasks = Tasks(
                self.log,
                self.http,
                v_config_data["config"]["tasks"],
                list_tasks["tasks"],
            )
            if getConfig("auto_tasks", True):
                tasks.start_tasks()
            else:
                self.log.info("<y>🔔 Auto tasks is disabled!</y>")

            self.log.info(
                f"<g>🤖 Farming is completed for account <cyan>{self.account_name}</cyan>!</g>"
            )
        except Exception as e:
            self.log.error(f"<r>❌ Error running FarmBot: {e}</r>")
            return False
