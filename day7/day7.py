import functools

card_rank = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
card_rank_J = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 1, "Q": 12, "K": 13, "A": 14}

@functools.total_ordering
class Hand:
    def __init__(self, hand_str, bid, wild_Js):
        self.bid = bid
        self.hand_str = hand_str 
        self.wild_Js = wild_Js  # boolean
        self.hand_dict = {}
        self.build_hand_dict()
        self.hand_type = self.classify_hand_type()
        if wild_Js:
            self.card_rank = card_rank_J
        else:
            self.card_rank = card_rank

    def __lt__(self, other):
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type

        # same hand type
        for self_char, other_char in zip(self.hand_str, other.hand_str):
            if self_char != other_char:
                return self.card_rank[self_char] < self.card_rank[other_char]
        return False  # equal

    def classify_hand_type(self):
        if len(self.hand_dict.keys()) == 1:
            return 7  # 5 of a kind
        if len(self.hand_dict.keys()) == 5:
            return 1  # high card
        if len(self.hand_dict.keys()) == 4:
            return 2  # one pair
        if len(self.hand_dict.keys()) == 2:
            # either 4 of a kind OR full house
            for key, val in self.hand_dict.items():
                if val == 4 or val == 1:
                    return 6  # 4 of a kind
                else:
                    return 5  # full house
        if len(self.hand_dict.keys()) == 3:
            # either 2 pair of 3 of a kind
            for key, val in self.hand_dict.items():
                if val == 3:
                    return 4  # 3 of a kind
            return 3
        return -1  # ERROR

    def build_hand_dict(self):
        for char in self.hand_str:
            if char not in self.hand_dict.keys():
                self.hand_dict[char] = 1
            else:
                self.hand_dict[char] += 1
        if self.wild_Js:
            self.optimize_hand()
    
    def optimize_hand(self):
        if 'J' not in self.hand_dict.keys():
            return
        numJs = self.hand_dict['J']
        if numJs == 5:
            return
        del self.hand_dict['J']
        
        highest_cardinality_card = max(self.hand_dict, key=self.hand_dict.get)
        self.hand_dict[highest_cardinality_card] += numJs


def part1(filename):
    with open(filename) as file:
        lines = file.readlines()
        hand_objs_list = sorted([Hand(l.split()[0], int(l.split()[1]), False) for l in lines])
    return sum([(i + 1) * hand.bid for i, hand in enumerate(hand_objs_list)])

def part2(filename):
    with open(filename) as file:
        lines = file.readlines()
        hand_objs_list = sorted([Hand(l.split()[0], int(l.split()[1]), True) for l in lines])
    return sum([(i + 1) * hand.bid for i, hand in enumerate(hand_objs_list)])

if __name__ == "__main__":
    print(part1("day7-input.txt"))
    print(part2("day7-input.txt"))