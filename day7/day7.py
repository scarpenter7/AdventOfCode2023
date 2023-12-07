import functools

card_rank = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
card_rank_J = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 1, "Q": 12, "K": 13, "A": 14}

@functools.total_ordering
class Hand:
    def __init__(self, hand_str):
        self.hand_str = hand_str

    def _is_valid_operand(self, other):
        return (hasattr(other, "hand_str"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.hand_str == other.hand_str)

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        self_hand_type = self.classify_hand_type()
        other_hand_type = other.classify_hand_type()
        if self_hand_type < other_hand_type:
            return True
        elif self_hand_type > other_hand_type:
            return False

        # same hand type
        for self_char, other_char in zip(self.hand_str, other.hand_str):
            if self_char != other_char:
                return card_rank[self_char] < card_rank[other_char]
        return False  # equal

    def classify_hand_type(self):
        hand_dict = self.build_hand_dict()
        if len(hand_dict.keys()) == 1:
            return 7  # 5 of a kind
        if len(hand_dict.keys()) == 5:
            return 1  # high card
        if len(hand_dict.keys()) == 4:
            return 2  # one pair
        if len(hand_dict.keys()) == 2:
            # either 4 of a kind OR full house
            for key, val in hand_dict.items():
                if val == 4 or val == 1:
                    return 6  # 4 of a kind
                else:
                    return 5  # full house
        if len(hand_dict.keys()) == 3:
            # either 2 pair of 3 of a kind
            for key, val in hand_dict.items():
                if val == 3:
                    return 4  # 3 of a kind
            return 3
        return -1  # ERROR


    def build_hand_dict(self):
        res = {}
        for char in self.hand_str:
            if char not in res.keys():
                res[char] = 1
            else:
                res[char] += 1
        return res

def part1(filename):
    res = 0
    with open(filename) as file:
        lines = file.readlines()
        hands_bids_dict = {l.split()[0] : int(l.split()[1]) for l in lines}
        hand_objs_list = sorted([Hand(s) for s in hands_bids_dict.keys()])
        for i, hand in enumerate(hand_objs_list):
            multiplier = i + 1
            res += multiplier * hands_bids_dict[hand.hand_str]
    return res

if __name__ == "__main__":
    print(part1("day7-input.txt"))
    #print(part2("test.txt"))