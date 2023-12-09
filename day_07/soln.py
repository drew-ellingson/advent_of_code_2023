from dataclasses import dataclass, field
from typing import List
from collections import Counter
from functools import cmp_to_key
from copy import copy

P1_CARD_VALS = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

P2_CARD_VALS = copy(P1_CARD_VALS)
P2_CARD_VALS["J"] = 0


@dataclass
class Hand:
    raw_cards: List[str] = field(repr=False)
    bid: int
    part: int = field(default=1)

    cards: List[int] = field(init=False)

    def __post_init__(self):
        self.cards = [
            (P1_CARD_VALS if self.part == 1 else P2_CARD_VALS)[x]
            for x in self.raw_cards
        ]

    def get_hand_score(self):
        c = Counter(self.cards)

        if self.part == 2:  # replace jokers with copies of most freq card
            j = c[0]
            del c[0]
            if c:
                max_card = max(c.keys(), key=lambda x: c[x])
                c[max_card] += j
            else:
                return 7  # edge case: 5 Jokers
        counts = c.values()

        if 5 in counts:
            return 7  # five of a kind
        elif 4 in counts:
            return 6  # four of a kind
        elif 3 in counts and 2 in counts:
            return 5  # full house
        elif 3 in counts:
            return 4  # three of a kind
        elif 2 in counts and len(counts) <= 3:
            return 3  # two pair
        elif 2 in counts:
            return 2  # pair
        else:
            return 1  # high card


@dataclass
class Game:
    hands: List[Hand]

    def compare(self, h1, h2):
        if h1.get_hand_score() < h2.get_hand_score():
            return -1
        elif h1.get_hand_score() > h2.get_hand_score():
            return 1
        else:
            if h1.cards < h2.cards:
                return -1
            elif h1.cards > h2.cards:
                return 1
            else:
                return 0

    def get_total_winnings(self):
        ranked_hands = sorted(self.hands, key=cmp_to_key(self.compare))
        return sum(h.bid * (i + 1) for i, h in enumerate(ranked_hands))


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [x.strip().split(" ") for x in f.readlines()]
        raw_cards, bids = [x[0] for x in lines], [int(x[1]) for x in lines]

    p1_game = Game([Hand(c, b, 1) for c, b in zip(raw_cards, bids)])
    p2_game = Game([Hand(c, b, 2) for c, b in zip(raw_cards, bids)])

print(f"P1 Soln is: {p1_game.get_total_winnings()}")
print(f"P2 Soln is: {p2_game.get_total_winnings()}")
