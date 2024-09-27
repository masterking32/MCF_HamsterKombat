# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

from .Basic import Basic


class Cards:
    def __init__(self, log, HttpRequest):
        self.log = log
        self.http = HttpRequest
        self.basic = Basic(log, HttpRequest)

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
        return card["price"] / card["profitPerHourDelta"]
