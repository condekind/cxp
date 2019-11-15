package main

import (
	"fmt"
	"os"
	"path/filepath"
)

type Benchmark struct {
	Suite string `json:"suite"` // Uppercased first letter
	Bench string `json:"bench"` // Uppercased first letter
}

func ReadDirNames(s string) ([]string, error) {
	f, err := os.Open(s)
	if err != nil {
		return []string{}, err
	}
	fnames, err := f.Readdirnames(-1)
	if err != nil {
		return fnames, err
	}
	return fnames, nil
}

func main() {

	//fnames, _ := ReadDirNames("./src")
	basedir, _ := os.Getwd()
	fmt.Println(basedir)

	err := filepath.Walk(".",
		func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			fmt.Println(path, info.Size())
			return nil
		})
	if err != nil {
		fmt.Println(err)
	}

}
