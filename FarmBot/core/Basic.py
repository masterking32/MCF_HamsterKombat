# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json


class Basic:
    def __init__(self, log, HttpRequest):
        self.log = log
        self.http = HttpRequest

    def ip(self):

        self.log.info(f"🌍 <y>Getting IP ...</y>")
        response = self.http.get(
            url="/ip", valid_option_response_code=200, auth_header=False
        )

        if response is None:
            self.log.error("🔴 <red>Failed to get IP!</red>")
            return None

        self.log.info(
            f"🌍 <g>IP: <y>{response['ip']}</y>, Country: <y>{response['country_code']}</y></g>"
        )

        return response

    def get_sync(self):
        self.log.info(f"🔄 <y>Getting sync ...</y>")

        response = self.http.post(
            url="interlude/sync",
        )

        if response is None or "interludeUser" not in response:
            self.log.error("🔴 <red>Failed to get sync!</red>")
            return None

        return response["interludeUser"]

    def get_promos(self):
        self.log.info(f"🔄 <y>Getting promos ...</y>")

        response = self.http.post(
            url="interlude/get-promos",
        )

        if response is None or "promos" not in response:
            self.log.error("🔴 <red>Failed to get promos!</red>")
            return None

        return response

    def get_config(self):
        self.log.info(f"🔄 <y>Getting config ...</y>")

        response = self.http.post(
            url="interlude/config",
        )

        if response is None or "dailyKeysMiniGames" not in response:
            self.log.error("🔴 <red>Failed to get config!</red>")
            return None

        return response

    def get_version_config(self, version):
        self.log.info(f"🔄 <y>Getting config <c>{version}</c> ...</y>")

        response = self.http.get(
            url=f"interlude/config/{version}",
        )

        if response is None and "config" not in response:
            self.log.error("🔴 <red>Failed to get config!</red>")
            return None

        return response

    def get_upgrades_for_buy(self):
        self.log.info(f"🔄 <y>Getting upgrades ...</y>")

        response = self.http.post(
            url="interlude/upgrades-for-buy",
        )

        if response is None or "upgradesForBuy" not in response:
            self.log.error("🔴 <red>Failed to get upgrades!</red>")
            return None

        return response

    def get_list_tasks(self):
        self.log.info(f"🔄 <y>Getting tasks ...</y>")

        response = self.http.post(
            url="interlude/list-tasks",
        )

        if response is None or "tasks" not in response:
            self.log.error("🔴 <red>Failed to get tasks!</red>")
            return None

        return response

    def get_skin(self):
        self.log.info(f"🔄 <y>Getting skin ...</y>")

        response = self.http.post(
            url="interlude/get-skin",
        )

        if response is None or "skins" not in response:
            self.log.error("🔴 <red>Failed to get skin!</red>")
            return None

        return response

    def get_list(self, ip_data):
        self.log.info(f"🔄 <y>Getting list ...</y>")

        response = self.http.post(
            url="interlude/withdraw/list",
            payload=json.dumps(
                {
                    "ipInfo": ip_data,
                }
            ),
        )

        if response is None:
            self.log.error("🔴 <red>Failed to get list!</red>")
            return None

        return response
