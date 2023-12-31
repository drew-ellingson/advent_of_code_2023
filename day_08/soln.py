from dataclasses import dataclass
from typing import List, Dict, Tuple
import re
import math


@dataclass
class Node:
    left: str
    right: str


@dataclass
class Graph:
    nodes: Dict[str, Node]
    instrs: List[str]

    def get_steps(self, start_node: str = "AAA", p2: bool = False) -> int:
        curr_node = start_node
        curr_steps = 0

        while not curr_node == "ZZZ" if not p2 else not curr_node.endswith("Z"):
            curr_instr = self.instrs[curr_steps % len(self.instrs)]
            if curr_instr == "L":
                curr_node = self.nodes[curr_node].left
            else:
                curr_node = self.nodes[curr_node].right
            curr_steps += 1

        return curr_steps

    def all_get_steps(self) -> int:
        """
        assuming periodicity immmediately with no starting lag. not sure this is generally true
        but the approach works for this problem.
        """
        start_nodes = {k: v for k, v in self.nodes.items() if k.endswith("A")}
        steps = {k: self.get_steps(start_node=k, p2=True) for k in start_nodes}
        return math.lcm(*steps.values())


def parse_node(node: Node) -> Tuple[str, Node]:
    label, children = node.split(" = ")
    children = re.sub(r"\(|\)", "", children)
    left, right = children.split(", ")
    return label, Node(left, right)


if __name__ == "__main__":
    with open("input.txt") as f:
        instrs, nodes = f.read().split("\n\n")

        instrs = [x for x in instrs]
        nodes = {parse_node(x)[0]: parse_node(x)[1] for x in nodes.split("\n")}

    graph = Graph(nodes, instrs)

    print(f"P1 Soln is: {graph.get_steps()}")
    print(f"P2 Soln is: {graph.all_get_steps()}")
