from dataclasses import dataclass
from random import shuffle


@dataclass(frozen=True)
class Card:
    suit: str
    rank: int

    def __post_init__(self):
        if self.suit not in ("S", "H", "D", "C"):
            raise ValueError("suit must be one of 'S', 'H', 'D', 'C'")
        if self.rank not in range(1, 14):
            raise ValueError("rank must be an integer between 1 and 13")

    def __str__(self):
        suit_str = {"S": "♠", "H": "♥", "D": "♦", "C": "♣"}[self.suit]
        rank_str = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(
            self.rank, str(self.rank))
        return f"{rank_str}{suit_str}"


def standard_deck():
    return [Card(suit, rank) for suit in "SHDC" for rank in range(1, 14)]


def shuffled_deck():
    cards = standard_deck()
    shuffle(cards)
    return cards


def deal_one_five_card_hand():
    deck = shuffled_deck()
    return set(deck[:5])


def deal(number_of_hands, cards_per_hand):
    # Return a list of sets, each containing the cards for one hand.
    # You must validate the input parameters according to the test
    # cases that you will find in cards_test.py. Make sure to remove
    # this comment and the pass statement below before submitting.
    pass


def poker_classification(hand):
    # Returns a string describing the poker hand. First, validate the input
    # to make sure it is a set of 5 cards, and raise the appropriate error
    # (TypeError or ValueError) if necessary.
    #
    # Then return one of the following strings:
    # "High Card", "One Pair", "Two Pair", "Three of a Kind",
    # "Straight", "Flush", "Full House", "Four of a Kind",
    # "Straight Flush", "Royal Flush"
    #
    # Make sure to remove this comment and the pass statement below
    # before submitting.
    pass
