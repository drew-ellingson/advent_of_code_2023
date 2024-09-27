from __future__ import annotations
from dataclasses import dataclass
from typing import List
from functools import reduce


def parse_range(raw_range: str) -> RangeMap:
    return RangeMap(*map(int, raw_range.split(" ")))


def parse_garden_map(raw_garden_map: str) -> GardenMap:
    lines = raw_garden_map.split("\n")

    src, tgt = lines[0].replace(" map:", "").split("-to-")
    range_maps = [parse_range(x) for x in lines[1:]]

    return GardenMap(src, tgt, range_maps)


def parse_garden(raw_garden: str) -> Garden:
    content_blocks = raw_garden.split("\n\n")

    seeds = [int(x) for x in content_blocks[0].replace("seeds: ", "").split(" ")]
    maps = [parse_garden_map(x) for x in content_blocks[1:]]

    return Garden(seeds, maps)


@dataclass
class RangeMap:
    tgt_start: int
    src_start: int
    rng: int


@dataclass
class GardenMap:
    src: str
    tgt: str
    range_maps: List[RangeMap]

    def transform(self, value):
        rel_rm = [
            rm
            for rm in self.range_maps
            if rm.src_start <= value <= rm.src_start + rm.rng
        ]
        if rel_rm:
            return rel_rm[0].tgt_start + (value - rel_rm[0].src_start)
        else:
            return value


@dataclass
class Garden:
    seeds: List[int]
    maps: List[GardenMap]

    # assumes maps are presented in order.
    def transform(self, value):
        steps = [m.transform for m in self.maps]

        def compose(f, g):
            return lambda x: g(f(x))

        return reduce(compose, steps)(value)


if __name__ == "__main__":
    with open("day_05/input2.txt") as input_file:
        content = input_file.read()
        garden = parse_garden(content)

    min_loc = min(garden.transform(x) for x in garden.seeds)

    print(f"P1 Soln is: {min_loc}")
