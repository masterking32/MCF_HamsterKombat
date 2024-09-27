# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import json
from utilities.hk import DetectOS, GenerateHKFingerprint


class Auth:
    def __init__(self, log, HttpRequest):
        self.log = log
        self.http = HttpRequest

    def login(self, web_app_query):
        self.log.info(f"🔑 <y>Logging in to HamsterKombat bot ...</y>")

        try:
            DetectedOS = DetectOS(self.http.user_agent)
            self.log.info(f"📱 <g> Logging in as <y>{DetectedOS}</y> device!</g>")
            HKFingerprint = GenerateHKFingerprint(DetectedOS)
            HKFingerprint["initDataRaw"] = web_app_query
            login_data = self.http.post(
                url="/auth/auth-by-telegram-webapp",
                payload=json.dumps(HKFingerprint),
                headers={"authorization": ""},
                auth_header=False,
            )

            if (
                login_data is None
                or "authUserId" not in login_data
                or "authToken" not in login_data
            ):
                self.log.error("🔑 <red>Failed to login to HamsterKombat bot!</red>")
                return None

            self.log.info(
                f"✅ <g>Successfully logged in to HamsterKombat bot, UserID: </g><c>{login_data['authUserId']}</c>"
            )

            return login_data
        except Exception as e:
            self.log.error(f"🔑 <red>Failed to login to HamredKombat bot: {e}</red>")
            return None

    def get_account_info(self):
        self.log.info(f"🗒️ <y>Getting account info ...</y>")
        response = self.http.post(
            url="auth/account-info",
        )

        if response is None or "accountInfo" not in response:
            self.log.error("🔴 <red>Failed to get account info!</red>")
            return None

        date = response["accountInfo"]["at"].split("T")[0].replace("-", "/")
        self.log.info(
            f"🗒️ <g>Account ID: <c>{response['accountInfo']['id']}</c>, Join Date: <c>{date}</c></g>"
        )
        return response
