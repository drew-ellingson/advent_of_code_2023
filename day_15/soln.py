from dataclasses import dataclass, field
from typing import List


def compute_hash(raw: str) -> int:
    cv = 0
    for chr in raw:
        cv += ord(chr)
        cv *= 17
        cv = cv % 256
    return cv


@dataclass
class Instr:
    raw_instr: str

    label: str = field(init=False)
    op: str = field(init=False)
    focal_length: int = field(init=False)
    tgt_box: int = field(init=False)

    def __post_init__(self):
        if "=" in self.raw_instr:
            self.focal_length = int(self.raw_instr[-1])
            self.op = self.raw_instr[-2]
            self.label = self.raw_instr[:-2]
        else:
            self.focal_length = None
            self.op = self.raw_instr[-1]
            self.label = self.raw_instr[:-1]

        self.tgt_box = compute_hash(self.label)


@dataclass
class Lens:
    focal_length: int
    label: str


@dataclass
class LightBoxes:
    boxes: List[List[Lens]] = field(init=False)

    def __post_init__(self):
        self.boxes = [[] for _ in range(256)]

    def do_instr(self, instr: Instr) -> None:

        lens_slots = self.boxes[instr.tgt_box]

        if instr.op == "-":
            self.boxes[instr.tgt_box] = [
                x for x in lens_slots if x.label != instr.label
            ]
        else:
            match = [x for x in lens_slots if x.label == instr.label]
            if match:
                match[0].focal_length = instr.focal_length
            else:
                lens_slots.append(Lens(instr.focal_length, instr.label))

    def compute_focus_power(self):
        fp = 0
        for i, b in enumerate(self.boxes):
            for j, l in enumerate(b):
                fp += (i + 1) * (j + 1) * l.focal_length
        return fp


if __name__ == "__main__":
    with open("input.txt") as f:
        raws = f.read().split(",")
        instrs = [Instr(instr) for instr in raws]

    print(f"P1 Soln is: {sum(compute_hash(raw) for raw in raws)}")

    lb = LightBoxes()

    for i in instrs:
        lb.do_instr(i)

    print(f"P2 Soln is: {lb.compute_focus_power()}")
