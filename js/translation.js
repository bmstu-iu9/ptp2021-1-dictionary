function trim(word) {
    var str = "";
    var i = 0;
    for (i; word[i] == ' ' || word[i] == '\n' || word[i] == '\t'; i += 1) {}
    var j = word.length - 1;
    for (j; word[j] == ' ' || word[j] == '\n' || word[j] == '\t'; j -= 1) {}
    for (i; i <= j; i += 1) {
        str += word[i];
    }
    return str;
}

function parse(str) {
    var i = 0;
    var answ = new Array();
    var wrd = "";
    for (i; i < str.length; i += 1) {
        if (str[i] == ',' || str[i] == '/') {
            answ.push(trim(wrd));
            wrd = "";
            continue;
        }
        if (str[i] == '(' && (i == 0 || str[i - 1] != ' ')) {
            var wrd2 = wrd;
            i += 1;
            for (i; str[i] != ')' ; i++) {
                wrd2 += str[i];
            }
            i += 1;
            for (i; i < str.length && str[i] != ',' && str[i] != '/' ; i++) {
                wrd += str[i];
                wrd2 += str[i];
            }
            if (i!= str.length) {
                answ.push(trim(wrd));
                wrd = "";
            }
            answ.push(trim(wrd2));
        } else {
            if (str[i] == '(') {
                for (i; str[i] != ')' ; i++) {}
            } else {
                wrd += str[i];
            }
        }
    }
    answ.push(trim(wrd));
    return answ;
}

function correct(want) {
    var str = "";
    for (var i = 0 ; i < want.length ; i++) {
        if (i != 0) { str += " ИЛИ "; }
        str += want[i];
    }
    return str;
}

function checkAnswer(want) {
    var got = trim(document.getElementById('inpt').value);
    var yes = 0;
    for (var i = 0 ; i < want.length ; i++) {
        //alert(want[i].toUpperCase() + " " + got.toUpperCase());
        if ((want[i].toLowerCase().replace(/ё/g, "е") === got.toLowerCase()) || (want[i].toLowerCase() === got.toLowerCase())) { yes++; }
    }
    if (yes != 0) { 
        newWord();
        document.getElementById('inpt').value = "";
        document.querySelector('.commentary').textContent = "";
    } else {
        document.querySelector('.commentary').textContent = "Неправильный ответ. Правильный: " + correct(want);
    }
}

function newWord() {
    var rand = Math.floor(Math.random() * words.length);
    var word, trans;
    if (lang == "eng") {
        word = trim(words[rand].word) + " (" + trim(words[rand].pos) + ")";
        trans = trim(words[rand].translation);
    } else {
        word = trim(words[rand].translation);
        trans = trim(words[rand].word);
    }
    //alert(word);
    document.getElementById("exercise").textContent = word;
    var answ = parse(trans);
    document.getElementById('btn1').onclick = function () {
        checkAnswer(answ);
    }
    document.getElementById('inpt').addEventListener('keydown', function(e) {
        if (e.keyCode === 13) {
            checkAnswer(answ);
        }
    });
}

var url = new URL(document.location.href);
document.getElementById('inpt').value = "";
var task = url.searchParams.get('task');
var lang = url.searchParams.get('lang');
var rb = document.querySelector('.checkAnswer');
if (task == "translate") { 
    rb.style.display = 'none';
    newWord();
}
