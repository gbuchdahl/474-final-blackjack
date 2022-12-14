from typing import List, Tuple, Optional
from random import shuffle


class Card:
    """
    Hands, Shoes are composed of card objects
    """

    def __init__(self, value: int) -> None:
        self.value = value

    def get_value(self) -> int:
        return min(self.value, 10)

    def __repr__(self) -> str:
        if self.value == 1:
            return "Ace"
        elif self.value == 11:
            return "Jack"
        elif self.value == 12:
            return "Queen"
        elif self.value == 13:
            return "King"
        else:
            return str(self.value)


class Hand:
    """
    Collection of cards that has a soft or hard value
    A few other helpers are defined here: is_blackjack, is_bust
    """

    def __init__(self, cards: Optional[List[Card]] = None):
        if cards is None:
            cards = []
        self.cards = cards
        self.value: int = sum([card.get_value() for card in self.cards])

    def add_card(self, card: Card) -> None:
        self.cards.append(card)
        self.value += card.get_value()

    def get_value(self) -> Tuple[int, bool]:
        """
        :return: value, is_soft
        """
        num_aces = len([card for card in self.cards if card.value == 1])
        if num_aces == 0:
            return self.value, False
        else:
            value = self.value
            for i in range(num_aces):
                value += 10
                if value <= 21:
                    return value, True
                else:
                    value -= 10

            return value, False

    def is_bust(self) -> bool:
        return self.get_value()[0] > 21

    def is_blackjack(self):
        return len(self) == 2 and self.get_value()[0] == 21

    def __repr__(self):
        value = self.get_value()[0]
        is_soft = self.get_value()[1]
        if self.is_blackjack():
            return f"Blackjack! {self.cards[0]} and {self.cards[1]}"
        return f"{'Soft' if is_soft else 'Hard'} " + str(value) + f" -- {str(self.cards)}"

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, index):
        return self.cards[index]


class Shoe:
    """
    Composed of num_decks decks of Card objects
    Can be shuffled, dealt, and provides methods for card counting
    """

    def __init__(self, num_decks: int = 2, is_stacked=False):
        self.cards: List[Card] = []
        self.discards: List[Card] = []
        self.__num_decks = num_decks
        for i in range(num_decks):
            for value in range(1, 14):
                self.cards.append(Card(value))
                self.cards.append(Card(value))
                self.cards.append(Card(value))
                self.cards.append(Card(value))
            if is_stacked:
                for value in range(10, 14):
                    self.cards.append(Card(value))
                    self.cards.append(Card(value))
                self.cards.append(Card(1))
                self.cards.append(Card(1))
        self.count = 0
        self.shuffle()

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        self.count = 0
        shuffle(self.cards)

    def deal(self) -> Card:
        if len(self.cards) <= 10:
            self.cards = self.cards + self.discards
            self.discards = []
            self.shuffle()
        card = self.cards.pop()
        self.discards.append(card)
        if card.get_value() == 10 or card.get_value() == 1:
            self.count -= 1
        elif card.get_value() <= 6:
            self.count += 1
        return card

    def deal_hand(self) -> Hand:
        hand = Hand()
        hand.add_card(self.deal())
        hand.add_card(self.deal())
        return hand

    def get_count(self) -> int:
        return self.count

    def __repr__(self):
        return f"{self.__num_decks} deck shoe with {len(self.cards)} cards left"
