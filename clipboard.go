// +build ignore

import (
	"os"
	"path/filepath"
)

func Crawler(benchpaths chan<- string, suite, path string) error {

	benchs := make([]string)
	currSuite := suite
	currBench := ""

	if data[currSuite] == nil {
		data[currSuite] = make(map[string][]statistic)
	}

	return func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if filepath.Ext(path) != ".c" {
			return nil
		}
		benchDir, err = filepath.Dir(path)
		if err != nil {
			currBench = ""
			return err
		}
		currBench = filepath.Base(benchDir)
		if st, ok := data[currSuite][currBench]; ok {
			return nil
		} else if err = os.Chdir(benchDir); err != nil {
			return err
		} else {
			data[currSuite][currBench] = make([]statistic)
			crawlerFn()
		}
		return nil
		//
	}
}