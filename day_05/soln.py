from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Interval:
    src_start: int # flipping src and tgt from aoc statement
    tgt_start: int 
    rng: int 

@dataclass
class GardenMap:
    raw_map: str = field(repr = False)
    
    src: str = field(init=False)
    tgt: str = field(init=False)
    intervals: List[Interval] = field(init=False)

    def __post_init__(self) -> None:
        self.src, self.tgt = self.__parse_src_tgt()
        self.intervals = self.__parse_intervals()

    def __parse_src_tgt(self) -> tuple:
        src_tgt = self.raw_map.split('\n')[0].replace(' map:', '')
        src_tgt = src_tgt.split('-')
        return src_tgt[0], src_tgt[2]
    
    def __parse_intervals(self) -> dict:
        lines = self.raw_map.split('\n')[1:] # ignore source and target heading
        lines = [[int(val) for val in row.split(' ')] for row in lines]
        return [Interval(l[1], l[0], l[2]) for l in lines]

    def find_tgt_val(self, val) -> int:
        # assuming non overlapping intervals
        rel_int = [i for i in self.intervals if i.src_start <= val < i.src_start + i.rng]
        if rel_int:
            diff = val - rel_int[0].src_start
            return rel_int[0].tgt_start + diff
        else:
            return val
        
@dataclass
class Garden:
    raw_garden: str = field(repr = False)

    p1_seeds: List[int] = field(init=False)
    p2_seeds: List[int] = field(init=False)

    garden_maps: List[GardenMap] = field(init=False)

    def __post_init__(self) -> None:
        comps = self.raw_garden.split('\n\n')
        self.p1_seeds = [int(x) for x in comps[0].replace('seeds: ', '').split(' ')]

        p2_seeds = []
        for s in range(0, len(self.p1_seeds), 2):
            new_range = list(range(self.p1_seeds[s], self.p1_seeds[s] + self.p1_seeds[s+1]))
            p2_seeds.extend(new_range)
        
        self.p2_seeds = p2_seeds

        self.garden_maps = [GardenMap(raw_map) for raw_map in comps[1:]] 

    def find_location(self, seed) -> int:
        curr_src, curr_val = 'seed', seed
        while curr_src != 'location':
            curr_map = [m for m in self.garden_maps if m.src == curr_src][0]
            curr_val = curr_map.find_tgt_val(curr_val)
            curr_src = curr_map.tgt
        return curr_val

    def find_min_loc(self, part=1) -> int:
        seeds = self.p1_seeds if part == 1 else self.p2_seeds
        return min(self.find_location(s) for s in seeds)

if __name__=="__main__":
    with open('input2.txt') as f:
        raw_garden = f.read()
        garden = Garden(raw_garden)

print(f'P1 Soln is: {garden.find_min_loc(part=1)}')
print(f'P2 Soln is: {garden.find_min_loc(part=2)}')