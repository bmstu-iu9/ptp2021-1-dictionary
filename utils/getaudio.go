package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/PuerkitoBio/goquery"
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
	*word = strings.Trim(*word, " ")
	splittedWord := strings.Split(*word, " ")

	re, err := http.Get("https://www.oxfordlearnersdictionaries.com/definition/english/" + *word + "?q=" + *word)
	//re, err := http.Get("https://www.oxfordlearnersdictionaries.com/definition/english/application?q=application")
	if err != nil {
		log.Panic(err)
	}

	defer re.Body.Close()
	if re.StatusCode != 200 {
		log.Println("bad status code")
		log.Println(re.StatusCode)
	}

	doc, err := goquery.NewDocumentFromReader(re.Body)

	if err != nil {
		log.Fatal(err)
	}

	audioUrl, _ := doc.Find(".sound").First().Attr("data-src-mp3")
	fmt.Print(audioUrl)
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
		fmt.Print(entries.Entries[i].Word + " ")
		sendGetRequest(&entries.Entries[i].Word)
		fmt.Println()
	}

	wordsFileJson.Close()
}

func getAudioFromJson(jsonPath *string, audioPath *string) {
	getWordsFromJson(jsonPath)
}

func main() {
	logFile, err := os.OpenFile("./main.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Fatal("There is no log file")
	}
	log.SetOutput(logFile)

	wordsFilePtr := flag.String("jsonpath", "../json/words.json", "Path to file with words")
	audioFolderPtr := flag.String("audiopath", "./", "Path to store audio files")

	flag.Parse()

	getAudioFromJson(wordsFilePtr, audioFolderPtr)
}
