from dataclasses import dataclass, field
from typing import List

RED_LIMIT = 12
GREEN_LIMIT = 13
BLUE_LIMIT = 14


@dataclass
class Draw:
    r: int
    g: int
    b: int


@dataclass
class Game:
    id: int
    draws: List[Draw]
    power: int = field(init=False)

    def __post_init__(self):
        self.power = self.get_power()

    def is_possible(self) -> bool:
        return not any(
            draw.r > RED_LIMIT or draw.g > GREEN_LIMIT or draw.b > BLUE_LIMIT
            for draw in self.draws
        )

    def get_power(self) -> int:
        r_max = max(draw.r for draw in self.draws)
        g_max = max(draw.g for draw in self.draws)
        b_max = max(draw.b for draw in self.draws)
        return r_max * g_max * b_max


def parse_draw(draw) -> Draw:
    r, g, b = 0, 0, 0
    cubes = draw.split(", ")
    print(cubes)
    for color in cubes:
        if color.endswith("red"):
            r = int(color.split(" ")[0])
        if color.endswith("green"):
            g = int(color.split(" ")[0])
        if color.endswith("blue"):
            b = int(color.split(" ")[0])
    return Draw(r, g, b)


def parse_game(line) -> Game:
    id, draws = [x.strip() for x in line.split(":")]
    id = int(id.split(" ")[-1])

    draws = [parse_draw(d) for d in draws.split("; ")]
    return Game(id, draws)


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        games = [parse_game(line) for line in lines]

    print(f"P1 Soln is: {sum(game.id for game in games if game.is_possible())}")
    print(f"P2 Soln is: {sum(game.power for game in games)}")
