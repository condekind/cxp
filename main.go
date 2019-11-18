package main

import (
	"flag"
	"fmt"
	"os"
	"sync"

	"path/filepath"
)

type statistic struct {
	name        string
	value       int
	description string
}

var (
	defaultChSz       = 32
	ch0Sz             *int
	ch1Sz             *int
	ch2Sz             *int
	defaultNumWorkers = 1
	numWorkers        *int
	suitepath         *string
	sBenchCmp         *bool
	sBenchDir         *string
)

type benchInfo map[string]map[string][]statistic

func ReadDirNames(s string) ([]string, error) {
	f, err := os.Open(s)
	if err != nil {
		return nil, err
	}
	fnames, err := f.Readdirnames(-1)
	if err != nil {
		return nil, err
	}
	return fnames, nil
}

func prod(ch chan<- string, p string) func(string, os.FileInfo, error) error {

	benchs := make(map[string]bool)

	return func(p string, _ os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if filepath.Ext(p) != ".c" {
			return nil
		}

		benchDir := filepath.Dir(p)
		if benchDir == "." {
			return err
		}

		if _, err = os.Stat(benchDir); err != nil {
			return nil
		}

		if _, seen := benchs[benchDir]; seen {
			return nil
		}

		benchs[benchDir] = true
		ch <- benchDir
		return nil
	}
}

func cons(ch <-chan string, wg *sync.WaitGroup) {

	// loop only breaks when the channel is empty and closed
	for {

		// while there are benchmarks on the channel
		bench, valid := <-ch
		if valid {

			os.Chdir(bench)
			fmt.Printf("Starting benchmark: %s\n", bench)

			// fnames, err := ReadDirNames(bench)
			// if err != nil {
			// 	fmt.Println(err)
			// 	continue
			// }

			// { // todo ... source info.sh, call llvm, get output, send to main
			// 	var vars map[string]expand.Variable
			// 	var err error
			// 	vars, err = shell.SourceFile("info.sh") // todo: add context w/ timeout
			// }

		} else {
			// channel is empty and closed
			wg.Done()
			return
		}

	}
}

func max(a, b int) int {
	if b > a {
		return b
	} else {
		return a
	}
}

func init() {
	ch0Sz = flag.Int("buff", defaultChSz, "Channel buffer size")
	ch1Sz = flag.Int("buff1", defaultChSz, "Channel buffer size")
	ch2Sz = flag.Int("buff2", defaultChSz, "Channel buffer size")
	numWorkers = flag.Int("workers", defaultNumWorkers, "Channel buffer size")
	suitepath = flag.String("dir", "suites", "Path to suites directory")
	sBenchCmp = flag.Bool("b", false, "Set to true to compile a single benchmark")
	sBenchDir = flag.String("bdir", "", "Path to single benchmark folder")
}

func main() {

	basedir, err := os.Getwd()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	flag.Parse()
	*ch0Sz = max(*ch0Sz, defaultChSz)
	*ch1Sz = max(*ch1Sz, defaultChSz)
	*ch2Sz = max(*ch2Sz, defaultChSz)
	*numWorkers = max(*numWorkers, defaultNumWorkers)

	ch := make(chan string, max(*ch0Sz, *ch1Sz))
	var wg sync.WaitGroup

	suitesdir := filepath.Join(basedir, *suitepath)
	if fi, err := os.Stat(suitesdir); !fi.IsDir() {
		fmt.Println(err)
		os.Exit(1)
	}

	suites, err := ReadDirNames(suitesdir)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// producer
	wg.Add(1)
	go func(wg *sync.WaitGroup) {
		for _, suite := range suites {
			crawler := prod(ch, filepath.Join(suitesdir, suite))
			err = filepath.Walk(filepath.Join(suitesdir, suite), crawler)
			if err != nil {
				fmt.Println(err)
			}
		}
		close(ch)
		wg.Done()
	}(&wg)

	// consumers
	for i := 0; i < *numWorkers; i++ {
		wg.Add(1)
		go cons(ch, &wg)
	}

	wg.Wait()
}
