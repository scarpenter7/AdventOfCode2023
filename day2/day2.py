RED = 12
GREEN = 13
BLUE = 14

def part1(filename):
    res = 0
    with open(filename) as file:
        for line in file.readlines():
            split1 = line.replace(" ", "").split(':')
            ID = int(split1[0].replace("Game", ""))
            draws = split1[1].split(';')
            red_draw, blue_draw, green_draw = (0, 0, 0)
            possible = True
            for draw in draws:
                color_separated = draw.split(',')
                for color in color_separated:
                    if "red" in color:
                        red_draw = int(color.replace("red", ""))
                    if "blue" in color:
                        blue_draw = int(color.replace("blue", ""))
                    if "green" in color:
                        green_draw = int(color.replace("green", ""))
                if red_draw > RED or blue_draw > BLUE or green_draw > GREEN:
                    possible = False
                    break
            if possible:
                res += ID
    return res

def part2(filename):
    res = 0
    with open(filename) as file:
        for line in file.readlines():
            split1 = line.replace(" ", "").split(':')
            ID = int(split1[0].replace("Game", ""))
            draws = split1[1].split(';')
            red_max, blue_max, green_max = (0, 0, 0)
            red_draw, blue_draw, green_draw = (0, 0, 0)
            for draw in draws:
                color_separated = draw.split(',')
                for color_str in color_separated:
                    if "red" in color_str:
                        red_draw = int(color_str.replace("red", ""))
                    if "blue" in color_str:
                        blue_draw = int(color_str.replace("blue", ""))
                    if "green" in color_str:
                        green_draw = int(color_str.replace("green", ""))
                    if red_draw > red_max:
                        red_max = red_draw
                    if blue_draw > blue_max:
                        blue_max = blue_draw
                    if green_draw > green_max:
                        green_max = green_draw
            res += power(red_max, green_max, blue_max)
    return res

def power(reds, greens, blues):
    return reds * greens * blues

if __name__ == "__main__":
    print(part1("day2-1input.txt"))
    print(part2("day2-1input.txt"))