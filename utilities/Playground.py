# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import json
import random
import threading
import time
import uuid
import string
from .PromoGames import PromoGames
import requests


class Playground:
    def __init__(self, log):
        self.log = log
        self.requests = []

    def start(self):
        self.log.info("<m>[Playground]</m> 🤖 <g>Starting Playground thread...</g>")
        while True:
            time.sleep(5)
            try:
                if len(self.requests) == 0:
                    continue
                for request in self.requests:
                    try:
                        if request.get("status", "finished") != "active":
                            continue

                        threading.Thread(
                            target=self.handle_request, args=(request,)
                        ).start()
                    except Exception as e:
                        self.log.error(
                            f"<m>[Playground]</m> 🔴 <red>Error generating promo key: {e}</red>"
                        )
                        continue

            except Exception as e:
                self.log.error(
                    f"<m>[Playground]</m> 🔴 <red>Error generating promo key: {e}</red>"
                )
                continue

    def get_request_index_by_proxy(self, proxy=None):
        for request in self.requests:
            if request.get("proxy") == proxy:
                return self.requests.index(request)
        return None

    def get_not_used_request(self, proxy=None):
        for request in self.requests:
            if request.get("proxy") == proxy and request.get("status") == "finished":
                return request

        return None

    def mark_request_as_used(self, promo_id, promo_code):
        for request in self.requests:
            if (
                request.get("promoId") == promo_id
                and request.get("promoCode") == promo_code
            ):
                self.requests[self.requests.index(request)]["promoCode"] = None
                self.requests[self.requests.index(request)]["status"] = "used"
                return True
        return False

    def add_request(self, promo_id, proxy=None, user_agent=None):
        if promo_id is None:
            return False

        if promo_id not in PromoGames:
            self.log.error(
                f"<m>[Playground]</m> 🟡 <y>Promo ID <y>{promo_id}</y> is not supported!</y>"
            )
            return False

        p_game = PromoGames[promo_id]
        promo_name = p_game["name"]
        request_index = self.get_request_index_by_proxy(proxy)
        new_request = {
            "promoId": promo_id,
            "proxy": proxy,
            "userAgent": user_agent,
            "status": "active",
            "promoCode": None,
        }

        if request_index is None:
            self.log.info(
                f"<m>[Playground]</m> 🟢 <g>Adding a new request for <y>{promo_name}</y> to the playground queue.</g>"
            )
            self.requests.append(new_request)
            return True

        request = self.requests[request_index]
        if request.get("status") != "used":
            return False

        self.requests[request_index] = new_request
        self.log.info(
            f"<m>[Playground]</m> 🟢 <g>Adding a new request for <y>{promo_name}</y> to the playground queue.</g>"
        )
        return True

    def handle_request(self, request):
        request_index = self.requests.index(request)
        request_status = request.get("status", "finished")
        if request_status != "active":
            return False

        promo_id = request.get("promoId", None)
        promo_proxy = request.get("proxy", None)
        promo_user_agent = request.get("userAgent", None)

        request_status = "working"
        request["promoCode"] = None
        request["status"] = request_status
        self.requests[request_index] = request

        if promo_id is None:
            return False

        if promo_id not in PromoGames:
            self.log.error(
                f"<m>[Playground]</m> 🟡 <y>Promo ID <y>{promo_id}</y> is not supported!</y>"
            )
            self.requests[request_index] = request
            return False

        promo_response = self.generate_promo_key(
            promo_id, promo_proxy, promo_user_agent
        )

        if promo_response is None or not promo_response.get("promoCode"):
            request_status = "used"
            request["status"] = request_status
            request["promoCode"] = None
            self.requests[request_index] = request
            return False

        request["status"] = "finished"
        request["promoCode"] = promo_response["promoCode"]

        self.requests[request_index] = request
        return True

    def generate_promo_key(self, promo_id, proxy=None, user_agent=None):
        try:
            promo_game = PromoGames[promo_id]
            promo_name = promo_game["name"]
            clientToken = self._promo_login(promo_id, proxy, user_agent)

            if clientToken is None:
                return None

            time.sleep(2)

            promo_response = self._promo_create_code(
                promo_id, clientToken, proxy, user_agent
            )
            if promo_response is None:
                return None

            self.log.info(
                f"<m>[Playground]</m> 💤 <y>Sleeping for {promo_game['delay']} secs ...</y>"
            )
            time.sleep(promo_game["delay"])

            self.log.info(
                f"<m>[Playground]</m> ⚒️ <g>Starting to generate promo key for <y>{promo_name}</y>...</g>"
            )
            self.log.info(
                f"<m>[Playground]</m> 💻 <y>This process may take a while (up to 20 minutes)...</y>"
            )
            self.log.info(
                f"<m>[Playground]</m> ✅ <y> Once the key is generated, it will be used in the next account check.</y>"
            )
            tries = 0
            while tries < 20:
                response = self._promo_register_event(
                    promo_id, clientToken, proxy, user_agent
                )
                if response:
                    # self.log.info(
                    #     f"<m>[Playground]</m> 🎯 <y>Event registered for <g>{promo_name}</g>...</y>"
                    # )
                    break

                # self.log.info(
                #     f"<m>[Playground]</m> 🔁 <y>Retrying to register event after {promo_game['retry_delay']} seconds.</y>"
                # )
                time.sleep(promo_game["retry_delay"])
                tries += 1

            if tries >= 20:
                # self.log.error(
                #     f"<m>[Playground]</m> 🔴 <red>Failed to generate promo key for <y>{promo_name}</y>!</red>"
                # )
                return None

            # self.log.info(
            #     f"<m>[Playground]</m> 🏓 <g>Proceeding to the final step of key generation...</g>"
            # )
            promo_response = self._promo_create_code(
                promo_id, clientToken, proxy, user_agent
            )
            if promo_response is None:
                return None

            self.log.info(
                f"<m>[Playground]</m> 🔑 <g>Generated promo key for <y>{promo_name}</y>: <c>{promo_response['promoCode']}</c></g>"
            )

            self.log.info(
                f"<m>[Playground]</m> <g>This key will be used in the next account check.</g>"
            )
            return promo_response
        except Exception as e:
            self.log.error(
                f"<m>[Playground]</m> 🔴 <red>Error generating promo key: {e}</red>"
            )

            return None

    def _promo_register_event(self, promo_id, clientToken, proxy=None, user_agent=None):
        promo_game = PromoGames[promo_id]
        promo_name = promo_game["name"]
        promo_id = promo_game["promoId"]
        response = None
        self.log.info(
            f"<m>[Playground]</m> 🔄 <y>Registering event for <g>{promo_name}</g>...</y>"
        )

        url = "https://api.gamepromo.io/promo/register-event"

        if promo_game.get("newApi"):
            url = "https://api.gamepromo.io/promo/1/register-event"

        if "optionsHeaders" in promo_game:
            headers = self._get_promo_headers(promo_id, "OPTIONS", user_agent)
            headers["access-control-request-headers"] = "authorization,content-type"
            response = self.http_request(
                url=url,
                method="OPTIONS",
                headers=headers,
                valid_response_code=204,
                proxy=proxy,
                display_error=False,
            )

        headers = self._get_promo_headers(promo_id, user_agent=user_agent)
        headers["authorization"] = f"Bearer {clientToken}"
        response = self.http_request(
            url=url,
            method="POST",
            headers=headers,
            payload=json.dumps(self._get_register_event_payload(promo_id)),
            valid_response_code=200,
            proxy=proxy,
            display_error=False,
        )

        if response is None or "hasCode" not in response:
            return False

        return response["hasCode"]

    def _promo_create_code(self, promo_id, clientToken, proxy=None, user_agent=None):
        promo_game = PromoGames[promo_id]
        promo_name = promo_game["name"]
        promo_id = promo_game["promoId"]
        response = None
        self.log.info(
            f"<m>[Playground]</m> ⚙️ <y>Creating code for <g>{promo_name}</g>...</y>"
        )

        url = "https://api.gamepromo.io/promo/create-code"

        if promo_game.get("newApi"):
            url = "https://api.gamepromo.io/promo/1/create-code"

        if "optionsHeaders" in promo_game:
            headers = self._get_promo_headers(promo_id, "OPTIONS", user_agent)
            headers["access-control-request-headers"] = "authorization,content-type"
            response = self.http_request(
                url=url,
                method="OPTIONS",
                headers=headers,
                valid_response_code=204,
                proxy=proxy,
            )

        headers = self._get_promo_headers(promo_id, user_agent=user_agent)
        headers["authorization"] = f"Bearer {clientToken}"
        response = self.http_request(
            url=url,
            method="POST",
            headers=headers,
            payload=json.dumps({"promoId": promo_id}),
            valid_response_code=200,
            proxy=proxy,
        )

        if response is None or "promoCode" not in response:
            self.log.error(
                f"<m>[Playground]</m> 🔴 <red>Failed to create code for <y>{promo_name}</y>!</red>"
            )
            return None

        return response

    def http_request(
        self,
        url,
        proxy=None,
        method="POST",
        headers=None,
        payload=None,
        valid_response_code=200,
        display_error=True,
        retries=2,
    ):
        if retries < 0:
            return None

        try:
            if proxy is not None:
                proxy = {"http": proxy, "https": proxy}

            response = None
            if method == "GET":
                response = requests.get(url, headers=headers, proxies=proxy)
            elif method == "POST":
                response = requests.post(
                    url, headers=headers, data=payload, proxies=proxy
                )
            elif method == "OPTIONS":
                response = requests.options(url, headers=headers, proxies=proxy)

            if response.status_code != valid_response_code:
                if display_error:
                    self.log.error(
                        f"<m>[Playground]</m> 🔴 <red> {method} Request Error: {url} Response code: {response.status_code}</red>"
                    )
                return None
            if method == "OPTIONS":
                return True

            return response.json()
        except Exception as e:
            if retries > 0:
                self.log.info(
                    f"<m>[Playground]</m> 🟡 <y> Unable to send request, retrying in 10 seconds...</y>"
                )
                time.sleep(10)
                return self.http_request(
                    url,
                    proxy,
                    method,
                    headers,
                    payload,
                    valid_response_code,
                    retries=retries - 1,
                )
            return None

    def _promo_login(self, promo_id, proxy=None, user_agent=None):
        promo_game = PromoGames[promo_id]
        promo_name = promo_game["name"]
        promo_id = promo_game["promoId"]
        self.log.info(
            f"<m>[Playground]</m> 🔐 <y>Logging in to <g>{promo_name}</g>...</y>"
        )

        url = "https://api.gamepromo.io/promo/login-client"

        if promo_game.get("newApi"):
            url = "https://api.gamepromo.io/promo/1/login-client"

        if "optionsHeaders" in promo_game:
            headers = self._get_promo_headers(promo_id, "OPTIONS", user_agent)
            headers["access-control-request-headers"] = "content-type"
            response = self.http_request(
                url=url,
                proxy=proxy,
                method="OPTIONS",
                headers=headers,
                valid_response_code=204,
            )

        response = self.http_request(
            url=url,
            proxy=proxy,
            method="POST",
            headers=self._get_promo_headers(promo_id, user_agent=user_agent),
            payload=json.dumps(self._get_login_payload(promo_id)),
            valid_response_code=200,
        )

        if response is None or "clientToken" not in response:
            self.log.error(
                f"<m>[Playground]</m> 🔴 <red>Failed to login to <y>{promo_name}</y>!</red>"
            )
            return None

        return response["clientToken"]

    def _generate_id(self, type=None):
        if type is None or type == "uuid":
            return str(uuid.uuid4())
        elif type == "7digits":
            # return str(random.randint(1000000, 1999999))
            return "".join(random.choices(string.digits, k=7))
        elif type == "32strLower":
            return "".join(
                random.choices(string.ascii_letters + string.digits, k=32)
            ).lower()
        elif type == "16strUpper":
            return "".join(
                random.choices(string.ascii_letters + string.digits, k=16)
            ).upper()
        elif type == "ts-19digits":
            return f"{int(time.time() * 1000)}-" + "".join(
                random.choices(string.digits, k=19)
            )
        elif type == "28str":
            return "".join(random.choices(string.ascii_letters + string.digits, k=28))
        else:
            return type

    def _get_register_event_payload(self, promo_id):
        promo_game = PromoGames[promo_id]
        payload = {
            "promoId": promo_id,
            "eventId": self._generate_id(promo_game["eventIdType"]),
        }

        if "eventOrigin" in promo_game:
            payload["eventOrigin"] = promo_game["eventOrigin"]

        if "eventType" in promo_game:
            payload["eventType"] = promo_game["eventType"]

        cleaned_payload = {
            key: value
            for key, value in payload.items()
            if value is not None and value != ""
        }

        return cleaned_payload

    def _get_login_payload(self, promo_id):
        promo_game = PromoGames[promo_id]

        payload = {
            "appToken": promo_game["appToken"],
            "clientId": self._generate_id(promo_game["clientIdType"]),
        }

        if "clientOrigin" in promo_game:
            payload["clientOrigin"] = promo_game["clientOrigin"]

        if "clientVersion" in promo_game:
            payload["clientVersion"] = promo_game["clientVersion"]

        cleaned_payload = {
            key: value
            for key, value in payload.items()
            if value is not None and value != ""
        }

        return cleaned_payload

    def _get_promo_headers(self, promo_id, method="POST", user_agent=None):
        promo_game = PromoGames[promo_id]
        headers = {
            "accept": "*/*",
            "content-type": "application/json; charset=utf-8",
            "host": "api.gamepromo.io",
            "origin": None,
            "referer": None,
            "sec-fetch-dest": None,
            "sec-fetch-mode": None,
            "sec-fetch-site": None,
            "pragma": None,
            "cache-control": None,
            "user-agent": user_agent,
        }

        method_headers = {}

        if promo_game.get("headers"):
            method_headers = promo_game["headers"]

        for key, value in method_headers.items():
            headers[key] = value

        if method.upper() == "OPTIONS" and "optionsHeaders" in promo_game:
            method_headers = promo_game["optionsHeaders"]
        elif method.upper() == "POST" and "postHeaders" in promo_game:
            method_headers = promo_game["postHeaders"]

        for key, value in method_headers.items():
            headers[key] = value

        # In PromoGames, if user-agent is "", This means that the user-agent should be removed
        # If user-agent is None, it will be set to the default user-agent
        # If user-agent is set to a value, it will be used as the user-agent
        if "user-agent" in method_headers and method_headers["user-agent"] == "":
            headers["user-agent"] = None

        return headers
