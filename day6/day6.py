
def part1(filename):
    res = 1
    with open(filename) as file:
        lines = file.readlines()
        times = [int(l) for l in lines[0].split()[1:]]
        distances = [int(l) for l in lines[1].split()[1:]]
        for time, dist in zip(times, distances):
            options = 0
            for button_hold in range(1, time):
                dist_travelled = button_hold * (time - button_hold)
                if dist_travelled > dist:
                    options += 1
            res *= options
    return res

def part2(filename):
    # O(n) solution
    res = 0
    with open(filename) as file:
        lines = file.readlines()
        times = [int(l) for l in lines[0].split()[1:]]
        distances = [int(l) for l in lines[1].split()[1:]]
        time = int(str(times[0]) + str(times[1]) + str(times[2]) + str(times[3]))
        dist = int(str(distances[0]) + str(distances[1]) + str(distances[2]) + str(distances[3]))
        start_hold_time = time // 2
        start_go_time = start_hold_time
        first = True
        while start_hold_time * start_go_time > dist:
            if first:
                res = 1
                first = False
            else:
                res += 2
            start_hold_time += 1
            start_go_time -= 1
    return res

def part2alt(filename):
    # O(log(n)) using binary search
    with open(filename) as file:
        lines = file.readlines()
        times = [int(l) for l in lines[0].split()[1:]]
        distances = [int(l) for l in lines[1].split()[1:]]

        time = int(str(times[0]) + str(times[1]) + str(times[2]) + str(times[3]))
        dist = int(str(distances[0]) + str(distances[1]) + str(distances[2]) + str(distances[3]))
        upper_boundary = time // 2
        lower_boundary = 0
        current_bisection = (upper_boundary + lower_boundary) // 2
        go_time = time - current_bisection
        breaks_record = current_bisection * go_time > dist
        last_broken = None
        while upper_boundary - lower_boundary > 1:
            if breaks_record: # move left
                if last_broken is None:
                    last_broken = current_bisection
                elif current_bisection < last_broken:
                    last_broken = current_bisection
                upper_boundary = current_bisection
                current_bisection = (upper_boundary + lower_boundary) // 2
            else: # move right
                lower_boundary = current_bisection
                current_bisection = (upper_boundary + lower_boundary) // 2
            go_time = time - current_bisection
            breaks_record = current_bisection * go_time > dist

        
    return (time // 2 - last_broken)*2 + 1

if __name__ == "__main__":
    print(part1("day6-input.txt"))
    print(part2alt("day6-input.txt"))
    print(part2("day6-input.txt"))