import sys

with open("day10-input.txt") as file:
    pipe_map = file.readlines()

def find_start():
    for row, line in enumerate(pipe_map):
        try:
            curr_col = line.index('S')
            curr_row = row
            break
        except Exception as e:
            continue
    return curr_row, curr_col

def get_loop_len(curr_row, curr_col):
    up = pipe_map[curr_row - 1][curr_col]
    if up in ['F', '|', '7']:
        return traverse_up(curr_row - 1, curr_col, 1)
    down = pipe_map[curr_row + 1][curr_col]
    if down in ['L', '|', 'J']:
        return traverse_down(curr_row + 1, curr_col, 1)
    right = pipe_map[curr_row][curr_col + 1]
    if right in ['J', '-', '7']:
        return traverse_right(curr_row, curr_col + 1, 1)
    left = pipe_map[curr_row][curr_col - 1]
    if left in ['F', '-', 'L']:
        return traverse_left(curr_row, curr_col - 1, 1)
    raise Exception("No valid pipe neighbors next to start position")

def traverse_up(curr_row, curr_col, length):
    curr_pipe = pipe_map[curr_row][curr_col]
    if curr_pipe == 'F':
        return traverse_right(curr_row, curr_col + 1, length + 1)
    if curr_pipe == '|':
        return traverse_up(curr_row - 1, curr_col, length + 1)
    if curr_pipe == '7':
        return traverse_left(curr_row, curr_col - 1, length + 1)
    if curr_pipe == 'S':
        return length + 1

def traverse_down(curr_row, curr_col, length):
    curr_pipe = pipe_map[curr_row][curr_col]
    if curr_pipe == 'L':
        return traverse_right(curr_row, curr_col + 1, length + 1)
    if curr_pipe == '|':
        return traverse_down(curr_row + 1, curr_col, length + 1)
    if curr_pipe == 'J':
        return traverse_left(curr_row, curr_col - 1, length + 1)
    if curr_pipe == 'S':
        return length + 1

def traverse_right(curr_row, curr_col, length):
    curr_pipe = pipe_map[curr_row][curr_col]
    if curr_pipe == '-':
        return traverse_right(curr_row, curr_col + 1, length + 1)
    if curr_pipe == '7':
        return traverse_down(curr_row + 1, curr_col, length + 1)
    if curr_pipe == 'J':
        return traverse_up(curr_row - 1, curr_col, length + 1)
    if curr_pipe == 'S':
        return length + 1

def traverse_left(curr_row, curr_col, length):
    curr_pipe = pipe_map[curr_row][curr_col]
    if curr_pipe == '-':
        return traverse_left(curr_row, curr_col - 1, length + 1)
    if curr_pipe == 'F':
        return traverse_down(curr_row + 1, curr_col, length + 1)
    if curr_pipe == 'L':
        return traverse_up(curr_row - 1, curr_col, length + 1)
    if curr_pipe == 'S':
        return length + 1

def part1():
    curr_row, curr_col = find_start()
    loop_len = get_loop_len(curr_row, curr_col)

    if loop_len % 2 == 1:
        return loop_len // 2 + 1
    return loop_len // 2

"""
def part2(filename):
    with open(filename) as file:
        lines = file.readlines()
    return sum(process_line(line, False) for line in lines)
"""

if __name__ == "__main__":
    sys.setrecursionlimit(3000)
    print(sys.getrecursionlimit())
    print(part1())
    #print(part2("day9-input.txt"))