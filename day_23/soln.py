from collections import defaultdict
import sys 
from copy import copy 
from os import getpid

def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))

class Grid:
    def __init__(self, raw_grid, p2=False):
        # dont use raw_grid once you call other methods. it doesn't update
        self.raw_grid = raw_grid 
        self.p2 = p2
        
        self.grid = self.build_grid()
        self.graph = self.build_graph()

    def __repr__(self):
        msg = ''
        for row in self.grid:
            msg = msg + ''.join(row) + '\n'
        return msg 

    def build_grid(self):
        if not self.p2:
            return [[x for x in row.strip()] for row in self.raw_grid.split('\n')]
        else:
            return [['.' if x in ['v','<','>','^'] else x for x in row.strip()] for row in self.raw_grid.split('\n')]

    def build_graph(self):
        def get_adjs(x):
            dirs = {'v':(1,0), '>':(0,1),'^':(-1,0),'<':(0,-1)}
            adjs = []
            for sym, dir in dirs.items():
                try:
                    new = _add(x, dir)
                    if self.grid[x[0]][x[1]] == sym and not self.p2:
                        adjs.append(new)
                        break
                    elif self.grid[new[0]][new[1]] != '#':
                        adjs.append(new)
                except IndexError:
                    continue
            return adjs

        graph = defaultdict(list)
        for i,row in enumerate(self.grid):
            for j in range(len(row)):
                if self.grid[i][j] == '#':
                    continue 
                else:
                    graph[(i,j)].extend(get_adjs((i,j)))

        return graph

    def dfs(self, vert, seen=[], path=[]):
        if not path: path = [vert]

        seen.append(vert)

        paths = []
        for i, adj in enumerate(self.graph[vert]):
            if adj not in seen:
                adj_path = path + [adj]
                paths.append(tuple(adj_path))

                # running into oom errors. some kludges below to work on it.
                # to see memory after completion: max_rss in `/usr/bin/time --verbose python soln.py`
                # to see memory while running: RSS_anon in `cat /proc/PID/status` 
                
                # cleanup non-maximal length paths as we go once we finish a branch
                if i == len(self.graph[vert]):
                    paths.remove(path)
                
                # the recursive dfs call
                seen_copy = copy(seen)
                paths.extend(self.dfs(adj, seen_copy, adj_path))

                #discard 'obviously wrong' paths. this will introduce errors if we choose the thresh too low
                thresh = 100
                max_len = max(len(p) for p in paths)
                paths = [x for x in paths if len(x) >= max_len - thresh]
                
                # clean up some space when we finish a branch i guess
                del seen_copy
                del adj_path
        
        return paths 

    def get_max_path(self):
        paths = self.dfs((0,1))
        end_node = (len(self.grid) - 1, len(self.grid[0]) - 2)

        max_path = max([x for x in paths if x[-1] == end_node], key = lambda x: len(x))

        # grid visual update for light debugging
        self.grid = [[x if (i,j) not in max_path else 'O' for j,x in enumerate(row)] for i,row in enumerate(self.grid)]
        return max_path

if __name__=="__main__":
    sys.setrecursionlimit(100000) # default 1k fails on full input

    with open('input.txt') as f:
        contents = f.read()
        grid = Grid(contents)
        p2_grid = Grid(contents, p2 = True)

    print(f'Current PID: {getpid()}')
    print(f'P1 Soln is: {len(grid.get_max_path()) - 1}')
    print(f'P2 Soln is: {len(p2_grid.get_max_path()) - 1}')
