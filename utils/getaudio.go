package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
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

func downloadFile(filePath string, fileUrl string) error {
	resp, err := http.Get(fileUrl)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	out, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	return err
}

func prepareWordForRequest(word *string) (string, string) {
	*word = strings.Trim(*word, " ")
	*word = strings.ToLower(*word)
	splittedWord := strings.Split(*word, " ")

	if len(splittedWord) > 1 {
		return strings.Join(splittedWord[:], "-"), strings.Join(splittedWord[:], "+")
	}
	return *word, *word
}

// https://www.oxfordlearnersdictionaries.com/definition/english/word?q=word
// https://www.oxfordlearnersdictionaries.com/definition/english/splitted-word?q=splitted+word

func sendGetRequestOxfordDictionary(word *string, audioFolderPtr *string) {
	pathVariable, queryVariable := prepareWordForRequest(word)

	fmt.Println(pathVariable + "  " + queryVariable)
	re, err := http.Get("https://www.oxfordlearnersdictionaries.com/definition/english/" + pathVariable + "?q=" + queryVariable)

	if err != nil {
		log.Panic(err)
	}

	defer re.Body.Close()

	if re.StatusCode != 200 {
		log.Println("bad status code")
		log.Println(re.StatusCode)
		log.Println(*word)
		// try to bruteforce
	} else {
		doc, err := goquery.NewDocumentFromReader(re.Body)

		if err != nil {
			log.Fatal(err)
		}

		audioUrl, _ := doc.Find(".sound").First().Attr("data-src-mp3")
		log.Println("downloaded " + audioUrl)
		downloadErr := downloadFile(*audioFolderPtr+"/"+*word+".mp3", audioUrl)
		if downloadErr != nil {
			log.Println(downloadErr)
		}
	}
}

func getAudioFromJson(jsonPath *string, audioFolderPath *string) {
	wordsFileJson, err := os.Open(*jsonPath)

	if err != nil {
		fmt.Println("Invalid path to a file")
	}

	byteValue, _ := ioutil.ReadAll(wordsFileJson)

	var entries Entries
	json.Unmarshal(byteValue, &entries)

	for i := 0; i < len(entries.Entries); i++ {
		if entries.Entries[i].Pos != "phr" {
			sendGetRequestOxfordDictionary(&entries.Entries[i].Word, audioFolderPath)
		}
	}

	wordsFileJson.Close()
}

func main() {
	logFile, err := os.OpenFile("./main.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Fatal("There is no log file")
	}
	log.SetOutput(logFile)

	wordsFilePtr := flag.String("jsonpath", "../json/words.json", "Path to file with words")
	audioFolderPtr := flag.String("audiopath", "./audio", "Path to store audio files")

	flag.Parse()

	if _, pathErr := os.Stat(*audioFolderPtr); os.IsNotExist(pathErr) {
		pathErr := os.Mkdir(*audioFolderPtr, 0770)
		if pathErr != nil {
			log.Panicln("Can't create folder for audio")
		}
		getAudioFromJson(wordsFilePtr, audioFolderPtr)
	}
}
