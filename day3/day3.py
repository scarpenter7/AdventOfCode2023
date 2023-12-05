

def part1(filename):
    res = 0
    grid = []
    with open(filename) as file:
        for line in file.readlines():
            grid.append(line)

    for row_idx, row in enumerate(grid):
        curr_num = ""
        for col_idx, char in enumerate(row):
            if curr_num != "":
                curr_num = curr_num[1:]
                continue # skip until current char isn't a digit already accounted for
            curr_char = char
            while curr_char.isdigit(): # extract the complete number
                curr_num = "".join([curr_num, curr_char])
                curr_char = grid[row_idx][col_idx + len(curr_num)]
            if curr_num != "":
                res += check_if_valid(grid, row_idx, col_idx, curr_num)
    return res

def part2(filename):
    res = 0
    grid = []
    with open(filename) as file:
        for line in file.readlines():
            grid.append('#' + line[:-1] + '#')

    # pad the boundaries with '#'s
    grid.insert(0, '#' * len(grid[0]))
    grid.append('#' * len(grid[0]))

    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if row_idx == 0 or col_idx == 0 or row_idx == (len(grid) - 1) or col_idx == (len(grid[0]) - 1):
                continue # skip padding
            if char == '*':
                product = check_gear(grid, row_idx, col_idx)
                res += product

    return res

def check_if_valid(grid, row_idx, col_idx, num):
    # PROTECT THE BOUNDARIES
    top = True
    bottom = True
    top_left = True
    top_right = True
    bottom_left = True
    bottom_right = True
    left = True
    right = True

    if row_idx == 0: # number in top row
        top = False
        top_left = False
        top_right = False
    if col_idx == 0: # number starts in leftmost column
        left = False
        top_left = False
        bottom_left = False
    if row_idx == len(grid) - 1: # number in bottom row
        bottom = False
        bottom_left = False
        bottom_right = False
    if (col_idx + len(num)) == len(grid[0]) - 1: # number in rightmost column (don't forget \n char at end)
        right = False
        top_right = False
        bottom_right = False

    check_for_symbols = lambda x: x == '.'

    if top:
        top_symbols = grid[row_idx - 1][col_idx:(col_idx + len(num))]
        if not all(map(check_for_symbols, top_symbols)):
            return int(num)
    if bottom:
        bottom_symbols = grid[row_idx + 1][col_idx:(col_idx + len(num))]
        if not all(map(check_for_symbols, bottom_symbols)):
            return int(num)
    if top_left:
        if grid[row_idx - 1][col_idx - 1] != '.':
            return int(num)
    if top_right:
        if grid[row_idx - 1][col_idx + len(num)] != '.':
            return int(num)
    if bottom_left:
        if grid[row_idx + 1][col_idx - 1] != '.':
            return int(num)
    if bottom_right:
        if grid[row_idx + 1][col_idx + len(num)] != '.':
            return int(num)
    if left:
        if grid[row_idx][col_idx - 1] != '.':
            return int(num)
    if right:
        if grid[row_idx][col_idx + len(num)] != '.':
            return int(num)
    return 0  # this number is not adjacent to a symbol that isn't a '.'

def check_gear(grid, row_idx, col_idx):
    nums = []

    top_left = grid[row_idx - 1][col_idx - 1]
    top = grid[row_idx - 1][col_idx]
    top_right = grid[row_idx - 1][col_idx + 1]
    left = grid[row_idx][col_idx - 1]
    right = grid[row_idx][col_idx + 1]
    bottom_left = grid[row_idx + 1][col_idx - 1]
    bottom = grid[row_idx + 1][col_idx]
    bottom_right = grid[row_idx + 1][col_idx + 1]

    tops = scan_row(grid, row_idx - 1, col_idx, top, top_left, top_right)
    bottoms = scan_row(grid, row_idx + 1, col_idx, bottom, bottom_left, bottom_right)

    nums += tops + bottoms

    if left.isdigit():
        curr_num = left
        curr_num = scan_left(grid, row_idx, col_idx - 1, curr_num)
        nums.append(int(curr_num))
    if right.isdigit():
        curr_num = right
        curr_num = scan_right(grid, row_idx, col_idx + 1, curr_num)
        nums.append(int(curr_num))

    if len(nums) == 2:
        return nums[0] * nums[1]
    return 0  # this gear doesn't have 2 numbers adjacent

def scan_row(grid, row_idx, col_idx, middle, left, right):
    nums = []
    if middle.isdigit():
        curr_num = middle
        curr_num = scan_left(grid, row_idx, col_idx, curr_num)
        curr_num = scan_right(grid, row_idx, col_idx, curr_num)
        nums.append(int(curr_num))
    elif left.isdigit() and right.isdigit():
        curr_num = left
        curr_num = scan_left(grid, row_idx, col_idx - 1, curr_num)
        nums.append(int(curr_num))

        curr_num = right
        curr_num = scan_right(grid, row_idx, col_idx + 1, curr_num)
        nums.append(int(curr_num))
    elif left.isdigit():
        curr_num = left
        curr_num = scan_left(grid, row_idx, col_idx - 1, curr_num)
        nums.append(int(curr_num))
    elif right.isdigit():
        curr_num = right
        curr_num = scan_right(grid, row_idx, col_idx + 1, curr_num)
        nums.append(int(curr_num))
    return nums

def scan_left(grid, row_idx, col_idx, curr_num):
    curr_idx = col_idx - 1
    curr_char = grid[row_idx][curr_idx]
    while curr_char.isdigit():
        curr_num = curr_char + curr_num
        curr_idx -= 1
        curr_char = grid[row_idx][curr_idx]
    return curr_num

def scan_right(grid, row_idx, col_idx, curr_num):
    curr_idx = col_idx + 1
    curr_char = grid[row_idx][curr_idx]
    while curr_char.isdigit():
        curr_num += curr_char
        curr_idx += 1
        curr_char = grid[row_idx][curr_idx]
    return curr_num

if __name__ == "__main__":
    print(part1("day3-input.txt"))
    print(part2("day3-input.txt"))