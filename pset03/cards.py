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
    if not isinstance(number_of_hands, int) or not isinstance(cards_per_hand, int):
        raise TypeError("number_of_hands and cards_per_hand must be integers")
    if number_of_hands <= 0 or cards_per_hand <= 0:
        raise ValueError("number_of_hands and cards_per_hand must be positive")
    if number_of_hands * cards_per_hand > 52:
        raise ValueError("Not enough cards in deck")

    deck = shuffled_deck()
    hands = []
    for i in range(number_of_hands):
        start = i * cards_per_hand
        end = start + cards_per_hand
        hands.append(set(deck[start:end]))
    return hands


def poker_classification(hand):
    if not isinstance(hand, set):
        raise TypeError("hand must be a set")
    if len(hand) != 5:
        raise ValueError("hand must contain exactly 5 cards")
    if not all(isinstance(card, Card) for card in hand):
        raise TypeError("hand must contain only Card objects")

    ranks = sorted([card.rank for card in hand])
    suits = [card.suit for card in hand]

    if ranks == [1, 10, 11, 12, 13]:
        straight = True
    else:
        straight = all(ranks[i] + 1 == ranks[i + 1] for i in range(4))
    flush = len(set(suits)) == 1

    counts = {rank: ranks.count(rank) for rank in ranks}
    counts_values = sorted(counts.values(), reverse=True)

    if straight and flush and ranks[-1] == 13 and ranks[0] == 1:
        return "Royal Flush"
    elif straight and flush:
        return "Straight Flush"
    elif counts_values == [4, 1]:
        return "Four of a Kind"
    elif counts_values == [3, 2]:
        return "Full House"
    elif flush:
        return "Flush"
    elif straight:
        return "Straight"
    elif counts_values == [3, 1, 1]:
        return "Three of a Kind"
    elif counts_values == [2, 2, 1]:
        return "Two Pair"
    elif counts_values == [2, 1, 1, 1]:
        return "One Pair"
    else:
        return "High Card"
