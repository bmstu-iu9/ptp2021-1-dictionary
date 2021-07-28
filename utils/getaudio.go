package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
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

func sendGetRequest(word *string) {
	http.Get("https://www.oxfordlearnersdictionaries.com/definition/english/hello?q=hello")
}

func getWordsFromJson(jsonPath *string) {
	wordsFileJson, err := os.Open(*jsonPath)

	if err != nil {
		fmt.Println("Invalid path to a file")
	}

	byteValue, _ := ioutil.ReadAll(wordsFileJson)

	var entries Entries
	json.Unmarshal(byteValue, &entries)

	for i := 0; i < len(entries.Entries); i++ {
		fmt.Println(entries.Entries[i].Word)
	}

	wordsFileJson.Close()
}

func getAudioFromJson(jsonPath *string, audioPath *string) {
	go getWordsFromJson(jsonPath)
}

func main() {
	wordsFilePtr := flag.String("jsonpath", "../json/words.json", "Path to file with words")
	audioFolderPtr := flag.String("audiopath", "./", "Path to store audio files")

	flag.Parse()

	getAudioFromJson(wordsFilePtr, audioFolderPtr)
}
