# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


class Basic:
    def __init__(self, log, HttpRequest):
        self.log = log
        self.http = HttpRequest

    def ip(self):

        self.log.info(f"🌍 <y>Getting IP ...</y>")
        response = self.http.get(
            url="/ip", Allowed_Option_Response_Code=200, with_Auth=False
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
