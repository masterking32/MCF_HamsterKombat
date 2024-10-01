# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import datetime
import json
import random
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
        basic = self.basic.get_upgrades_for_buy()
        if basic is None or "upgradesForBuy" not in basic:
            return

        cards = self.get_available_cards(basic["upgradesForBuy"])
        if not cards or len(cards) == 0:
            self.log.info(f"💸 <y>No upgrades available ...</y>")
            return

        self.filter_by_balance(cards, balance)
        if not cards or len(cards) == 0:
            self.log.info(f"💴 <y>No upgrades available ...</y>")
            return

        self.filter_by_coefficient(cards)
        if not cards or len(cards) == 0:
            self.log.info(f"💴 <y>No upgrades available ...</y>")
            return
        
        self.sort_cards(cards)
        
        cards_price = sum(card['price'] for card in cards)
        cards_profit = sum(card['profitPerHourDelta'] for card in cards)

        self.log.info(
            f"💸 <g>Available cards: <c>{len(cards)}</c> "
            f"with total price <c>{cards_price:.2f}💎</c> "
            f"and profit <c>+{cards_profit:.2f}💎</c></g>"
        )

        buy_errors = 0
        for best_card in cards:
            time.sleep(5)
            buy_card = self.buy_card(best_card)
            if not buy_card:
                if buy_errors >= 3:
                    self.log.error(
                        f"❌ <red>Buying cards has been interrupted due to errors ({buy_errors}).</red>"
                    )
                    break
                continue
            spent_amount = spent_amount + best_card["price"]
            profit_per_hour = profit_per_hour + best_card["profitPerHourDelta"]
            time.sleep(5)

        if spent_amount == 0 and profit_per_hour == 0:
            self.log.info(f"💴 <y>No upgrades available ...</y>")
        else:
            self.log.info(
                f"💸 <g>Upgrade completed, spent amount: <c>{spent_amount:.2f}💎</c>, "
                f"profit per hour: <c>{profit_per_hour:.2f}💎</c></g>"
            )

    def filter_by_balance(self, cards, balance):
        potential_price = 0
        potential_profit = 0
        for i in reversed(range(len(cards))):
            upgrade_cost = cards[i]["price"]
            upgrade_profit = cards[i]["profitPerHourDelta"]
            if potential_price + upgrade_cost <= balance:
                potential_price += upgrade_cost
                potential_profit += upgrade_profit
            else:
                del cards[i]

    def filter_by_coefficient(self, cards):
        coefficient_limit = getConfig("upgrade_coefficient", 200)
        expensive_cards = []

        for i in reversed(range(len(cards))):
            card_coefficient = self.get_card_coefficient(cards[i])
            if card_coefficient > coefficient_limit:
                expensive_cards.append(cards[i])
                del cards[i]

        if expensive_cards:
            expensive_card_names = ", ".join(
                [f"<c>{card['name']}</c>" for card in expensive_cards]
            )
            self.log.info(
                f"🪙 <y>Cards {expensive_card_names} exceed the upgrade coefficient ({coefficient_limit}).</y>"
            )
            self.log.info(
                f"🪙 <y>You can adjust the coefficient in module settings.</y>"
            )

    def buy_card(self, card):
        if card is None or "id" not in card:
            self.log.error("❌ <red>Card not found!</red>")
            return False

        cardId = card["id"]
        cardName = card["name"]
        cardPrice = card["price"]
        cardLevel = card["level"]

        self.log.info(
            f"💳 <g>Start upgrading card <c>{cardName}</c> to level <c>{cardLevel}</c> for <c>{cardPrice:.2f}💎</c></g>"
        )
        response = self.http.post(
            url="interlude/buy-upgrade",
            payload=json.dumps(
                {
                    "upgradeId": cardId,
                    "timestamp": int(datetime.datetime.now().timestamp() * 1000)
                    - random.randint(100, 1000),
                }
            ),
        )

        if response is None or "interludeUser" not in response:
            self.log.error("❌ <red>Failed to buy card!</red>")
            return False

        self.log.info(
            f"💰 <g>Card <c>{card['name']}</c> was upgraded to level <c>{card['level']}</c> for <c>{card['price']:.2f}💎</c></g>"
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

            if card.get("maxLevel") is not None:
                if card.get("level", 0) >= card.get("maxLevel"):
                    continue

            new_cards.append(card)

        return new_cards

    def sort_cards(self, cards):
        return cards.sort(key=lambda x: x["price"] / x["profitPerHourDelta"])

    def get_card_coefficient(self, card):
        if card["price"] == 0 or card["profitPerHourDelta"] == 0:
            return 0
        return card["price"] / card["profitPerHourDelta"]
