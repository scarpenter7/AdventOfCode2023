import math

def get_key(line):
    return line.split(' = ')[0]

def lcm(nums):
  res = 1
  for num in nums:
      res = lcm2(res, num)
  return res

def lcm2(a, b):
    return (a * b) // math.gcd(a, b)

def get_value(line):
    val_str = line.split(' = ')[1][1:][:-2]
    left = val_str[:3]
    right = val_str[-3:]
    return left, right

def part1(filename):
    res = 0
    with open(filename) as file:
        lines = file.readlines()
        instructions = lines[0][:-1]
        travel_map_lines = lines[2:]
        travel_dict = {get_key(line): get_value(line) for line in travel_map_lines}

    curr_location = "AAA"
    arrived = False
    while not arrived:
        for dir in instructions:
            if dir == 'L':
                curr_location = travel_dict[curr_location][0]
            elif dir == 'R':
                curr_location = travel_dict[curr_location][1]
        if curr_location == "ZZZ":
            arrived = True
        res += len(instructions)
    return res

def part2(filename):
    # Too slow
    res = 0
    with open(filename) as file:
        lines = file.readlines()
        instructions = lines[0][:-1]
        travel_map_lines = lines[2:]
        travel_dict = {get_key(line): get_value(line) for line in travel_map_lines}
        curr_locations = [l for l in travel_dict.keys() if l[-1] == 'A']
        cycle_lens = explore(curr_locations, instructions, travel_dict)

    return lcm(cycle_lens)


def check_same(list):
   return list[1:] == list[:-1]

def explore(curr_locations, instructions, travel_dict):
    z1s_found_lens = [0] * len(curr_locations)
    z1s_found = [False] * len(curr_locations)

    num_steps = 0
    while True:
        for dir in instructions:
            num_steps += 1
            if dir == 'L':
                curr_locations = [travel_dict[loc][0] for loc in curr_locations]
            elif dir == 'R':
                curr_locations = [travel_dict[loc][1] for loc in curr_locations]
            for i, loc in enumerate(curr_locations):
                if loc[-1] == 'Z':
                    if z1s_found_lens[i] == 0:
                        z1s_found[i] = True
                        z1s_found_lens[i] = num_steps
            if all(z1s_found):
                return z1s_found_lens


if __name__ == "__main__":
    print(part1("day8-input.txt"))
    print(part2("day8-input.txt"))
