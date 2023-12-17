from typing import List, TypeVar

T = TypeVar("T")


def list_diff(l1: List[T], l2: List[T]) -> int:
    """assumes len(l1) = len(l2) and finds # of indices diff"""
    return len([i for i, x in enumerate(l1) if l1[i] != l2[i]])


class Grid:
    def __init__(self, raw_grid: str):
        self.raw_grid = raw_grid

        self.rows = self.parse_grid()

        self.w = len(self.rows[0])
        self.h = len(self.rows)

        self.cols = [[row[i] for row in self.rows] for i in range(self.w)]

    def parse_grid(self) -> List[List[str]]:
        return [[x for x in row] for row in self.raw_grid.split("\n")]

    def vert_sym_diff(self, left_idx: int) -> int:
        """
        Given a left index, determine how many smudges away from a vertical reflection
        across that index we are.
        """
        match_cols = min([left_idx, self.w - left_idx]) + 1
        return sum(
            list_diff(self.cols[left_idx - i], self.cols[left_idx + i - 1])
            for i in range(1, match_cols)
        )

    def find_vert_sym(self, req_diff: int = 0) -> int:
        """
        Find an index that is req_diff smudges away from a vertical reflection.
        For part 1 this is 0, for part 2 this is 1.
        """
        vert_sym = [i for i in range(1, self.w) if self.vert_sym_diff(i) == req_diff]
        if vert_sym:
            return vert_sym[0]
        return 0

    def hor_sym_diff(self, top_idx: int) -> int:
        """
        given a top index, determine how many smudges away from a horizontal reflection
        across that index we are.
        """
        match_rows = min([top_idx, self.h - top_idx]) + 1
        return sum(
            list_diff(self.rows[top_idx - i], self.rows[top_idx + i - 1])
            for i in range(1, match_rows)
        )

    def find_hor_sym(self, req_diff: int = 0) -> int:
        """
        Find an index that is req_diff smudges away from a horizontal reflection.
        For part 1 this is 0, for part 2 this is 1.
        """
        hor_sym = [i for i in range(1, self.h) if self.hor_sym_diff(i) == req_diff]
        if hor_sym:
            return hor_sym[0]
        return 0

    def score_grid(self, req_diff: int = 0) -> int:
        return 100 * self.find_hor_sym(req_diff) + self.find_vert_sym(req_diff)


if __name__ == "__main__":
    with open("input.txt") as f:
        grids = f.read().split("\n\n")
    grids = [Grid(grid) for grid in grids]

    print(f"P1 Soln is: {sum(grid.score_grid() for grid in grids)}")
    print(f"P2 Soln is: {sum(grid.score_grid(req_diff=1) for grid in grids)}")
