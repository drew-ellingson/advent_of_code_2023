from dataclasses import dataclass, field  
from typing import Tuple, List 

@dataclass 
class Node:
    pos: Tuple[int]
    cost: int
    
    # populated in graph constructor or djikstra's
    label: int = field(default = None) # 
    prev_node: int = field(default = 0)
    sum_cost: int = field(default =  None)

class Graph:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self.h = max(n.pos[0] for n in self.nodes) + 1
        self.w = max(n.pos[1] for n in self.nodes) + 1

        # assign each node an int index so we can traverse quickly.
        for n in self.nodes:
            n.label = n.pos[0] * self.w + n.pos[1]
            n.sum_cost = 10 * self.h * self.w # safe upper bound
    
    def __repr__(self):
        msg = ''
        for i in range(self.h):
            node_list = sorted([n for n in self.nodes if n.pos[0] == i], key = lambda x: x.label)
            msg = msg + ' , '.join([str(x.sum_cost) + '|' + str(x.cost) for x in node_list]) + '\n'
        return msg 

    def get_min_node(self, unvisited):
        return min([n for n in self.nodes if n.label in unvisited], key = lambda x: x.sum_cost)

    def get_neighbors(self, node_label):
        up = node_label - self.w
        down = node_label + self.w
        left = node_label - 1 
        right = node_label + 1 

        if node_label % self.w == self.w - 1:
            cands = [up, left, down]
        elif node_label % self.w == 0:
            cands = [up, right, down]
        else:
            cands = [up, right, down, left]
        
        last_1 = self.nodes[node_label].prev_node
        last_2 = self.nodes[last_1].prev_node
        last_3 = self.nodes[last_2].prev_node
    
        cands = [x for x in cands if 0 <= x < len(self.nodes)]

        if len(set([last_1, last_2, last_3])) != 3:
            pass

        elif len(set([self.nodes[l].pos[0] for l in [last_1, last_2, last_3]])) == 1:
            cands = [x for x in cands if self.nodes[x].pos[0] != self.nodes[last_1].pos[0]]
        
        elif len(set([self.nodes[l].pos[1] for l in [last_1, last_2, last_3]])) == 1:
            cands = [x for x in cands if self.nodes[x].pos[1] != self.nodes[last_1].pos[1]]



        return [x for x in cands if 0 <= x < len(self.nodes)]

    def find_min_paths(self, start_label):

        visited = []
        unvisited = list(range(len(self.nodes)))

        self.nodes[start_label].sum_cost = 0
        while unvisited:
            curr = self.get_min_node(unvisited)
            neighbors = self.get_neighbors(curr.label)
            for n in neighbors:
                path_cost = curr.sum_cost + self.nodes[n].cost
                
                if path_cost < self.nodes[n].sum_cost:
                    self.nodes[n].sum_cost = min(path_cost, self.nodes[n].sum_cost)
                    self.nodes[n].prev_node = curr.label
            unvisited.remove(curr.label)
            visited.append(curr.label)
            # print(curr.label)
            # print(unvisited)
            # print(visited)
            # input()
        
        

if __name__=="__main__":
    with open('input2.txt') as f:
        lines = [x.strip() for x in f.readlines()]
        nodes = [Node(pos=(i, j), cost=int(ele)) for i, row in enumerate(lines) for j, ele in enumerate(row) ]
        graph = Graph(nodes)
 
    graph.find_min_paths(0)
    print(graph)

print(4 + 1 + 1)



