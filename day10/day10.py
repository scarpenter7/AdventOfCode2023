import numpy as np
from matplotlib import pyplot as plt

with open("day10-input.txt") as file:
    pipe_map = file.readlines()
    pipe_map_np = np.zeros((len(pipe_map), len(pipe_map))).astype(str)
    for i, row in enumerate(pipe_map):
        pipe_map_np[i, :] = np.array(list(row[:-1]))
    map_mask = np.zeros((len(pipe_map), len(pipe_map)))

def find_start():
    for row, line in enumerate(pipe_map):
        try:
            curr_col = line.index('S')
            curr_row = row
            break
        except Exception as e:
            continue
    map_mask[curr_row, curr_col] = 1
    return curr_row, curr_col

def get_loop_len(start_row, start_col):
    curr_row, curr_col = start_row, start_col
    up = pipe_map[start_row - 1][start_col]
    down = pipe_map[start_row + 1][start_col]
    right = pipe_map[start_row][start_col + 1]
    left = pipe_map[start_row][start_col - 1]
    if up in ['F', '|', '7']:
        curr_row -= 1
    elif down in ['L', '|', 'J']:
        curr_row += 1
    elif right in ['J', '-', '7']:
        curr_col += 1
    elif left in ['F', '-', 'L']:
        curr_col -= 1
    curr_pipe = pipe_map[curr_row][curr_col]
    prev_row, prev_col = start_row, start_col
    map_mask[curr_row, curr_col] = 1
    length = 1
    while curr_pipe != 'S':
        if curr_pipe == 'F':
            if curr_row - prev_row == -1:  # go right
                prev_row, prev_col = curr_row, curr_col
                curr_col += 1
            else: # go down
                prev_row, prev_col = curr_row, curr_col
                curr_row += 1
        elif curr_pipe == '|':
            if curr_row - prev_row == -1:  # go up
                prev_row, prev_col = curr_row, curr_col
                curr_row -= 1
            else:
                # go down
                prev_row, prev_col = curr_row, curr_col
                curr_row += 1
        elif curr_pipe == '7':
            if curr_row - prev_row == -1:  # go left
                prev_row, prev_col = curr_row, curr_col
                curr_col -= 1
            else:  # go down
                prev_row, prev_col = curr_row, curr_col
                curr_row += 1
        elif curr_pipe == '-':
            if curr_col - prev_col == 1:  # go right
                prev_row, prev_col = curr_row, curr_col
                curr_col += 1
            else:  # go left
                prev_row, prev_col = curr_row, curr_col
                curr_col -= 1
        elif curr_pipe == 'J':
            if curr_col - prev_col == 1:  # go up
                prev_row, prev_col = curr_row, curr_col
                curr_row -= 1
            else: # go left
                prev_row, prev_col = curr_row, curr_col
                curr_col -= 1
        elif curr_pipe == 'L':
            if curr_row - prev_row == 1:  # go right
                prev_row, prev_col = curr_row, curr_col
                curr_col += 1
            else: # go up
                prev_row, prev_col = curr_row, curr_col
                curr_row -= 1
        curr_pipe = pipe_map[curr_row][curr_col]
        length += 1
        map_mask[curr_row, curr_col] = 1

    return length

def part1():
    curr_row, curr_col = find_start()
    loop_len = get_loop_len(curr_row, curr_col)
    plt.imshow(map_mask)
    plt.show()

    if loop_len % 2 == 1:
        return loop_len // 2 + 1
    return loop_len // 2

def part2():
    no_garbage_pipes_map = np.zeros_like(pipe_map_np)
    no_garbage_pipes_map[map_mask == 1] = pipe_map_np[map_mask == 1]
    res = 0
    inside = False
    curr_edge = None
    for i, row in enumerate(no_garbage_pipes_map):
        for j, curr_element in enumerate(row):
            if curr_element == 'S':
                up = no_garbage_pipes_map[i - 1, j]
                down =  no_garbage_pipes_map[i + 1, j]
                right =  no_garbage_pipes_map[i, j + 1]
                left =  no_garbage_pipes_map[i, j - 1]
                if up in ['F', '|', '7']:
                    up = True
                if down in ['L', '|', 'J']:
                    down = True
                elif right in ['J', '-', '7']:
                    right = True
                elif left in ['F', '-', 'L']:
                    left = True
                if up and down:
                    element = '|'
                elif up and right:
                    element = 'L'
                elif up and left:
                    element = 'J'
                elif left and right:
                    element = '-'
                elif down and right:
                    element = 'F'
                elif down and left:
                    element = '7'
            else:
                element = curr_element
            if element == '':
                if inside: res += 1
            elif element == '|':
                inside = not inside
            elif element in ['F', 'L']:
                curr_edge = element
            elif element == 'J':
                if curr_edge == 'F':
                    inside = not inside
                    curr_edge = None
            elif element == '7':
                if curr_edge == 'L':
                    inside = not inside
                    curr_edge = None
    return res

if __name__ == "__main__":
    print(part1())
    print(part2())