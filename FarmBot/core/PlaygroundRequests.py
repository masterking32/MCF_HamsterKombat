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
from utilities.PromoGames import PromoGames


class PlaygroundRequests:
    def __init__(self, log, HttpRequest, bot_globals):
        self.log = log
        self.http = HttpRequest
        self.basic = Basic(log, HttpRequest)
        self.bot_globals = bot_globals

    def claim_random(self):
        try:
            promos = self.basic.get_promos()
            if promos is None:
                return

            promos = self.clean_promos(promos)
            if not promos or len(promos) == 0:
                self.log.info("🟢 <y>No promos to claim!</y>")
                return

            promoCodeResponse = self.bot_globals["Playground"].get_not_used_request(
                self.http.proxy
            )

            if promoCodeResponse is not None:
                promoCode = promoCodeResponse["promoCode"]
                promoId = promoCodeResponse["promoId"]

                for promo in promos:
                    if promo["promoId"] == promoId:
                        self.bot_globals["Playground"].mark_request_as_used(
                            promoId, promoCode
                        )

                        self.log.info(
                            f"🔑 <y>Claiming Playground with promo code <g>{promoCode}</g>...</y>"
                        )

                        self.apply_promo(promoCode)

                        self.log.info(
                            f"✅ <g>Claimed Playground with promo code <y>{promoCode}</y>!</g>"
                        )
                        promos = self.basic.get_promos()
                        if promos is None:
                            return

                        promos = self.clean_promos(promos)
                        if not promos or len(promos) == 0:
                            self.log.info("🟢 <y>No promos to claim!</y>")
                            return

            promo = random.choice(promos)
            self.add_to_queue(promo)
        except Exception as e:
            self.log.error(f"🔴 <red>Error claiming random Playground: {e}</red>")

    def clean_promos(self, promos):
        states = promos["states"]
        promos = promos["promos"]
        final_promos = []
        for promo in promos:
            promo_name = promo["title"]["en"]
            if promo["promoId"] in [  # Exculude promos
                "b2436c89-e0aa-4aed-8046-9b0515e1c46b",  # Zoopolis
            ]:
                continue
            if promo["promoId"] not in PromoGames:
                self.log.info(
                    f"🟡 <y>Unsupported promo <g>{promo_name}</g> game...</y>"
                )
                continue

            receiveKeysToday = 0
            for state in states:
                if state["promoId"] == promo["promoId"] and "receiveKeysToday" in state:
                    receiveKeysToday = state["receiveKeysToday"]
                    break

            if int(receiveKeysToday) >= int(promo["rewardsPerDay"]):
                self.log.info(f"✅ <g>Max keys reached for <c>{promo_name}</c>...</g>")
                continue

            final_promos.append(promo)

        return final_promos

    def add_to_queue(self, promo):
        try:
            if self.bot_globals["Playground"].add_request(
                promo["promoId"], self.http.proxy, self.http.user_agent
            ):
                return True

            return False
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
