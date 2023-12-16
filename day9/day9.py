def check_same(lst):
    return lst[1:] == lst[:-1]


def process_line(line, future=True):
    nums = [int(num) for num in line.split()]
    return find_diff(nums, future)


def find_diff(nums, future):
    if check_same(nums):
        return nums[0]
    diffs = diff_adjacent_elements_3(nums)
    if future:
        return nums[-1] + find_diff(diffs, future)
    return nums[0] - find_diff(diffs, future)


def diff_adjacent_elements_3(lst):
    return list(map(lambda x, y: y - x, lst[:-1], lst[1:]))


def part1(filename):
    with open(filename) as file:
        lines = file.readlines()
    return sum(process_line(line) for line in lines)

def part2(filename):
    with open(filename) as file:
        lines = file.readlines()
    return sum(process_line(line, False) for line in lines)

if __name__ == "__main__":
    print(part1("day9-input.txt"))
    print(part2("day9-input.txt"))
