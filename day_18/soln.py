from dataclasses import dataclass, field
from typing import Tuple, List 
from shapely.geometry import Point as s_point
from shapely.geometry.polygon import Polygon


dirs = {
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
    'U': (-1, 0),
}

def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))

def _mult(tup, scal):
    return tuple(scal * x for x in tup)

@dataclass
class Point:
    pos: Tuple[int]
    color: str = field(default = None)

@dataclass
class Instr:
    dir: str
    steps: int 
    color: str

def follow_instrs(instrs):
    curr_pos = (0,0)
    visited = [Point(curr_pos, instrs[0].color)]
    
    for i in instrs:
        for s in range(1, i.steps + 1):
            curr_pos = _add(curr_pos, dirs[i.dir])
            visited.append(Point(curr_pos, i.color))
    return visited

class Grid:
    def __init__(self, points):
        self.points = points
        self.h = max(x.pos[0] for x in self.points) + 1
        self.w = max(x.pos[1] for x in self.points) + 1

    def get_enclosed_area(self):
        """return number of points strictly enclosed by the cycle (not convex hull)"""
        
        poly = Polygon([p.pos for p in self.points])
        interior = [
            (i, j)
            for i in range(self.h)
            for j in range(self.w)
            if any(p.pos == (i,j) for p in self.points) or poly.contains(s_point((i, j)))
        ]
        return len(interior)

if __name__=="__main__":
    with open('input2.txt') as f:
        instrs = [line.strip().split(' ')  for line in f.readlines()]

    instrs = [Instr(x[0], int(x[1]), x[2][1:-1]) for x in instrs]

    points = follow_instrs(instrs)
    grid = Grid(points)

    print(f'Part 1 Soln is: {grid.get_enclosed_area()}')