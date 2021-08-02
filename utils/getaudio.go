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

func processCase(mainUrl *string, pathVariable *string, queryVariable *string, suffix string) string {
	re, err := http.Get(*mainUrl + *pathVariable + suffix + "?q=" + *queryVariable)
	if err != nil {
		log.Println(re.StatusCode)
	}

	defer re.Body.Close()

	doc, docErr := goquery.NewDocumentFromReader(re.Body)
	if docErr != nil {
		log.Fatal(docErr)
	}

	return doc.Find(".pos").First().Text()
}

func processExceptionalCases(re **http.Response,
	mainUrl *string, pathVariable *string,
	queryVariable *string, pos *string) error {

	type1 := processCase(mainUrl, pathVariable, queryVariable, "_1")
	type2 := processCase(mainUrl, pathVariable, queryVariable, "_2")
	var err error

	if len(type1) > 0 && len(type2) > 0 {
		if *pos == string(type1[0]) {
			*re, err = http.Get(*mainUrl + *pathVariable + "_1?q=" + *queryVariable)
		} else if *pos == string(type2[0]) {
			*re, err = http.Get(*mainUrl + *pathVariable + "_2?q=" + *queryVariable)
		}
	}
	return err
}

// https://www.oxfordlearnersdictionaries.com/definition/english/word?q=word
// https://www.oxfordlearnersdictionaries.com/definition/english/splitted-word?q=splitted+word

func sendGetRequestOxfordDictionary(word *string, pos *string, audioFolderPtr *string) {
	pathVariable, queryVariable := prepareWordForRequest(word)
	mainUrl := "https://www.oxfordlearnersdictionaries.com/definition/english/"

	re, err := http.Get(mainUrl + pathVariable + "?q=" + queryVariable)

	if err != nil {
		log.Panic(err)
	}

	defer re.Body.Close()

	if re.StatusCode != 200 {
		err := processExceptionalCases(&re, &mainUrl, &pathVariable, &queryVariable, pos)
		if err != nil {
			log.Printf("Cannot download word %s: not found or bad request\n", *word)
		}
	}

	doc, err := goquery.NewDocumentFromReader(re.Body)

	if err != nil {
		log.Fatal(err)
	}

	audioUrl, _ := doc.Find(".sound").First().Attr("data-src-mp3")

	downloadErr := downloadFile(*audioFolderPtr+"/"+*word+".mp3", audioUrl)

	if downloadErr != nil {
		log.Printf("Cannot download word %s: %e\n", *word, downloadErr)
		if re.StatusCode == 404 {
			log.Println("There is no such word in dictionary")
		}
		log.Println(audioUrl)
	} else {
		log.Println("downloaded " + audioUrl)
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
			sendGetRequestOxfordDictionary(&entries.Entries[i].Word, &entries.Entries[i].Pos, audioFolderPath)
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
	}
	getAudioFromJson(wordsFilePtr, audioFolderPtr)
}
