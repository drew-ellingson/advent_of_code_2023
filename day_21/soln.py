from dataclasses import dataclass 

def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))


class Garden:
    def __init__(self, grid):
        self.grid = [[x if x != 'S' else 'O' for x in row] for row in grid]

    def __repr__(self):
        msg = ''
        for g in self.grid:
            msg = msg + ''.join(g) + '\n' 
        return msg

    def get_plot(self, coord):
        return self.grid[coord[0]][coord[1]]

    def get_adjs(self, coord):
        dirs = [(1,0), (0,1), (-1, 0), (0, -1)]        
        adjs = []

        for dir in dirs:
            cand = _add(coord, dir)
            try:
                if self.get_plot(cand) in ['.', 'O']:
                    adjs.append(cand)
            except IndexError:
                continue 
        
        return adjs 

    def get_curr_coords(self):
        return [(i,j) for  i in range(len(self.grid)) for j in range(len(self.grid[0])) if self.grid[i][j] == 'O']

    def step(self):
        curr_coords = self.get_curr_coords()

        # reset 
        self.grid = [[x if x != 'O' else '.' for x in row] for row in self.grid]

        new_coords = []
        
        for c in curr_coords:
            new_coords.extend(self.get_adjs(c))
            
        self.grid = [[x if (i,j) not in new_coords else 'O' for j,x in enumerate(row)] for i, row in enumerate(self.grid)]
            
    def many_step(self, steps):
        for i in range(steps):
            self.step()
            print(f'Step {i} completed. with {len(self.get_curr_coords())} possible locations')
        return len(self.get_curr_coords())

if __name__=="__main__":
    with open('input.txt') as f:
        grid = [[x for x in line.strip()] for line in f.readlines()]
        garden = Garden(grid)

        print(f'P1 Soln is: {garden.many_step(64)}')
    
