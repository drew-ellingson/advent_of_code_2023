from dataclasses import dataclass
from typing import List


@dataclass
class Sequence:
    seq: List[int]

    def get_next_term(self, p2=False):
        diffs = [self.seq]
        while any(x != 0 for x in diffs[-1]):
            curr = diffs[-1]
            new = [curr[i + 1] - curr[i] for i in range(len(curr) - 1)]
            diffs.append(new)
        if not p2:
            return sum(x[-1] for x in diffs)
        else:
            return sum((-1) ** i * x[0] for i, x in enumerate(diffs))


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [[int(y) for y in x.strip().split(" ")] for x in f.readlines()]
        sequences = [Sequence(line) for line in lines]

print(f"P1 Soln is: {sum(s.get_next_term() for s in sequences)}")
print(f"P2 Soln is: {sum(s.get_next_term(p2=True) for s in sequences)}")
