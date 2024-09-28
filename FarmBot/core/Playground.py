# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import json
import random
import time
import uuid
import string
from .Basic import Basic
from .PromoGames import PromoGames


class Playground:
    def __init__(self, log, HttpRequest):
        self.log = log
        self.http = HttpRequest
        self.basic = Basic(log, HttpRequest)

    def claim_random(self):
        try:
            self.log.info(f"🕹️ <y>Claiming random Playground...</y>")

            promos = self.basic.get_promos()
            if promos is None:
                return

            promos = self.clean_promos(promos)
            if not promos or len(promos) == 0:
                self.log.error("🔴 <red>No promos to claim!</red>")
                return

            promo = random.choice(promos)
            self.claim_promo(promo)
        except Exception as e:
            self.log.error(f"🔴 <red>Error claiming random Playground: {e}</red>")

    def clean_promos(self, promos):
        states = promos["states"]
        promos = promos["promos"]
        final_promos = []
        for promo in promos:
            promo_name = promo["title"]["en"]
            if promo["promoId"] not in PromoGames:
                self.log.info(
                    f"🟡 <y>Unsupporting promo <g>{promo_name}</g> game...</y>"
                )
                continue

            receiveKeysToday = 0
            for state in states:
                if state["promoId"] == promo["promoId"] and "receiveKeysToday" in state:
                    receiveKeysToday = state["receiveKeysToday"]
                    break

            if int(receiveKeysToday) >= int(promo["keysPerDay"]):
                self.log.info(f"✅ <g>Max keys reached for <c>{promo_name}</c>...</g>")
                continue

            final_promos.append(promo)

        return final_promos

    def claim_promo(self, promo):
        try:
            self.log.info(
                f"🔄 <y>Claiming Playground <g>{promo['title']['en']}</g>...</y>"
            )
            promo_response = self.generate_promo_key(promo["promoId"])
            if promo_response is None:
                return False

            if not promo_response.get("promoCode"):
                return False

            resp = self.apply_promo(promo_response.get("promoCode"))
            if not resp:
                return False

            self.log.info(
                f"✅ <g>Claimed Playground <y>{promo['title']['en']}</y>!</g>"
            )

            return True
        except Exception as e:
            self.log.error(f"🔴 <red>Error claiming Playground: {e}</red>")
            return False

    def apply_promo(self, promoCode):
        self.log.info(f"🎲 <y>Applying promo code <g>{promoCode}</g>...</y>")

        response = self.http.post(
            url="interlude/apply-promo",
            payload=json.dumps({"promoCode": promoCode}),
        )

        if response is None or "reward" not in response:
            self.log.error(
                f"🔴 <red>Failed to apply promo code <y>{promoCode}</y>!</red>"
            )
            return False

        self.log.info(f"✅ <g>Applied promo code <y>{promoCode}</y>!</g>")
        return True

    def generate_promo_key(self, promo_id):
        try:
            promo_game = PromoGames[promo_id]
            promo_name = promo_game["name"]
            clientToken = self._promo_login(promo_id)

            if clientToken is None:
                return None

            time.sleep(2)

            promo_response = self._promo_create_code(promo_id, clientToken)
            if promo_response is None:
                return None

            self.log.info(f"💤 <y>Sleeping for {promo_game['delay']} secs ...</y>")
            time.sleep(promo_game["delay"])

            self.log.info(
                f"⚒️ <g>Starting to generate promo key for <y>{promo_name}</y>...</g>"
            )
            self.log.info(
                f"💻 <y>This process may take a while (up to 20 minutes)...</y>"
            )
            tries = 0
            while tries < 20:
                response = self._promo_register_event(promo_id, clientToken)
                if response:
                    self.log.info(
                        f"🎯 <y>Event registered for <g>{promo_name}</g>...</y>"
                    )
                    break

                self.log.info(
                    f"🔁 <y>Retrying to register event after {promo_game['retry_delay']} seconds.</y>"
                )
                time.sleep(promo_game["retry_delay"])
                tries += 1

            if tries >= 20:
                self.log.error(
                    f"🔴 <red>Failed to generate promo key for <y>{promo_name}</y>!</red>"
                )
                return None

            self.log.info(
                f"🏓 <g>Proceeding to the final step of key generation...</g>"
            )
            promo_response = self._promo_create_code(promo_id, clientToken)
            if promo_response is None:
                return None

            self.log.info(
                f"🔑 <g>Generated promo key for <y>{promo_name}</y>: <c>{promo_response['promoCode']}</c></g>"
            )
            return promo_response
        except Exception as e:
            self.log.error(f"🔴 <red>Error generating promo key: {e}</red>")
            return None

    def _promo_register_event(self, promo_id, clientToken):
        promo_game = PromoGames[promo_id]
        promo_name = promo_game["name"]
        promo_id = promo_game["promoId"]
        response = None
        self.log.info(f"🔄 <y>Registering event for <g>{promo_name}</g>...</y>")

        url = "https://api.gamepromo.io/promo/register-event"

        if promo_game.get("newApi"):
            url = "https://api.gamepromo.io/promo/1/register-event"

        if "optionsHeaders" in promo_game:
            headers = self._get_promo_headers(promo_id, "OPTIONS")
            headers["access-control-request-headers"] = "authorization,content-type"
            response = self.http.options(
                url=url,
                method="OPTIONS",
                headers=headers,
                valid_response_code=204,
            )

        headers = self._get_promo_headers(promo_id)
        headers["authorization"] = f"Bearer {clientToken}"
        response = self.http.post(
            url=url,
            payload=json.dumps(self._get_register_event_payload(promo_id)),
            headers=headers,
            auth_header=False,
            send_option_request=False,
        )

        if response is None or "hasCode" not in response:
            return False

        return response["hasCode"]

    def _promo_create_code(self, promo_id, clientToken):
        promo_game = PromoGames[promo_id]
        promo_name = promo_game["name"]
        promo_id = promo_game["promoId"]
        response = None
        self.log.info(f"⚙️ <y>Creating code for <g>{promo_name}</g>...</y>")

        url = "https://api.gamepromo.io/promo/create-code"

        if promo_game.get("newApi"):
            url = "https://api.gamepromo.io/promo/1/create-code"

        if "optionsHeaders" in promo_game:
            headers = self._get_promo_headers(promo_id, "OPTIONS")
            headers["access-control-request-headers"] = "authorization,content-type"
            response = self.http.options(
                url=url,
                method="OPTIONS",
                headers=headers,
                valid_response_code=204,
            )

        headers = self._get_promo_headers(promo_id)
        headers["authorization"] = f"Bearer {clientToken}"
        response = self.http.post(
            url=url,
            payload=json.dumps({"promoId": promo_id}),
            headers=headers,
            auth_header=False,
            send_option_request=False,
        )

        if response is None or "promoCode" not in response:
            self.log.error(
                f"🔴 <red>Failed to create code for <y>{promo_name}</y>!</red>"
            )
            return None

        return response

    def _promo_login(self, promo_id):
        promo_game = PromoGames[promo_id]
        promo_name = promo_game["name"]
        promo_id = promo_game["promoId"]
        self.log.info(f"🔐 <y>Logging in to <g>{promo_name}</g>...</y>")

        url = "https://api.gamepromo.io/promo/login-client"

        if promo_game.get("newApi"):
            url = "https://api.gamepromo.io/promo/1/login-client"

        if "optionsHeaders" in promo_game:
            headers = self._get_promo_headers(promo_id, "OPTIONS")
            headers["access-control-request-headers"] = "content-type"
            response = self.http.options(
                url=url,
                method="OPTIONS",
                headers=headers,
                valid_response_code=204,
            )

        response = self.http.post(
            url=url,
            payload=json.dumps(self._get_login_payload(promo_id)),
            headers=self._get_promo_headers(promo_id),
            auth_header=False,
            send_option_request=False,
        )

        if response is None or "clientToken" not in response:
            self.log.error(f"🔴 <red>Failed to login to <y>{promo_name}</y>!</red>")
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

    def _get_promo_headers(self, promo_id, method="POST"):
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
            "user-agent": self.http.user_agent,
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
