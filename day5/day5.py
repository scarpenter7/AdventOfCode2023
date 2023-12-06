import numpy as np
import time
import multiprocessing as mp

def part1(filename):
    res = None
    with open(filename) as file:
        lines = file.readlines()
        seeds = [int(seed) for seed in lines[0].split()[1:]]

        # build the maps
        maps_list = []
        curr_set = []
        for line in lines[3:]:
            if ':' in line:
                mymap = buildMap(curr_set)
                maps_list.append(mymap)
                curr_set = []
            elif line == '\n':
                continue
            else:
                curr_set.append([int(i) for i in line.split()])
        mymap = buildMap(curr_set)
        maps_list.append(mymap)
        # convert each seed
        for seed in seeds:
            location = convertSeed(seed, maps_list)
            if res is None or location < res:
                res = location
    return res

def part2(filename):
    res = None
    with open(filename) as file:
        lines = file.readlines()
        seeds = [int(seed) for seed in lines[0].split()[1:]]
        seeds_reshaped = np.reshape(seeds, (int(len(seeds)/2), 2))
        print(np.sum(seeds_reshaped[:, 1]))

        # build the maps
        maps_list = []
        curr_set = []
        for line in lines[3:]:
            if ':' in line:
                mymap = buildMap(curr_set)
                maps_list.append(mymap)
                curr_set = []
            elif line == '\n':
                continue
            else:
                curr_set.append([int(i) for i in line.split()])
        mymap = buildMap(curr_set)
        maps_list.append(mymap)

        for seed_range in seeds_reshaped:
            idx = 0
            start = time.time()
            first = True

            for seed in range(seed_range[0], seed_range[0] + seed_range[1]):
                # convert each seed
                location = convertSeed(seed, maps_list)
                idx += 1
                if idx >= 100000 and first:
                    end = time.time()
                    print(end - start)
                    first = False
                if res is None or location < res:
                    res = location
            print("done")
    return res

def buildMap(curr_set):
    def map(num):

        for line in curr_set:
            destination_start = line[0]
            source_start = line[1]
            difference = destination_start - source_start
            range_len = line[2]
            if num in range(source_start, source_start + range_len):
                return destination_start + num - source_start
        return num
    return lambda x : map(x)

def convertSeed(seed, maps_list):
    res = seed
    for map in maps_list:
        res = map(res)
    return res

if __name__ == "__main__":
    #print(part1("day5-input.txt"))
    print(part2("day5-input.txt"))
