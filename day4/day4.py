


def part1(filename):
    res = 0
    with open(filename) as file:
        for line in file.readlines():
            split1 = line.split(':')
            winners_picks = split1[1].split('|')
            winners = set(winners_picks[0].split())
            picks = set(winners_picks[1].split())
            intersection_len = len(winners.intersection(picks))
            if intersection_len == 0:
                continue
            res += 2 ** (intersection_len - 1)
    return res

def part2(filename):
    with open(filename) as file:
        lines = file.readlines()
        res_dict = {line_num: 1 for line_num in range(len(lines))}
        cards_dict = {line_num: 0 for line_num in range(len(lines))}

        # First score the cards
        for card_num, line in enumerate(lines):
            split1 = line.split(':')
            winners_picks = split1[1].split('|')
            winners = set(winners_picks[0].split())
            picks = set(winners_picks[1].split())
            intersection_len = len(winners.intersection(picks))
            cards_dict[card_num] = intersection_len

        # Then count the copies using the pre-computed scores
        for card_num in range(len(lines)):
            score = cards_dict[card_num]
            for card in range(card_num + 1, card_num + score + 1):
                res_dict[card] += res_dict[card_num]

    return sum([res_dict[key] for key in res_dict.keys()])

if __name__ == "__main__":
    print(part1("day4-input.txt"))
    print(part2("day4-input.txt"))