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

        self.sort_cards(cards)

        potential_upgrades = []
        potential_price = 0
        potential_profit = 0
        for upgrade in cards:
            upgrade_cost = upgrade["price"]
            upgrade_profit = upgrade["profitPerHourDelta"]
            if potential_price + upgrade_cost <= balance:
                potential_upgrades.append(upgrade)
                potential_price += upgrade_cost
                potential_profit += upgrade_profit
            else:
                break

        if not potential_upgrades or len(potential_upgrades) == 0:
            self.log.info(f"💴 <y>No upgrades available ...</y>")
            return

        self.log.info(
            f"💸 <g>Potential upgrades: <c>{len(potential_upgrades)}</c> "
            f"with total price <c>{'{:.2f}'.format(potential_price)}💎</c> "
            f"and profit <c>+{'{:.2f}'.format(potential_profit)}💎</c></g>"
        )

        buy_errors = 0
        for best_card in potential_upgrades:
            time.sleep(5)
            buy_card = self.buy_card(best_card)
            if not buy_card:
                if buy_errors >= 3:
                    self.log.error(
                        f"❌ <red>Buying upgrades has been interrupted due to errors ({buy_errors}).</red>"
                    )
                    return
                continue
            spent_amount = spent_amount + best_card["price"]
            profit_per_hour = profit_per_hour + best_card["profitPerHourDelta"]
            time.sleep(5)

        if spent_amount == 0 and profit_per_hour == 0:
            self.log.info(f"💴 <y>No upgrades available ...</y>")
        else:
            self.log.info(
                f"💸 <g>Upgrade completed, spent amount: <c>{'{:.2f}'.format(spent_amount)}💎</c>, "
                f"profit per hour: <c>{'{:.2f}'.format(profit_per_hour)}💎</c></g>"
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
            f"💳 <g>Start upgrading card <c>{cardName}</c> to level <c>{cardLevel}</c> for <c>{cardPrice}💎</c></g>"
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
            f"💰 <g>Card <c>{card['name']}</c> was upgraded to level <c>{card['level']}</c> for <c>{card['price']}💎</c></g>"
        )
        return True

    def get_available_cards(self, cards):
        new_cards = []
        expensive_cards = []
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

            coefficient_limit = getConfig("upgrade_coefficient", 200)
            card_coefficient = self.get_card_coefficient(card)
            if card_coefficient > coefficient_limit:
                expensive_cards.append(card)
                continue

            new_cards.append(card)

        expensive_card_names = ", ".join([f"<c>{card['name']}</c>" for card in expensive_cards])
        self.log.info(
            f"🪙 <y>Cards {expensive_card_names} exceeds the upgrade coefficient ({coefficient_limit}).</y>"
        )
        self.log.info(f"🪙 <y>You can adjust the coefficient in module settings.</y>")

        return new_cards

    def sort_cards(self, cards):
        return cards.sort(key=lambda x: x["price"] / x["profitPerHourDelta"])

    def get_card_coefficient(self, card):
        if card["price"] == 0 or card["profitPerHourDelta"] == 0:
            return 0
        return card["price"] / card["profitPerHourDelta"]
