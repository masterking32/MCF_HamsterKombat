# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot
import json
import requests


class HttpRequest:
    def __init__(self, log, proxy=None, user_agent=None):
        self.log = log
        self.proxy = proxy
        self.user_agent = user_agent
        self.game_url = "https://api.hamsterkombatgame.io"
        self.configVersion = None
        self.authToken = None

    def get(
        self,
        url,
        headers=None,
        sendOptions=True,
        Allowed_Response_Code=200,
        Allowed_Option_Response_Code=204,
        with_Auth=True,
    ):
        try:
            default_headers = self._get_default_headers()

            if headers is None:
                headers = {}

            if with_Auth and self.authToken:
                headers["authorization"] = f"Bearer {self.authToken}"

            if headers:
                for key, value in headers.items():
                    default_headers[key] = value

            if sendOptions:
                self.options(url, "GET", headers, Allowed_Option_Response_Code)

            response = requests.get(
                self._fix_url(url),
                headers=default_headers,
                proxies=self._get_proxy(),
            )

            if response.status_code != Allowed_Response_Code:
                self.log.error(
                    f"🔴 <red> GET Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                )
                return None

            if "config-version" in response.headers:
                self.configVersion = response.headers["config-version"]

            return response.json()
        except Exception as e:
            self.log.error(f"🔴 <red> GET Request Error: <y>{url}</y> {e}</red>")
            return None

    def post(
        self,
        url,
        payload=None,
        headers=None,
        sendOptions=True,
        Allowed_Response_Code=200,
        Allowed_Option_Response_Code=204,
        with_Auth=True,
    ):
        try:
            default_headers = self._get_default_headers()

            if headers is None:
                headers = {}

            if with_Auth and self.authToken is not None:
                headers["authorization"] = f"Bearer {self.authToken}"

            if headers:
                for key, value in headers.items():
                    default_headers[key] = value

            if sendOptions:
                self.options(url, "POST", headers, Allowed_Option_Response_Code)
            response = None
            if payload:
                response = requests.post(
                    self._fix_url(url),
                    headers=default_headers,
                    data=payload,
                    proxies=self._get_proxy(),
                )
            else:
                response = requests.post(
                    self._fix_url(url),
                    headers=default_headers,
                    proxies=self._get_proxy(),
                )

            if response.status_code != Allowed_Response_Code:
                self.log.error(
                    f"🔴 <red> POST Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                )
                return None

            if "config-version" in response.headers:
                self.configVersion = response.headers["config-version"]

            return response.json()
        except Exception as e:
            self.log.error(f"🔴 <red> POST Request Error: <y>{url}</y> {e}</red>")
            return None

    def options(self, url, method, headers=None, Allowed_Response_Code=204):
        try:
            default_headers = self._get_get_option_headers(headers, method)
            response = requests.options(
                self._fix_url(url),
                headers=default_headers,
                proxies=self._get_proxy(),
            )

            if response.status_code != Allowed_Response_Code:
                self.log.error(
                    f"🔴 <red> OPTIONS Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                )
                return None

            return True
        except Exception as e:
            self.log.error(f"🔴 <red> OPTIONS Request Error: <y>{url}</y> {e}</red>")
            return None

    def _get_proxy(self):
        if self.proxy:
            return {"http": self.proxy, "https": self.proxy}

        return None

    def _fix_url(self, url):
        if url.startswith("http"):
            return url
        elif url.startswith("/"):
            return f"{self.game_url}{url}"

        return f"{self.game_url}/{url}"

    def _get_default_headers(self):
        headers = {
            "accept": "application/json",
            "Origin": "https://hamsterkombatgame.io",
            "Referer": "https://hamsterkombatgame.io/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": self.user_agent,
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "Content-Type": "application/json",
        }

        if "android" in self.user_agent.lower():
            headers["Sec-CH-UA-Platform"] = '"Android"'
            headers["Sec-CH-UA-Mobile"] = "?1"
            headers["Sec-CH-UA"] = (
                '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"'
            )
            headers["X-Requested-With"] = "org.telegram.messenger"

        return headers

    def _get_get_option_headers(self, headers=None, method="GET"):
        default_headers = {
            "Accept": "*/*",
            "Origin": "https://hamsterkombatgame.io",
            "Referer": "https://hamsterkombatgame.io/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": self.user_agent,
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "access-control-request-method": method,
            "access-control-request-headers": "content-type",
        }

        if not headers:
            return default_headers

        if "authorization" in headers:
            default_headers["access-control-request-headers"] = (
                default_headers["access-control-request-headers"] + ",authorization"
            )

        return default_headers
