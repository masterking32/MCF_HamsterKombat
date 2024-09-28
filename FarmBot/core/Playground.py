# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import json
import random
import time
import uuid
from .Basic import Basic
from .PromoGames import PromoGames


class Playground:
    def __init__(self, log, HttpRequest):
        self.log = log
        self.http = HttpRequest
        self.basic = Basic(log, HttpRequest)

    def claim_random(self):
        self.log.info(f"🕹️ <y>Claiming random Playground...</y>")

        promos = self.basic.get_promos()
        if promos is None:
            return

        promos = self.clean_promos(promos)
        if not promos:
            self.log.error("🔴 <red>No promos to claim!</red>")
            return

        random_promo = random.choice(promos)
        self.log.info(
            f"🎮 <y>Claiming Playground <g>{random_promo['title']['en']}</g>...</y>"
        )

        self.claim_promo(random_promo)

    def clean_promos(self, promos):
        promos = promos["promos"]
        final_promos = []
        for promo in promos:
            promo_name = promo["title"]["en"]
            if promo["promoId"] not in PromoGames:
                self.log.info(f"🟡 <y>Unsupporting promo <g>{promo_name}</g>...</y>")
                continue

            # if promo finished log it and not add it to final_promos

            final_promos.append(promo)

        return final_promos

    def claim_promo(self, promo):
        self.log.info(f"🔄 <y>Claiming Playground <g>{promo['title']['en']}</g>...</y>")
        promo_key = self.generate_promo_key(promo["promoId"])
        if promo_key is None:
            return

        self.apply_promo(promo_key)
        self.log.info(f"✅ <g>Claimed Playground <y>{promo['title']['en']}</y>!</g>")

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
            return

        self.log.info(f"✅ <g>Applied promo code <y>{promoCode}</y>!</g>")

    def generate_promo_key(self, promo_id):
        try:
            promo_game = PromoGames[promo_id]
            promo_name = promo_game["name"]
            clientToken = self._promo_login(promo_id)

            if clientToken is None:
                return None

            promo_code = self._promo_create_code(promo_id, clientToken)
            if promo_code is None:
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
            promo_code = self._promo_create_code(promo_id, clientToken)
            if promo_code is None:
                return None

            self.log.info(
                f"🔑 <g>Generated promo key for <y>{promo_name}</y>: <c>{promo_code}</c></g>"
            )
            return promo_code
        except Exception as e:
            self.log.error(f"🔴 <red>Error generating promo key: {e}</red>")
            return None

    def _promo_register_event(self, promo_id, clientToken):
        promo_game = PromoGames[promo_id]
        promo_name = promo_game["name"]
        promo_id = promo_game["promoId"]
        self.log.info(f"🔄 <y>Registering event for <g>{promo_name}</g>...</y>")

        headers = self._get_promo_headers(promo_id)
        headers["authorization"] = f"Bearer {clientToken}"
        response = self.http.post(
            url="https://api.gamepromo.io/promo/register-event",
            payload=json.dumps(self._get_register_event_payload(promo_id)),
            headers=headers,
            auth_header=False,
        )

        if response is None or "hasCode" not in response:
            return False

        return response["hasCode"]

    def _promo_create_code(self, promo_id, clientToken):
        promo_game = PromoGames[promo_id]
        promo_name = promo_game["name"]
        promo_id = promo_game["promoId"]
        self.log.info(f"⚙️ <y>Creating code for <g>{promo_name}</g>...</y>")

        headers = self._get_promo_headers(promo_id)
        headers["authorization"] = f"Bearer {clientToken}"
        response = self.http.post(
            url="https://api.gamepromo.io/promo/create-code",
            payload=json.dumps({"promoId": promo_id}),
            headers=headers,
            auth_header=False,
        )

        if response is None or "promoCode" not in response:
            self.log.error(
                f"🔴 <red>Failed to create code for <y>{promo_name}</y>!</red>"
            )
            return None

        return response["promoCode"]

    def _promo_login(self, promo_id):
        promo_game = PromoGames[promo_id]
        promo_name = promo_game["name"]
        promo_id = promo_game["promoId"]
        self.log.info(f"🔐 <y>Logging in to <g>{promo_name}</g>...</y>")

        response = self.http.post(
            url="https://api.gamepromo.io/promo/login-client",
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

        if type == "7digits":
            return str(random.randint(1000000, 1999999))

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

        return payload

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

        return payload

    def _get_promo_headers(self, promo_id):
        promo_game = PromoGames[promo_id]
        headers = {
            "accept": "*/*",
            "authorization": "Bearer",
            "Content-Type": "application/json",
            "Host": "api.gamepromo.io",
            "Origin": None,
            "Referer": None,
            "Sec-Fetch-Dest": None,
            "Sec-Fetch-Mode": None,
            "Sec-Fetch-Site": None,
            "pragma": None,
            "cache-control": None,
        }

        if "userAgent" in promo_game:
            headers["user-agent"] = promo_game["userAgent"]

        if "x-unity-version" in promo_game:
            headers["x-unity-version"] = promo_game["x-unity-version"]

        return headers
