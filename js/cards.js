var url = new URL(document.location.href);
var mod = url.searchParams.get('mods');
var inwords = [];
filter(mod);

function filter(str) {
    var acceptable = [12];
    for (var i = 0 ; i < str.length ; i++) {
        acceptable[str.charCodeAt(i) - 97] = 1;
    }
    for (var i = 0 ; i < words.length ; i++) {
        //alert(words[i].module - 1);
        //alert(acceptable[words[i].module - 1]);
        //alert(acceptable[words[i].module - 1] == 1);
        if (acceptable[words[i].module - 1] == 1) {
            //alert(words[i].word);
            inwords.push(words[i]);
        }
    }
}

var wordsContent = inwords;

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