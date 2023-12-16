from typing import List
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# valid exit directions by node
DIRS = {
    "S": [(1, 0), (0, 1), (-1, 0), (0, -1)],
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
    "J": [(-1, 0), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
}

# valid target nodes by direction
CONNS = {
    (1, 0): ["S", "|", "J", "L"],
    (-1, 0): ["S", "|", "7", "F"],
    (0, 1): ["S", "-", "J", "7"],
    (0, -1): ["S", "-", "L", "F"],
}

# vector addition
def _add(a1: tuple, a2: tuple) -> tuple:
    return tuple(map(sum, zip(a1, a2)))


class Maze:
    def __init__(self, maze: List[List[str]]):
        self.maze = maze
        self.start_pos = self.get_start_pos()
        self.cycle = self.build_cycle()

    def __repr__(self) -> str:
        msg = ""
        for row in self.maze:
            msg = msg + "".join(row) + "\n"

        msg = msg + "\n" + f"start pos: {self.start_pos}"
        return msg

    def get_start_pos(self) -> tuple:
        for i, row in enumerate(self.maze):
            try:
                return (i, row.index("S"))
            except ValueError:
                continue

    def get(self, pos: tuple) -> str:
        return self.maze[pos[0]][pos[1]]

    def get_neighbors(self, pos: tuple) -> List[tuple]:
        """given a node, return a list of valid connected nodes"""
        val = self.get(pos)
        neighbors = [
            _add(pos, vec)
            for vec in DIRS[val]
            if self.get(_add(pos, vec)) in CONNS[vec]
        ]
        return neighbors

    def one_step(self, path: List[tuple]) -> List[List[tuple]]:
        """given a path, return a list of valid paths extending that path"""
        neighbors = [
            x
            for x in self.get_neighbors(path[-1])
            if x not in path or (len(path) > 2 and x == self.start_pos)
        ]
        return [path + [n] for n in neighbors]

    def build_cycle(self) -> List[List[tuple]]:
        paths = [[(self.start_pos)]]
        while not any(p[0] == p[-1] and len(p) > 1 for p in paths):
            paths = [p for path in paths for p in self.one_step(path)]
        return [p for p in paths if p[0] == p[-1]][0]

    def get_farthest_distance(self):
        return (len(self.cycle) - 1) // 2

    def get_enclosed_area(self):
        """return number of points strictly enclosed by the cycle (not convex hull)"""
        poly = Polygon(self.cycle)
        interior = [
            (i, j)
            for i in range(len(self.maze))
            for j in range(len(self.maze[0]))
            if (i, j) not in self.cycle and poly.contains(Point((i, j)))
        ]
        return len(interior)


if __name__ == "__main__":
    with open("input.txt") as f:
        maze = Maze([[v for v in l.strip()] for l in f.readlines()])

print(f"P1 Soln is: {maze.get_farthest_distance()}")
print(f"P2 Soln is: {maze.get_enclosed_area()}")
