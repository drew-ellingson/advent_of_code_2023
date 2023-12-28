from __future__ import annotations

from collections import UserList
from dataclasses import dataclass 
from typing import List  
from itertools import combinations

import numpy as np
from gekko import GEKKO

@dataclass 
class Line:
    point: np.ArrayLike
    slope: np.ArrayLike

    def intersect_xy(self, other: Line):
        A = np.column_stack([self.slope, -1 * other.slope])[:2,:2] # build matrix, omit z
        b = np.array(other.point -1 * self.point)[:2]

        s, t = np.linalg.solve(A,b)
        x, y = (np.array(self.point) + s * np.array(self.slope))[:2] # substitute

        return s, t, x, y

@dataclass 
class LineCollection(UserList):
    data: List[Line]

    def count_intersections(self, min_val, max_val):
        pairs = combinations(self.data, 2)
        
        count = 0
        for l1, l2 in pairs:
            try:
                s,t,x,y = l1.intersect_xy(l2)
                if min_val <= x <= max_val and min_val <= y <= max_val and s >= 0 and t >= 0:
                    count += 1
            except np.linalg.LinAlgError: # parallel lines
                continue
        return count 

    def get_start_pos(self):
        m = GEKKO()
        vars = [m.Var(i) for i in range(9)]
        x = vars[:3]
        v = vars[3:6]
        t = vars[6:]

        lines = self.data[:3]

        equations = []
        
        for i in range(3):
            for j in range(3):
                equations.append(x[j] + t[i]*v[j] == lines[i].point[j] - lines[i].slope[j] * t[i])

        m.Equations(equations)
        for e in equations:
            print(e)
        m.solve(disp=False)

        return int(sum(x.value[0] for x in vars[:3]))


def parse_line(line):
    point, slope = line.split(' @ ')
    point = np.array([int(x) for x in point.split(', ')])
    slope = np.array([int(x) for x in slope.split(', ')])
    return point, slope 

if __name__=="__main__":
    input_file = 'input2.txt'
    min_val, max_val = 200000000000000, 400000000000000
      
    with open(input_file) as f:
        lines = LineCollection([Line(*parse_line(line)) for line in f.readlines()])
        
        xy_ints = lines.count_intersections(min_val, max_val)
        
        print(f'P1 Soln is: {xy_ints}')
        print(f'P2 Soln is: {lines.get_start_pos()}')

