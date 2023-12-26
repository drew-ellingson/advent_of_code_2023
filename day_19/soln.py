from __future__ import annotations

from dataclasses import dataclass, field 
from typing import List, Tuple, Dict
from collections import defaultdict

from itertools import product 
from functools import cmp_to_key


@dataclass
class Rule:
    rating: str 
    op: str 
    comp: int 
    tgt_label: str 

    def rule_pass(self, part):
        if not self.rating:
            return True 
        elif self.op == '>':
            return part.ratings[self.rating] > self.comp
        elif self.op == '<':
            return part.ratings[self.rating] < self.comp 

@dataclass 
class Workflow:
    label: str
    rules: List[Rule]

@dataclass
class Part:
    ratings: Dict[str, int] = field(default_factory=lambda: {})

    def is_accepted(self, workflows):
        wf = [x for x in workflows if x.label == 'in'][0]
        wf_hist = [wf]
        while True:
            for rule in wf.rules:
                rule_pass = rule.rule_pass(self)

                if not rule_pass:
                    continue 
                elif rule.tgt_label in ['A', 'R']:
                    return rule.tgt_label == 'A'
                else:
                    wf = [x for x in workflows if x.label == rule.tgt_label][0]
                    wf_hist.append(wf)
                    break


def parse_rule(raw_rule):
    if '<' not in raw_rule and '>' not in raw_rule:
        return Rule(rating=None, op=None, comp=None, tgt_label= raw_rule)
    else:
        rule, tgt = raw_rule.split(':')
        rating = rule[0]
        op = rule[1]
        comp = int(rule[2:])
        return Rule(rating=rating, op=op, comp=comp, tgt_label=tgt)

def parse_workflow(raw_wf):
    label = raw_wf[:raw_wf.index('{')]
    rules = raw_wf[raw_wf.index('{') + 1: -1]
    rules = [parse_rule(rule) for rule in rules.split(',')]
    return Workflow(label, rules)

def parse_part(raw_part):
    part = raw_part[1:-1]
    ratings = part.split(',')
    return Part({r[0]: int(r[r.index('=') + 1:]) for r in ratings})

def get_thresholds(workflows):
    thresholds = defaultdict(lambda: [1])
    for wf in workflows:
        for r in wf.rules:
            if r.rating:
                thresholds[r.rating].append(r.comp if r.op == '<' else r.comp + 1)
    thresholds = {k: sorted(v) for k,v in thresholds.items()}
    return thresholds

def get_test_parts(thresholds):
    keys = 'xmas'
    points = product(*[thresholds[k] for k in keys])
    parts = [Part({keys[i]: pt[i] for i in range(len(keys))}) for pt in points]
    return parts

def compute_test_parts(test_parts, workflows):
    output = []
    for part in test_parts:
        next_x = min([p.ratings['x'] for p in test_parts if p.ratings['x'] > part.ratings['x']].append(4000))
        next_m = min([p.ratings['m'] for p in test_parts if p.ratings['m'] > part.ratings['m']].append(4000))
        next_a = min([p.ratings['a'] for p in test_parts if p.ratings['a'] > part.ratings['a']].append(4000))
        next_s = min([p.ratings['s'] for p in test_parts if p.ratings['s'] > part.ratings['s']].append(4000))
        
        box_vol = (next_x - part.ratings['x'] + 1) * (next_m - part.ratings['m'] + 1) * (next_a - part.ratings['a'] + 1) * (next_s - part.ratings['s'] + 1)

        output.append(part, part.is_accepted(workflows), box_vol)
    return output


if __name__=="__main__":
    with open('input2.txt') as f:
        workflows, parts = f.read().split('\n\n') 

    workflows = [parse_workflow(wf.strip()) for wf in workflows.split('\n')]
    parts = [parse_part(p.strip()) for p in parts.split('\n')]


    accepted = [p for p in parts if p.is_accepted(workflows)]

    print(f'P1 Soln is: {(sum(sum(a.ratings.values()) for a in accepted))}')

    thresholds = get_thresholds(workflows)

    test_parts = get_test_parts(thresholds)

    ctp = compute_test_parts(test_parts, workflows)

    for p in ctp:
        print(p)