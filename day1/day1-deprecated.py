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

def part2(filename):
    word_trie = make_trie(word_to_num_dict.keys())
    res = 0

    test = 0
    with open("correct-answers-1-2.txt") as test_file:
        with open(filename) as file:
            for (line, test_line) in zip(file.readlines(), test_file.readlines()):

                backidx = 0
                frontidx = 0
                processedNums = []
                for char in line:
                    if char == '\n':
                        continue
                    frontidx += 1
                    substr = line[backidx:frontidx]
                    if char.isdigit():
                        processedNums.append(int(char))
                        backidx = frontidx
                    elif substr in word_to_num_dict.keys():
                        processedNums.append(word_to_num_dict[substr])
                        if char in word_trie.keys():
                            backidx = frontidx - 1
                        else:
                            backidx = frontidx
                    elif trie_get(word_trie, substr) is None:
                        for i, letter in enumerate(substr):
                            if i == 0: # only check the letters after the first
                                continue
                            if letter in word_trie.keys():
                                backidx += i
                                break

                if test < 1000:
                    if str(int(str(processedNums[0]) + str(processedNums[-1]))) != test_line[:-1]:
                        print(line)
                        print(processedNums)
                        print(int(str(processedNums[0]) + str(processedNums[-1])))
                        print("TEST FAILURE")
                        print()
                        print()
                    test += 1
                res += int(str(processedNums[0]) + str(processedNums[-1]))
    return res

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
    print(part2("day1-2input.txt"))
