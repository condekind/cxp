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

// todo ... source info.sh, call llvm, get output, send to main
func cons(ch <-chan string, wg *sync.WaitGroup) {

	// loop only breaks when the channel is empty and closed
	for {

		// while there are benchmarks on the channel
		bench, valid := <-ch
		if valid {

			os.Chdir(bench)
			fmt.Printf("Starting benchmark: %s\n", bench)

			// // info.sh source alternative
			// var benchEnv map[string]string
			// benchEnv, _ = godotenv.Read(*infoFilename)
			// for k, v := range benchEnv {
			// 	fmt.Printf("Key: %s\nValue: %s\n\n", k, v)
			// }

			// BENCH_NAME
			// SRC_FILES
			// COMPILE_FLAGS

			// var vars map[string]expand.Variable
			// // If using shell.SourceFile from github/mvdan, DO NOT allow the user
			// // to pass the name of the 'info.sh' file, as the method below allows
			// // arbitrary code execution
			// vars, err := shell.SourceFile("info.sh") // todo: add context w/ timeout
			// if err != nil {
			// 	// BENCH_NAME
			// 	// SRC_FILES
			// 	// COMPILE_FLAGS
			// }
			// if srcFiles, ok := vars["source_files"]; ok {
			// 	//
			// } else {
			// 	//
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

func main() {

	basedir, err := os.Getwd()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	var (
		defChSz    = 32
		ch0size    = flag.Int("bsize", defChSz, "Max channel buffer size")
		numWorkers = flag.Int("workers", 1, "Number of worker threads")
		suitesdir  = flag.String("dir", "suites", "Path to suites directory")
	)
	flag.Parse()

	ch := make(chan string, max(*ch0size, defChSz))
	var wg sync.WaitGroup

	suitespath := filepath.Join(basedir, *suitesdir)
	if fi, err := os.Stat(suitespath); !fi.IsDir() {
		fmt.Println(err)
		os.Exit(1)
	}

	suites, err := ReadDirNames(suitespath)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// producer
	wg.Add(1)
	go func(wg *sync.WaitGroup) {
		for _, suite := range suites {
			crawler := prod(ch, filepath.Join(suitespath, suite))
			err = filepath.Walk(filepath.Join(suitespath, suite), crawler)
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
	fmt.Printf("%d workers, buffer size: %d\n", *numWorkers, *ch0size)
}
