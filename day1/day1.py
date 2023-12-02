import re

word_to_num_dict = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
reversed_nums_dict = {key[::-1] : val for key, val in word_to_num_dict.items()}

def part1(filename):
    res = 0

    with open(filename) as file:
        for line in file.readlines():
            filtered_line = re.sub('\D', '', line)
            res += int(filtered_line[0] + filtered_line[-1])
    return res

def part2_alt(filename):
    word_trie = make_trie(word_to_num_dict.keys())
    word_trie_reversed = make_trie(reversed_nums_dict.keys())
    res = 0

    with open(filename) as file:
        for line in file.readlines():
            first_num = extractFirstNumber(line, word_trie, word_to_num_dict)
            second_num = extractFirstNumber(line[::-1][1:], word_trie_reversed, reversed_nums_dict)
            res += first_num*10 + second_num
    return res

def extractFirstNumber(line, trie, number_dict):
    # find the first number in the line (digit or word)
    for i, char in enumerate(line):
        remaining = line[i:]
        for j, char2 in enumerate(remaining):
            if char2.isdigit():
                return int(char2)
            word = line[i:i+j+1]
            if word in number_dict.keys():
                return number_dict[word]
            if trie_get(trie, word) is None:
                break

def make_trie(words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
    return root

def trie_get(trie, path):
    if len(path) == 0:
        return trie
    if path[0] not in trie.keys():
        return
    return trie_get(trie[path[0]], path[1:])

if __name__ == "__main__":
    print(part1("day1-1input.txt"))
    print()
    print(part2_alt("day1-2input.txt"))