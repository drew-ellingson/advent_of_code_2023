from dataclasses import dataclass
import re
from math import prod, sqrt, ceil, floor


@dataclass
class Race:
    time: int
    distance: int

    def get_dist(self, hold_time) -> int:
        return max((self.time - hold_time) * hold_time, 0)

    def count_winning_holds(self)-> int:
        return len([x for x in range(self.time) if self.get_dist(x) > self.distance])

    def compute_winning_holds(self)-> int:
        # ht - h^2 = d
        # h^2 - th + d = 0
        # zeroes at (t +-sqrt(t^2-4d))/2
        disc = sqrt(self.time**2 - 4 * self.distance)
        zeroes = (self.time + disc) / 2, (self.time - disc) / 2

        return floor(zeroes[0]) - ceil(zeroes[1]) + 1


if __name__ == "__main__":
    with open("input.txt") as f:
        input = re.sub(r" +", " ", f.read())
        input = re.sub(r"Time:|Distance:", "", input)
        p1_times, p1_distances = [x.strip() for x in input.split("\n")]
        p1_times = [int(x) for x in p1_times.split(" ")]
        p1_distances = [int(x) for x in p1_distances.split(" ")]

        p2_times = int("".join([str(x) for x in p1_times]))
        p2_distances = int("".join([str(x) for x in p1_distances]))

    p1_races = [Race(x[0], x[1]) for x in zip(p1_times, p1_distances)]
    p2_race = Race(p2_times, p2_distances)

    print(f"P1 Soln is: {prod(r.count_winning_holds() for r in p1_races)}")
    print(f"P2 Soln is: {p2_race.compute_winning_holds()}")
