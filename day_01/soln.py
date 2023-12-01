import re

p1_nums = re.compile(r'\d+?')
p2_nums = re.compile(r'(?=(\d+?|one|two|three|four|five|six|seven|eight|nine))')

NUMBER_NAMES = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

with open('input.txt') as f:
    instrs = [x.strip() for x in f.readlines()]

def get_calibration(instr , pattern):
    nums = pattern.findall(instr)
    nums = [NUMBER_NAMES.get(x) if not x.isdigit() else x for i, x in enumerate(nums)]
    return int(nums[0] + nums[-1]) if nums else 0
    
if __name__ == '__main__': 
    print(f'P1 Soln is: {sum(get_calibration(instr, p1_nums) for instr in instrs)}')
    print(f'P1 Soln is: {sum(get_calibration(instr, p2_nums) for instr in instrs)}')
