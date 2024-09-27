# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import datetime
import json
import time
from .Basic import Basic
from utilities.utilities import getConfig


class Cards:
    def __init__(self, log, HttpRequest):
        self.log = log
        self.http = HttpRequest
        self.basic = Basic(log, HttpRequest)

    def start_upgrades(self, balance):
        self.log.info("🔝 <y>Starting upgrade ...</y>")
        spent_amount = 0
        profit_per_hour = 0
        while True:
            basic = self.basic.get_upgrades_for_buy()
            if basic is None or "upgradesForBuy" not in basic:
                break

            cards = self.get_available_cards(basic["upgradesForBuy"])
            if not cards or len(cards) == 0:
                break

            self.sort_cards(cards)
            best_card = cards[0]
            if best_card["price"] > balance:
                self.log.info(
                    f"💴 <g>Card <c>{best_card['name']}</c> is too expensive</g>"
                )
                break

            card_coefficient = self.get_card_coefficient(best_card)
            if card_coefficient > getConfig("upgrade_coefficient", 200):
                self.log.info(
                    f"🪙 <g>Card <c>{best_card['name']}</c> exceeds the upgrade coefficient and is too expensive</g>"
                )
                break

            buy_card = self.buy_card(best_card)
            if not buy_card:
                self.log.error("❌ <red>Failed to buy card!</red>")
                break
            spent_amount = spent_amount + best_card["price"]
            profit_per_hour = profit_per_hour + best_card["profitPerHourDelta"]
            time.sleep(5)

        self.log.info(
            f"💸 <g>Upgrade completed, spent amount: <c>{spent_amount}💎</c>, profit per hour: <c>{profit_per_hour}💎</c></g>"
        )

    def buy_card(self, card):
        cardId = card["id"]
        cardName = card["name"]
        cardPrice = card["price"]
        cardLevel = card["level"]

        self.log.info(
            f"💳 <g>Start upgrading card <c>{cardName}</c> to level <c>{cardLevel}</c> for <c>{cardPrice}💎</c></g>"
        )

        response = self.http.post(
            url="interlude/buy-upgrade",
            payload=json.dumps(
                {
                    "upgradeId": cardId,
                    "timestamp": int(datetime.datetime.now().timestamp() * 1000),
                }
            ),
        )

        if response is None or "interludeUser" not in response:
            self.log.error("❌ <red>Failed to buy card!</red>")
            return False

        self.log.info(
            f"💰 <g>Card <c>{card['name']}</c> was upgraded to level <c>{card['level']}</c> for <c>{card['price']}💎</c></g>"
        )
        return True

    def get_available_cards(self, cards):
        new_cards = []
        for card in cards:
            if not card.get("isAvailable", True):
                continue

            if card.get("isExpired", False):
                continue

            if card.get("cooldownSeconds", 0) > 0:
                continue

            new_cards.append(card)

        return new_cards

    def sort_cards(self, cards):
        return cards.sort(key=lambda x: x["price"] / x["profitPerHourDelta"])

    def get_card_coefficient(self, card):
        if card["price"] == 0 or card["profitPerHourDelta"] == 0:
            return 0
        return card["price"] / card["profitPerHourDelta"]
