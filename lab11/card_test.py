import pytest
from card import Card, standard_deck, shuffled_deck, deal_one_five_card_hand


def test_valid_cards():
    assert str(Card(suit="H", rank=10)) == "10♥"
    assert str(Card(suit="S", rank=1)) == "A♠"
    assert str(Card(suit="D", rank=11)) == "J♦"
    assert str(Card(suit="C", rank=12)) == "Q♣"
    assert str(Card(suit="H", rank=13)) == "K♥"
    assert str(Card(suit="S", rank=5)) == "5♠"
    assert str(Card(suit="D", rank=3)) == "3♦"
    assert str(Card(suit="C", rank=2)) == "2♣"


def test_invalid_suit():
    with pytest.raises(ValueError):
        Card(suit="X", rank=5)
    with pytest.raises(ValueError):
        Card(suit="SPADES", rank=10)


def test_invalid_rank():
    with pytest.raises(ValueError):
        Card(suit="S", rank=14)
    with pytest.raises(ValueError):
        Card(suit="D", rank=0)
    with pytest.raises(ValueError):
        Card(suit="D", rank=3.5)
    with pytest.raises(ValueError):
        Card(suit="D", rank="10")


def test_cards_are_truly_immutable():
    card = Card(suit="H", rank=10)
    with pytest.raises(AttributeError):
        card.suit = "S"
    with pytest.raises(AttributeError):
        card.rank = 5
    with pytest.raises(AttributeError):
        card.dog = "dog"


def test_standard_deck():
    deck = standard_deck()
    assert isinstance(deck, list)
    assert len(deck) == 52
    assert all(isinstance(card, Card) for card in deck)
    deck_as_string = ''.join(str(card) for card in deck)
    assert deck_as_string == (
        "A♠2♠3♠4♠5♠6♠7♠8♠9♠10♠J♠Q♠K♠"
        "A♥2♥3♥4♥5♥6♥7♥8♥9♥10♥J♥Q♥K♥"
        "A♦2♦3♦4♦5♦6♦7♦8♦9♦10♦J♦Q♦K♦"
        "A♣2♣3♣4♣5♣6♣7♣8♣9♣10♣J♣Q♣K♣")


def test_shuffled_deck():
    deck = standard_deck()
    assert isinstance(deck, list)
    assert len(deck) == 52
    shuffled = shuffled_deck()
    assert isinstance(shuffled, list)
    assert len(shuffled) == 52
    for suit in "SHDC":
        for rank in range(1, 14):
            assert Card(suit, rank) in shuffled


def test_deal_one_five_card_hand():
    hand = deal_one_five_card_hand()
    assert isinstance(hand, set)
    assert len(hand) == 5
    assert all(isinstance(card, Card) for card in hand)
