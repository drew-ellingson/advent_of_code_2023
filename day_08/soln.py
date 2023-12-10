from dataclasses import dataclass, field
from typing import List, Dict
import re 

@dataclass 
class Node:
    left: str 
    right: str 

@dataclass
class Graph:
    nodes: Dict[str, Node]
    instrs: List[str]

    def get_steps(self, start_nodes = ['AAA'], end_nodes = ['ZZZ']) -> int:
        curr_nodes = start_nodes
        curr_steps = 0
        while not all(a in end_nodes for a in curr_nodes):
            curr_instr = self.instrs[curr_steps % len(self.instrs)]
            if curr_instr == 'L':
                curr_nodes = [self.nodes[a].left for a in curr_nodes]
            else:
                curr_nodes = [self.nodes[a].right for a in curr_nodes]
            curr_steps += 1
            if curr_steps % 100000 == 1:
                print(f'At step: {curr_steps}')
        return curr_steps
     
def parse_node(node):
    label, children = node.split(' = ')
    children = re.sub(r'\(|\)', '', children)
    left, right = children.split(', ')
    return label, Node(left, right)

if __name__=="__main__":
    with open('input.txt') as f:
        instrs, nodes = f.read().split('\n\n')
        
        instrs = [x for x in instrs]
        nodes = {parse_node(x)[0]: parse_node(x)[1] for x in nodes.split('\n')}

    graph = Graph(nodes, instrs)

    start_nodes = {k:v for k,v in nodes.items() if k.endswith('A')}
    end_nodes = {k:v for k,v in nodes.items() if k.endswith('Z')}

    print(f'P2 Soln is: {graph.get_steps(start_nodes=start_nodes, end_nodes = end_nodes)}')