# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import time
import requests


class HttpRequest:
    def __init__(
        self,
        log,
        proxy=None,
        user_agent=None,
    ):
        self.log = log
        self.proxy = proxy
        self.user_agent = user_agent
        self.game_url = "https://api.hamsterkombatgame.io"
        self.authToken = None

        if not self.user_agent or self.user_agent == "":
            self.user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.3"

        if "windows" in self.user_agent.lower():
            self.log.warning(
                "🟡 <y>Windows User Agent detected, For safety please use mobile user-agent</y>"
            )

    def get(
        self,
        url,
        headers=None,
        send_option_request=True,
        valid_response_code=200,
        valid_option_response_code=204,
        auth_header=True,
        return_headers=False,
        retries=3,
    ):
        try:
            url = self._fix_url(url)
            default_headers = (
                self._get_default_headers() if "hamsterkombatgame.io" in url else {}
            )

            if headers is None:
                headers = {}

            if auth_header and self.authToken:
                headers["authorization"] = f"Bearer {self.authToken}"

            if headers:
                for key, value in headers.items():
                    default_headers[key] = value

            if send_option_request:
                self.options(url, "GET", headers, valid_option_response_code)

            response = requests.get(
                self._fix_url(url),
                headers=default_headers,
                proxies=self._get_proxy(),
            )

            if response.status_code != valid_response_code:
                self.log.error(
                    f"🔴 <red> GET Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                )
                return (None, None) if return_headers else None

            return (
                (response.json(), response.headers)
                if return_headers
                else response.json()
            )
        except Exception as e:
            if retries > 0:
                self.log.info(f"🟡 <y> Unable to send request, retrying...</y>")
                time.sleep(0.5)
                return self.get(
                    url,
                    headers,
                    send_option_request,
                    valid_response_code,
                    valid_option_response_code,
                    auth_header,
                    return_headers,
                    retries - 1,
                )

            self.log.error(f"🔴 <red> GET Request Error: <y>{url}</y> {e}</red>")
            return (None, None) if return_headers else None

    def post(
        self,
        url,
        payload=None,
        headers=None,
        send_option_request=True,
        valid_response_code=200,
        valid_option_response_code=204,
        auth_header=True,
        return_headers=False,
        retries=3,
    ):
        try:
            url = self._fix_url(url)
            default_headers = (
                self._get_default_headers() if "hamsterkombatgame.io" in url else {}
            )

            if headers is None:
                headers = {}

            if auth_header and self.authToken is not None:
                headers["authorization"] = f"Bearer {self.authToken}"

            if headers:
                for key, value in headers.items():
                    default_headers[key] = value

            if send_option_request:
                self.options(url, "POST", headers, valid_option_response_code)
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

            if response.status_code != valid_response_code:
                self.log.error(
                    f"🔴 <red> POST Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                )
                return (None, None) if return_headers else None

            return (
                (response.json(), response.headers)
                if return_headers
                else response.json()
            )
        except Exception as e:
            if retries > 0:
                self.log.info(f"🟡 <y> Unable to send request, retrying...</y>")
                time.sleep(0.5)
                return self.post(
                    url,
                    payload,
                    headers,
                    send_option_request,
                    valid_response_code,
                    valid_option_response_code,
                    auth_header,
                    return_headers,
                    retries - 1,
                )

            self.log.error(f"🔴 <red> POST Request Error: <y>{url}</y> {e}</red>")
            return (None, None) if return_headers else None

    def options(self, url, method, headers=None, valid_response_code=204, retries=3):
        try:
            url = self._fix_url(url)
            default_headers = (
                self._get_get_option_headers(headers, method)
                if "hamsterkombatgame.io" in url
                else {}
            )

            if headers is None:
                headers = {}

            if headers:
                for key, value in headers.items():
                    default_headers[key] = value

            response = requests.options(
                url=url,
                headers=default_headers,
                proxies=self._get_proxy(),
            )

            if response.status_code != valid_response_code:
                self.log.error(
                    f"🔴 <red> OPTIONS Request Error: <y>{url}</y> Response code: {response.status_code}</red>"
                )
                return None

            return True
        except Exception as e:
            if retries > 0:
                self.log.info(f"🟡 <y> Unable to send option request, retrying...</y>")
                time.sleep(0.5)
                return self.options(
                    url, method, headers, valid_response_code, retries - 1
                )
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
