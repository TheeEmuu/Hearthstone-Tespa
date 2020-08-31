from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType
import hearthstone.deckstrings
import json

cardDatabase = {}


def main():
    initialize()

    deck = Deck.from_deckstring("AAECAR8engGoArUDxwOHBMkErgbFCNsJ7Qn+DJjwAp7wAu/xAqCAA6eCA5uFA/WJA+aWA/mWA76YA7acA56dA/yjA+WkA5+lA6KlA6alA4SnA5+3AwAA")

    for x in deck.cards:
        print("{0}x {1}".format(x[1], get_card(x[0])))


def get_card(ident):
    return cardDatabase.get(ident)


def initialize():
    with open("cards.collectible.json", encoding="utf8") as json_object:
        data = json.load(json_object)

        for x in data:
            cardDatabase[x["dbfId"]] = x["name"]


main()
