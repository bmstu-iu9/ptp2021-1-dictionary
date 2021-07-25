import words from "../json/words.json" assert { type: "json" };

var wordsContent = words.entries;

document.getElementById("flipper").onclick = function() {
    document.getElementById("flipper").classList.toggle("flip")
}

function getRandom() {
    return Math.floor(Math.random() * wordsContent.length);
}

function getWordAndTranslation(rand) {
    return {
        word: wordsContent[rand].word,
        trans: wordsContent[rand].translation,
    };
}

function changeWordAndTranslation() {
    var rand = getRandom();
    var data = getWordAndTranslation(rand);
    document.getElementById("front-content").innerText = data.word;
    document.getElementById("back-content").innerText = data.trans;
}

document.getElementById("changeWord").onclick = changeWordAndTranslation;

changeWordAndTranslation()