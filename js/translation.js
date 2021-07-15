var url = new URL(document.location.href);
document.getElementById('inpt').value = "";
var task = url.searchParams.get('task');
var lang = url.searchParams.get('lang');
var rb = document.querySelector('.checkAnswer');
if (task == "translate") { rb.style.display = 'none'; }
newWord();

function correct(want) {
    var str = "";
    for (var i = 0 ; i < want.length ; i++) {
        if (i != 0) { str += " ИЛИ "; }
        str += want[i];
    }
    return str;
}


function checkAnswer(want) {
    var got = document.getElementById('inpt').value;
    var yes = 0;
    for (var i = 0 ; i < want.length ; i++) {
        //alert(want[i].toUpperCase() + " " + got.toUpperCase());
        if (want[i].toUpperCase() === got.toUpperCase()) { yes++; }
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
    var rand = Math.floor(Math.random() * data.length);
    var word, trans;
    if (lang == "eng") {
        word = data[rand].word + " (" + data[rand].pos + ")";
        trans = data[rand].translation;
    } else {
        word = data[rand].translation;
        trans = data[rand].word;
    }
    document.getElementById("exercise").textContent = word;
    var answ = new Array();
    var str = "";
    for (var i = 0 ; i < trans.length ; i++) {
        if (trans[i] == ',') {
            answ.push(str);
            str = "";
            i+=2;
        }
        str += trans[i];
        //document.writeln(str);
    }
    answ.push(str);
    document.getElementById('btn1').onclick = function () {
        checkAnswer(answ);
    }
}

