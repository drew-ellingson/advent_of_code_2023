from dataclasses import dataclass, field
from typing import List
import re
from collections import defaultdict, UserList


@dataclass
class Card:
    id: int
    winning_nums: List[int]
    guess_nums: List[int]

    common_nums: List[int] = field(init=False)

    def __post_init__(self) -> None:
        self.common_nums = [x for x in self.winning_nums if x in self.guess_nums]

    def score_card_p1(self) -> int:
        return 2 ** (len(self.common_nums) - 1) if self.common_nums else 0


@dataclass
class CardCollection(UserList):
    data: List[Card]

    def score_cards_p2(self) -> int:
        card_mults = defaultdict(lambda: 1)

        for i, card in enumerate(self.data):
            cards_to_copy = list(range(i + 1, i + len(card.common_nums) + 1))
            if not cards_to_copy:  # explicitly catch the no matches case
                card_mults[i] = max(card_mults[i], 1)
            for j in cards_to_copy:
                card_mults[j] += card_mults[i]
        return sum(card_mults.values())


def parse_card(line) -> Card:
    line = re.sub(r" +", " ", line) # remove excess space for 1 digit nums

    id_part, cards_part = line.split(": ")
    id = int(id_part.split(" ")[-1])

    winning_nums, guess_nums = cards_part.split(" | ")

    winning_nums = [int(x) for x in winning_nums.split(" ")]
    guess_nums = [int(x) for x in guess_nums.split(" ")]

    return Card(id, winning_nums, guess_nums)


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        cards = CardCollection([parse_card(line) for line in lines])

print(f"P1 Soln is: {sum(c.score_card_p1() for c in cards)}")
print(f"P2 Soln is: {cards.score_cards_p2()}")
