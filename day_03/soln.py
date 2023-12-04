from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict
import re
from functools import reduce


@dataclass
class Part:
    num: int
    start: tuple


@dataclass
class Engine:
    raw_grid: str
    grid: List[List[str]] = field(init=False)
    parts: List[Part] = field(init=False, default_factory=list)
    symbol_locs: Dict[str, List[tuple]] = field(
        init=False, default_factory=lambda: defaultdict(lambda: [])
    )

    def __post_init__(self) -> None:
        self.grid = [[col for col in row.strip()] for row in self.raw_grid.split("\n")]

        int_re = re.compile(r"\d+")
        symbol_re = re.compile(r"([^\d.])")

        for i, row in enumerate(self.raw_grid.split("\n")):
            parts = int_re.finditer(row)  # returns iterator of match objects
            self.parts.extend(Part(int(m[0]), (i, m.start(0))) for m in parts)

            symbols = symbol_re.finditer(row)
            for s in symbols:
                self.symbol_locs[s[0]].append((i, s.start(0)))

    def get_adjacent_parts(self, x: tuple) -> List[Part]:
        r, c = x[0], x[1]
        return list(
            filter(
                lambda p: abs(p.start[0] - r) <= 1
                and p.start[1] - 1 <= c <= p.start[1] + len(str(p.num)),
                self.parts,
            )
        )

    def get_adjacent_symbols(self, part: Part) -> List[tuple]:
        c_1, c_2 = part.start[1], part.start[1] + len(str(part.num))
        r = part.start[0]

        # flatten dict values to get list of all symbol locs, regardless of type
        all_symbol_locs = list(
            reduce(lambda x, y: x + y, self.symbol_locs.values(), [])
        )
        return list(
            filter(
                lambda x: abs(x[0] - r) <= 1 and c_1 - 1 <= x[1] <= c_2,
                all_symbol_locs,
            )
        )

    def sum_valid_parts(self) -> int:
        return sum(
            part.num for part in self.parts if len(self.get_adjacent_symbols(part)) > 0
        )

    def sum_gear_ratios(self) -> int:
        gear_ratio = 0
        for s in self.symbol_locs["*"]:
            adj_parts = self.get_adjacent_parts(s)
            if not len(adj_parts) == 2:
                continue
            gear_ratio += adj_parts[0].num * adj_parts[1].num
        return gear_ratio


if __name__ == "__main__":
    with open("input.txt") as f:
        raw_grid = f.read()
        engine = Engine(raw_grid)

    print(f"P1 Soln is: {engine.sum_valid_parts()}")
    print(f"P2 Soln is: {engine.sum_gear_ratios()}")
