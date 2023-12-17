from copy import copy


class RockField:
    def __init__(self, rows):
        self.rows = rows

        self.w = len(rows[0])
        self.h = len(rows)

        self.cols = ["".join([row[i] for row in self.rows]) for i in range(self.w)]

    def sync_reps(self, source="rows"):
        """takes source of 'rows' or 'cols' and updates the other representation"""

        if source == "rows":
            self.cols = ["".join([row[i] for row in self.rows]) for i in range(self.w)]
        else:
            self.rows = ["".join([col[i] for col in self.cols]) for i in range(self.h)]

    def tilt(self, dir):
        my_strings = self.cols if dir in ["north", "south"] else self.rows
        reverse = dir in ["north", "west"]
        source = "cols" if dir in ["north", "south"] else "rows"

        for i, x in enumerate(my_strings):
            chunks = x.split("#")
            tilt_chunks = ["".join(sorted(chunk, reverse=reverse)) for chunk in chunks]
            tilted = "#".join(tilt_chunks)
            my_strings[i] = tilted

        self.sync_reps(source=source)

    def cycle(self):
        self.tilt(dir="north")
        self.tilt(dir="west")
        self.tilt(dir="south")
        self.tilt(dir="east")

    def find_period(self):
        """
        find the recurring period and index at which that period starts
        afterwards, reset rows and cols to original values
        """
        orig_rows, orig_cols = copy(self.rows), copy(self.cols)
        cycle_ends = [self.rows]

        while cycle_ends[-1] not in cycle_ends[:-1]:
            self.cycle()
            cycle_ends.append(self.rows)

        period_start = cycle_ends.index(cycle_ends[-1])
        period = len(cycle_ends) - period_start - 1

        self.rows, self.cols = (
            orig_rows,
            orig_cols,
        )  # reset since we were modifying in place

        return period_start, period

    def many_cycles(self, iters):
        """assumption: iters > period"""

        period_start, period = self.find_period()
        period_iters = (iters - period_start) % period

        for i in range(period_start + period_iters):
            self.cycle()

    def compute_load(self):
        return sum(
            len([x for x in row if x == "O"]) * (self.h - i)
            for i, row in enumerate(self.rows)
        )


if __name__ == "__main__":
    with open("input.txt") as f:
        rows = [line.strip() for line in f.readlines()]
        rf = RockField(rows)
        rf2 = RockField(rows)

    rf.tilt(dir="north")
    print(f"P1 Soln is: {rf.compute_load()}")

    rf2.many_cycles(iters=1000000000)
    print(f"P2 Soln is: {rf2.compute_load()}")
