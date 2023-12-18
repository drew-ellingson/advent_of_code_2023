from dataclasses import dataclass, field
from typing import List, Tuple 

# vector addition
def _add(a1: Tuple[int], a2: Tuple[int]) -> Tuple[int]:
    return tuple(map(sum, zip(a1, a2)))


@dataclass 
class Point:
    val: str 
    energy_count: int = field(default=0)

@dataclass
class Beam:
    pos: Tuple[int]
    dir: Tuple[int]

class Grid:
    def __init__(self, grid: List[List[Point]]):
        self.grid = grid 
        self.beams: List[Beam] = [Beam((0, 0), (0, 1))]

        self.h: int = len(self.grid)
        self.w: int = len(self.grid[0])

        self.beam_hist = self.beams 

    def __repr__(self) -> str:
        msg = ''
        for row in self.grid:
            msg = msg + ''.join(['#' if x.energy_count > 0 else x.val for x in row]) + '\n'

        return msg 
    
    def get_point(self, pos):
        return self.grid[pos[0]][pos[1]]

    def out_of_bounds(self, pos: Tuple[int]) -> bool:
        return (pos[0] < 0 or pos[0] >= self.h or pos[1] < 0 or pos[1] >= self.w)

    def beams_move(self) -> List[Beam]:
        new_beams = []
        for beam in self.beams:

            # edge case: first beam splits was causing subsequent to split
            # even if it shouldnt
            try:
                del new_dir_2 
            except UnboundLocalError:
                pass 

            point = self.get_point(beam.pos)
            point.energy_count += 1

            new_dir = beam.dir 

            if point.val == '|' and beam.dir in [(0, 1), (0, -1)]:
                new_dir = (1, 0) # send existing beam in pos dir
                new_dir_2 = (-1, 0) # create new beam in neg dir
            elif point.val == '-' and beam.dir in [(1, 0), (-1, 0)]:
                new_dir = (0, 1)
                new_dir_2 = (0, -1)
            elif point.val == '/':
                # (1, 0) -> (0, -1), (-1, 0) -> (0, 1), etc.
                new_dir = (-1 * beam.dir[1], -1 * beam.dir[0]) 
            elif point.val == '\\':
                # (1, 0) -> (0, 1), (0, 1) -> (1, 0), etc
                new_dir = (beam.dir[1], beam.dir[0])
            
            new_pos = _add(beam.pos, new_dir)
        
            if self.out_of_bounds(new_pos):
                continue
            
            new_beam = Beam(new_pos, new_dir)
            if new_beam not in self.beam_hist:
                new_beams.append(Beam(new_pos, new_dir))  

            try:
                new_pos_2 = _add(beam.pos, new_dir_2)
                if self.out_of_bounds(new_pos_2):
                    continue
                new_beam_2 = Beam(new_pos_2, new_dir_2)
                if new_beam_2 not in self.beam_hist:
                    new_beams.append(Beam(new_pos_2, new_dir_2))
            except UnboundLocalError:
                pass

        self.beams = new_beams
        self.beam_hist.extend(new_beams)

    def beams_move_until_done(self):
        old_beam_hist_len = len(self.beam_hist) 
        new_beam_hist_len = 0

        # items are never removed so this is valid
        while old_beam_hist_len != new_beam_hist_len:
            old_beam_hist_len = len(self.beam_hist)
            self.beams_move()
            new_beam_hist_len = len(self.beam_hist)


    def count_energized_tiles(self):
        return len([x for row in self.grid for x in row if x.energy_count >= 1])


if __name__=="__main__":
    with open('input.txt') as f:
        grid = [[Point(x) for x in line.strip()] for line in f.readlines()]
    grid = Grid(grid)

    grid.beams_move_until_done()
    print(f'P1 Soln is: {grid.count_energized_tiles()}')

    # P2 Thought:
    # Rework so that beams track point history and then memoize