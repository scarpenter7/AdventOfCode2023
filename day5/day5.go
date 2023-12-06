package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

var resContainer = Container{res: -1}

func part2(filename string) int {

	file, _ := os.Open(filename)
	defer file.Close()
	fileScanner := bufio.NewScanner(file)

	fileScanner.Split(bufio.ScanLines)

	linenum := 0
	skiplines := 0
	var all_sets [][][]int
	var curr_set [][]int
	var seed_starts []int
	var seed_lengths []int
	sets_idx := 0
	total_seeds := 0
	start := time.Now()

	for fileScanner.Scan() {
		linenum++
		line := fileScanner.Text()
		if linenum == 1 {
			seeds_strs := strings.Fields(line)[1:]
			for i, seed_str := range seeds_strs {
				num, _ := strconv.Atoi(seed_str)
				if i%2 == 0 {
					seed_starts = append(seed_starts, num)
				} else {
					seed_lengths = append(seed_lengths, num)
					total_seeds += num
				}
			}
			skiplines += 3
		}
		if skiplines > 0 {
			skiplines--
			continue
		}
		if line == "" {
			all_sets = append(all_sets, curr_set)
			curr_set = nil
			sets_idx++
			skiplines++
		} else {
			nums_strs := strings.Fields(line)
			var numRow []int
			for _, num_str := range nums_strs {
				num_int, _ := strconv.Atoi(num_str)
				numRow = append(numRow, num_int)
			}
			curr_set = append(curr_set, numRow)
		}
	}

	//testConvertSeed(all_sets)
	//testConvertSeedOnce(all_sets)
	//testConvertSeedTxtFile(all_sets)

	var wg sync.WaitGroup
	total := 0
	for i, seed_start := range seed_starts {
		for _, seed := range makeRange(seed_start, seed_start+seed_lengths[i]) {
			wg.Add(1)
			total++
			go func(num int) {
				defer wg.Done()
				location := convertSeed(num, all_sets)
				resContainer.compareMinRes(location)
			}(seed)
			if total%10000000 == 0 {
				now := time.Now()
				fmt.Println(total, float32(total)/float32(total_seeds), now.Minute()-start.Minute())
			}
		}
	}
	wg.Wait()
	return resContainer.res
}

func mapfunc(num int, currSet [][]int) int {
	for _, tuple := range currSet {
		destination_start := tuple[0]
		source_start := tuple[1]
		range_len := tuple[2]
		if num >= source_start && num < (source_start+range_len) {
			return destination_start + num - source_start
		}
	}
	return num
}

func testAll(maps_list []func(int) int) {
	fmt.Println(maps_list[0](82))
	fmt.Println(maps_list[1](84))
	fmt.Println(maps_list[2](84))
	fmt.Println(maps_list[3](84))
	fmt.Println(maps_list[4](77))
	fmt.Println(maps_list[5](45))
	fmt.Println(maps_list[6](46))
}

func testConvertSeed(all_sets [][][]int) {
	fmt.Println(all_sets)
	fmt.Println(convertSeed(79, all_sets) == 82)
	fmt.Println(convertSeed(14, all_sets) == 43)
	fmt.Println(convertSeed(55, all_sets) == 86)
	fmt.Println(convertSeed(13, all_sets) == 35)
	fmt.Println(convertSeed(82, all_sets) == 46)
}

func testConvertSeedOnce(all_sets [][][]int) {
	fmt.Println(mapfunc(79, all_sets[0]) == 81)
	fmt.Println(mapfunc(14, all_sets[0]) == 14)
	fmt.Println(mapfunc(55, all_sets[0]) == 57)
	fmt.Println(mapfunc(13, all_sets[0]) == 13)
}

func testConvertSeedTxtFile(all_sets [][][]int) {
	file, _ := os.Open("part1-tests.txt")
	defer file.Close()
	fileScanner := bufio.NewScanner(file)

	fileScanner.Split(bufio.ScanLines)

	for fileScanner.Scan() {
		line := fileScanner.Text()
		if line == "" {
			break
		}
		nums_strs := strings.Fields(line)
		seed, _ := strconv.Atoi(nums_strs[0])
		location, _ := strconv.Atoi(nums_strs[1])
		res := convertSeed(seed, all_sets)
		fmt.Println(seed, location, res)
		fmt.Println(res == location)
		fmt.Println()
	}
}

func makeRange(min, max int) []int {
	a := make([]int, max-min)
	for i := range a {
		a[i] = min + i
	}
	return a
}

func convertSeed(seed int, all_sets [][][]int) int {
	res := seed
	for _, set := range all_sets {
		res = mapfunc(res, set)
	}
	return res
}

type Container struct {
	mu  sync.Mutex
	res int
}

func (c *Container) compareMinRes(num int) {
	c.mu.Lock()
	defer c.mu.Unlock()
	if c.res == -1 || num < c.res {
		c.res = num
		fmt.Println(num)
	}
}

func main() {
	fmt.Println("hello!")
	fmt.Println(part2("day5-input.txt"))
	fmt.Println("finished.")
}
