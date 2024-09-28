# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import json
import random
from .Basic import Basic
from .PromoGames import PromoGames


class Playground:
    def __init__(self, log, HttpRequest):
        self.log = log
        self.http = HttpRequest
        self.basic = Basic(log, HttpRequest)

    def claim_random(self):
        self.log.info(f"🔄 <y>Claiming random Playground...</y>")

        promos = self.basic.get_promos()
        if promos is None:
            return

        promos = self.clean_promos(promos)
        if not promos:
            self.log.error("🔴 <red>No promos to claim!</red>")
            return

        random_promo = random.choice(promos)
        self.log.info(
            f"🔄 <y>Claiming Playground <g>{random_promo['title']['en']}</g>...</y>"
        )
        self.claim_promo(random_promo)

    def claim_promo(self, promo):
        self.log.info(f"🔄 <y>Claiming Playground <g>{promo['title']['en']}</g>...</y>")
        promo_key = self.generate_promo_key(promo["promoId"])
        if promo_key is None:
            return

        # send request to claim promo

        self.log.info(f"🔄 <g>Claimed Playground <y>{promo['title']['en']}</y>!</g>")

    def generate_promo_key(self, promo_id):
        #  response = self.http.post(
        #     url="https://testing.com",
        #     headers={
        #         "promoId": promo["promoId"],
        #         "promoKey": promo_key,
        #         "user-agent": "",
        #         "Origin": "",
        #         "Referer": "",
        #     },
        #     send_option_request=False,
        #     auth_header=False,
        # )
        return True

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
