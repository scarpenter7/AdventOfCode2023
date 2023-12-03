

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

    if top: # verified
        top_symbols = grid[row_idx - 1][col_idx:(col_idx + len(num))]
        if not all(map(check_for_symbols, top_symbols)):
            return int(num)
    if bottom: # verified
        bottom_symbols = grid[row_idx + 1][col_idx:(col_idx + len(num))]
        if not all(map(check_for_symbols, bottom_symbols)):
            return int(num)
    if top_left: # verified
        if grid[row_idx - 1][col_idx - 1] != '.':
            return int(num)
    if top_right: # verified
        if grid[row_idx - 1][col_idx + len(num)] != '.':
            return int(num)
    if bottom_left: # verified
        if grid[row_idx + 1][col_idx - 1] != '.':
            return int(num)
    if bottom_right: # verified
        if grid[row_idx + 1][col_idx + len(num)] != '.':
            return int(num)
    if left: # verified
        if grid[row_idx][col_idx - 1] != '.':
            return int(num)
    if right: # verified
        if grid[row_idx][col_idx + len(num)] != '.':
            return int(num)
    # verified
    return 0  # this number is not adjacent to a symbol that isn't a '.'


if __name__ == "__main__":
    print(part1("day3-input.txt"))