from dataclasses import dataclass, field
from typing import List, Tuple
import math


@dataclass
class SkyPatch:
    val: str
    weight: int = field(default=1)


class SkyImage:
    def __init__(self, image: List[List[SkyPatch]]):
        self.image = image
        self.update_weights()

    def __repr__(self) -> str:
        """Display print-friendly skyimage, as well as pixel weights due to
        cosmic expansion."""

        msg = "Image:\n"
        for row in image:
            msg = msg + "".join(p.val for p in row) + "\n"

        msg += "\nWeights:\n"

        for row in image:
            msg = msg + "".join(str(p.weight) for p in row) + "\n"

        return msg

    def get_patch(self, pos: Tuple[int]) -> SkyPatch:
        return self.image[pos[0]][pos[1]]

    def update_weights(self, exp_constant=2) -> None:
        """For empty rows or columns, multiply weight by exp_constant"""
        for row in self.image:
            if not any(i.val == "#" for i in row):
                for i in row:
                    i.weight *= exp_constant
        for col_idx in range(len(self.image[0])):
            if not any(row[col_idx].val == "#" for row in self.image):
                for row in self.image:
                    row[col_idx].weight *= exp_constant

    def reset_weights(self):
        for row in self.image:
            for col in row:
                col.weight = 1

    def compute_cost(self, pos1: Tuple[int], pos2: Tuple[int]):
        """a kludgey boi"""
        my_sum = 0
        while pos1 != pos2:
            try:
                y_sign = (pos2[0] - pos1[0]) / abs(pos2[0] - pos1[0])
            except ZeroDivisionError:
                y_sign = 0
            try:
                x_sign = (pos2[1] - pos1[1]) / abs(pos2[1] - pos1[1])
            except ZeroDivisionError:
                x_sign = 0

            cand1 = (int(pos1[0] + y_sign * 1), pos1[1])
            cand2 = (pos1[0], int(pos1[1] + x_sign * 1))

            if y_sign == 0:
                next_step = cand2
            elif x_sign == 0:
                next_step = cand1
            else:
                next_step = min([cand1, cand2], key=lambda x: self.get_patch(x).weight)

            my_sum += self.get_patch(next_step).weight
            pos1 = next_step

        return my_sum

    def path_sum(self) -> int:
        galaxies = [
            (i, j)
            for i in range(len(self.image))
            for j in range(len(self.image[0]))
            if self.get_patch((i, j)).val == "#"
        ]
        # relying on lexi ordering for tuples
        galaxy_pairs = [(x, y) for x in galaxies for y in galaxies if y > x]

        return sum(self.compute_cost(*a) for a in galaxy_pairs)


if __name__ == "__main__":
    with open("input.txt") as f:
        image = [[SkyPatch(x) for x in row.strip()] for row in f.readlines()]
        si = SkyImage(image)

print(f"P1 Soln is: {si.path_sum()}")

si.reset_weights()
si.update_weights(exp_constant=1000000)

print(f"P2 Soln is: {si.path_sum()}")
