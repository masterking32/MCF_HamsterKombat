# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot
import sys
import os


MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../../"))
)
sys.path.append(MasterCryptoFarmBot_Dir)
from .core.HttpRequest import HttpRequest
from .core.Auth import Auth
from .core.Basic import Basic


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

            account_info = auth.get_account_info()
            if account_info is None:
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

            totalDiamonds_Short = "{:.2f}".format(totalDiamonds)
            balanceDiamonds_Short = "{:.2f}".format(balanceDiamonds)
            earnPassivePerHour_Short = "{:.2f}".format(earnPassivePerHour)
            self.log.info(
                f"<g>🔷 Total Diamonds: <c>{totalDiamonds_Short}</c>, Balance Diamonds: <c>{balanceDiamonds_Short}</c>, Earn Passive Per Hour: <c>{earnPassivePerHour_Short}</c></g>"
            )

            # get-promos
            # config
            # upgrades-for-buy
            # list-tasks
            # get-skin
            # Start Farming ...
        except Exception as e:
            self.log.error(f"<r>❌ Error running FarmBot: {e}</r>")
            return False
