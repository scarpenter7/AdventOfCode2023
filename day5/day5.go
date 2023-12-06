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
	var maps_list []func(int) int
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
			mymap := buildMap(all_sets[sets_idx])
			maps_list = append(maps_list, mymap)
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
	//fmt.Println("Test 2")
	//testAll(maps_list)
	var wg sync.WaitGroup
	total := 0
	for i, seed_start := range seed_starts {
		for _, seed := range makeRange(seed_start, seed_start+seed_lengths[i]) {
			wg.Add(1)
			total++
			go func(num int) {
				defer wg.Done()
				location := convertSeed(num, maps_list)
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

func buildMap(currSet [][]int) func(int) int {
	set_ptr := &currSet
	return func(num int) int {
		for _, tuple := range *set_ptr {
			destination_start := tuple[0]
			source_start := tuple[1]
			range_len := tuple[2]
			if num >= source_start && num < (source_start+range_len) {
				return destination_start + num - source_start
			}
		}
		return num
	}
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

func makeRange(min, max int) []int {
	a := make([]int, max-min)
	for i := range a {
		a[i] = min + i
	}
	return a
}

func convertSeed(seed int, mapList []func(int) int) int {
	res := seed
	for _, mapfunc := range mapList {
		res = mapfunc(res)
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
	fmt.Println(part2("test.txt"))
	fmt.Println("finished.")
}
