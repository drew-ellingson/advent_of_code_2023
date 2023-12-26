from dataclasses import dataclass, field
from typing import List, Dict
from collections import defaultdict, UserList
from copy import deepcopy

@dataclass 
class Pulse:
    src: str 
    tgt: str 
    type: str 

@dataclass
class Module:
    label: str
    tgts: List[str]

    def emit(self, pulse):
        pass

@dataclass
class FlipFlopModule(Module):
    is_on: bool = field(default=False)

    def emit(self, pulse):
        if pulse.type == 'lo':
            self.is_on = not self.is_on
            return [Pulse(self.label, tgt, 'hi' if self.is_on else 'lo') for tgt in self.tgts]
        return []
@dataclass 
class ConjunctionModule(Module):
    input_modules: List[str] = field(init=False)
    most_recent_pulse_types: Dict[str, str] = field(init=False)

    def get_input_modules(self, module_list):
        return [m.src for m in module_list if self.label in m.tgts] 

    def emit(self, pulse):
        self.most_recent_pulse_types[pulse.src] = pulse.type

        if all(x == 'hi' for x in self.most_recent_pulse_types.values()):
            return [Pulse(self.label, tgt, 'lo') for tgt in self.tgts]
        else:
            return [Pulse(self.label, tgt, 'hi') for tgt in self.tgts]

@dataclass 
class BroadcastModule(Module):
    def emit(self, pulse):
        return [Pulse(self.label, tgt, pulse.type) for tgt in self.tgts]

@dataclass 
class ButtonModule(Module):
    label: str = field(default='button')
    tgts: str = field(default_factory=lambda: ['broadcaster'])

    def emit(self, pulse=None):
        return [Pulse(self.label, self.tgts[0], 'lo')]

@dataclass
class ModuleList(UserList):
    data: List[Module]
    high_pulse_count:int = 0
    low_pulse_count:int = 0

    rx_pulses: Dict[str, int] = field(default_factory=lambda: {'lo': 0, 'hi': 0})


    def __post_init__(self):
        self.data.insert(0, ButtonModule())
        self.get_conjunction_data()

    def get_conjunction_data(self):
        for m in self.data:
            if not isinstance(m, ConjunctionModule):
                pass 
            else:
                m.input_modules = [m2.label for m2 in self.data if m.label in m2.tgts]
                m.most_recent_pulse_types = {k: 'lo' for k in m.input_modules}

    def get_module(self, label):
        return [m for m in self.data if m.label == label][0]
        

    def push_button(self):
        self.rx_pulses = {'lo': 0, 'hi': 0}
        pulses = self.get_module('button').emit()

        while pulses:
            next_pulses = []
            for p in pulses:
                if p.type == 'hi':
                    self.high_pulse_count += 1
                elif p.type == 'lo':
                    self.low_pulse_count += 1
                else:
                    raise ValueError()


                if p.tgt == 'rx':
                    self.rx_pulses[p.type] += 1

                try:
                    m = self.get_module(p.tgt)
                except IndexError: # target module not in list
                    continue 

                next_pulses.extend(m.emit(p))
            pulses = next_pulses

    def many_push_button(self, pushes):
        for _ in range(pushes):
            self.push_button()

    def get_rx_activation(self):
        pushes = 0
        while self.rx_pulses['lo'] != 1:
            self.push_button()
            pushes += 1

            if pushes % 10000 == 1:
                print(pushes)
        return pushes

def parse_line(line):
    splits = line.split(' -> ')
    label, targets = splits[0], splits[1].split(', ')
    if label[0] == '%':
        return FlipFlopModule(label[1:], targets)
    elif label[0] == '&':
        return ConjunctionModule(label[1:], targets)
    elif label[0] == 'b':
        return BroadcastModule('broadcaster', targets) 
    else:
        pass 

if __name__=="__main__":
    with open('input.txt') as f:
        modules = ModuleList([parse_line(line.strip()) for line in f.readlines()])
        p2_modules = deepcopy(modules)

modules.many_push_button(1000)

print(f'P1 Soln is: {modules.high_pulse_count * modules.low_pulse_count}')
print(f'P2 Soln is: {p2_modules.get_rx_activation()}')
