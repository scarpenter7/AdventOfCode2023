import numpy as np

def gather_galaxy_indices(space_map):
    indices = []
    for i, row in enumerate(space_map):
        for j, element in enumerate(row):
            if element == '#':
                indices.append((i, j))
    return indices

def part1():
    with open("day11-input.txt") as file:
        input = file.readlines()
        space_map = np.array(list(input[0][:-1]))
        empty_space = '.' * len(input[0][:-1])
        first = True
        for line in input:
            if first:
                first = False
                continue
            if line[:-1] == empty_space:
                space_map = np.vstack((space_map, np.array(list(empty_space)), np.array(list(empty_space))))
            else:
                space_map = np.vstack((space_map, np.array(list(line[:-1]))))

        empty_col = np.array(list('.' * space_map.shape[0]))
        space_map_transposed = space_map.copy().T
        curr_index = 0
        for col in space_map_transposed:
            if all(col == empty_col):
                space_map = np.insert(space_map, curr_index, '.', axis=1)
                curr_index += 1
            curr_index += 1
    res = 0
    indices = gather_galaxy_indices(space_map)
    for i, ind_start in enumerate(indices[:-1]):
        for ind_dest in indices[i+1:]:
            distance = abs(ind_start[0] - ind_dest[0]) + abs(ind_start[1] - ind_dest[1])
            res += distance
    return res

def get_empty_indices(space_map):
    empty_row = np.array(list('.' * space_map.shape[1]))
    res = []
    for i, row in enumerate(space_map):
        if all(row == empty_row):
            res.append(i)
    return res

def part2():
    with open("day11-input.txt") as file:
        input = file.readlines()
        space_map = np.array(list(input[0][:-1]))

        first = True
        for line in input:
            if first:
                first = False
                continue
            space_map = np.vstack((space_map, np.array(list(line[:-1]))))

        row_indices = get_empty_indices(space_map)
        col_indices = get_empty_indices(space_map.T)

        res = 0
        galaxies = gather_galaxy_indices(space_map)
        for i, ind_start in enumerate(galaxies[:-1]):
            for ind_dest in galaxies[i + 1:]:
                distance = abs(ind_start[0] - ind_dest[0]) + abs(ind_start[1] - ind_dest[1])
                distance += 999999 * (len([i for i in row_indices if i in range(min(ind_start[0], ind_dest[0]), max(ind_start[0], ind_dest[0]))]) +
                                      len([i for i in col_indices if i in range(min(ind_start[1], ind_dest[1]), max(ind_start[1], ind_dest[1]))]))
                res += distance

    return res

if __name__ == "__main__":
    print(part1())
    print(part2())