package main

import (
	"flag"
	"fmt"
	"os"
)

type Entries struct {
	Entries []Entry `json:"entries"`
}

type Entry struct {
	Word        string    `json:"word"`
	Translation string    `json:"translation"`
	Pos         string    `json:"pos"`
	Examples    []Example `json:"examples"`
	Module      int       `json:"module"`
}

type Example struct {
	Eng string `json:"eng"`
	Ru  string `json:"ru"`
}

func main() {
	wordsFilePtr := flag.String("path", "../json/words.json", "Path to file with words")
	flag.Parse()

	wordsFileJson, err := os.Open(*wordsFilePtr)

	if err != nil {
		fmt.Println("Invalid path to a file")
	}

	wordsFileJson.Close()
}
