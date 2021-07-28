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

func getWordsFromJson(jsonPath *string, wordsChannel chan string) {
	wordsFileJson, err := os.Open(*jsonPath)

	if err != nil {
		fmt.Println("Invalid path to a file")
	}

	wordsFileJson.Close()
}

func getAudioFromJson(jsonPath *string, audioPath *string) {
	wordsChannel := make(chan string)
	go getWordsFromJson(jsonPath, wordsChannel)
}

func main() {
	wordsFilePtr := flag.String("jsonpath", "../json/words.json", "Path to file with words")
	audioFolderPtr := flag.String("audiopath", "./", "Path to store audio files")
	flag.Parse()
}
