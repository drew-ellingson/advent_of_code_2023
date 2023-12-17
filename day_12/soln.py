from dataclasses import dataclass
from typing import List, Tuple
from itertools import groupby


@dataclass
class SpringRow:
    springs: List[str]
    segments: List[int]

    def get_partial_segments(self, resolved: List[str]) -> List[int]:
        gps = groupby(resolved)
        return [len(list(g[1])) for g in gps if g[0] == "#"]

    def is_invalid(self, partially_resolved: List[str]) -> bool:
        try:
            resolved = partially_resolved[: partially_resolved.index("?")]
        except ValueError:
            resolved = partially_resolved

        partial_segs = self.get_partial_segments(resolved)

        if sum(self.segments) - sum(partial_segs) > len(partially_resolved) - len(
            resolved
        ):
            return True
        elif len(partial_segs) > len(self.segments):
            return True
        elif partial_segs and partial_segs[-1] > self.segments[len(partial_segs) - 1]:
            return True
        elif (
            partial_segs
            and partial_segs[-1] < self.segments[len(partial_segs) - 1]
            and resolved[-1] == "."
        ):
            return True
        elif len(partial_segs) > 1 and any(
            partial_segs[i] != self.segments[i] for i in range(len(partial_segs) - 1)
        ):
            return True
        else:
            return False

    def one_step(self, partially_resolved: List[str]) -> List[List[str]]:
        res_idx = partially_resolved.index("?")

        damaged = [
            "#" if i == res_idx else x for (i, x) in enumerate(partially_resolved)
        ]
        working = [
            "." if i == res_idx else x for (i, x) in enumerate(partially_resolved)
        ]

        return [x for x in [damaged, working] if not self.is_invalid(x)]

    def count_valid_confs(self) -> int:
        partial_springs = [self.springs]
        while any("?" in ps for ps in partial_springs):
            new_partial_springs = []
            for ps in partial_springs:
                new_partial_springs.extend(self.one_step(ps))
            partial_springs = new_partial_springs
        return len(
            [
                x
                for x in partial_springs
                if self.get_partial_segments(x) == self.segments
            ]
        )


class SpringField:
    def __init__(self, raw_sf: str, p2:bool=False):
        self.raw_sf = raw_sf
        self.p2 = p2
        self.spring_rows = self.parse_raw_input()

    def __repr__(self) -> str:
        msg = ""
        for a in self.spring_rows:
            msg = msg + str(a) + "\n"
        return msg

    def parse_raw_input(self) -> List[SpringRow]:
        lines = self.raw_sf.split("\n")
        return [
            SpringRow(*[self.parse_line(line) for line in lines][i])
            for i in range(len(lines))
        ]

    def parse_line(self, raw_line: str) -> Tuple[List[str], List[int]]:
        springs, sections = raw_line.split(" ")
        if self.p2:
            sections = (5 * (sections + ","))[:-1]
            springs = (5 * (springs + "?"))[:-1]
        springs = [x for x in springs]
        sections = [int(x) for x in sections.split(",")]

        return springs, sections


if __name__ == "__main__":
    with open("input2.txt") as f:
        content = f.read()
        sf = SpringField(content)
        sf2 = SpringField(content, p2=True)

    print(
        f"P1 Soln is: {sum(sf.spring_rows[i].count_valid_confs() for i in range(len(sf.spring_rows)))}"
    )
    print(
        f"P2 Soln is: {sum(sf2.spring_rows[i].count_valid_confs() for i in range(len(sf2.spring_rows)))}"
    )
