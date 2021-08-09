var modules = [12];
var ehe = 1;
var ehetenandayo = 0;
var mds = "";
modules[0] = 1;
document.getElementById('filter_1').style.backgroundColor = "dimgrey";
document.getElementById('filter_1').style.color = "antiquewhite";
timetowork();

function changefilter(j) {
    ehetenandayo = 0;
    var is_off = document.getElementById('filter_' + j).style.backgroundColor == "aliceblue" || document.getElementById('filter_' + j).style.backgroundColor == "";
    if (is_off) {
        document.getElementById('filter_' + j).style.backgroundColor = "dimgrey";
        document.getElementById('filter_' + j).style.color = "antiquewhite";
        modules[j - 1] = 1;
        ehe++;
        timetowork();
    } else if (ehe != 1) {
        ehetenandayo = 0;
        document.getElementById('filter_' + j).style.backgroundColor = "aliceblue";
        document.getElementById('filter_' + j).style.color = "black";
        modules[j - 1] = 0;
        ehe--;
        timetowork();
    } else {
        ehetenandayo++;
        if (ehetenandayo == 50) {
            ehetenandayo = 0;
            window.location.replace("https://www.youtube.com/watch?v=dQw4w9WgXcQ");
        }
    }
}

function timetowork() {
    mds="";
    var quant = [];
    var only = "";
    var mods = "";
    var msg = "В упражнениях будут использоваться слова ";
    for (var i = 0 ; i < 12 ; i++) {
        if (modules[i] == 1) {
            quant.push(i + 1);
        }
    }
    if (quant.length == 0) {
        alert("так низя");
        only = " только ";
        mods = " модуля";
        modules[0] = 1;
        document.getElementById('filter_1').style.backgroundColor = "dimgrey";
        document.getElementById('filter_1').style.color = "antiquewhite";
        quant.push(1);
    } else {
        if (quant.length == 1) {
            only = " только ";
            mods = " модуля";
        } else {
            only = "";
            mods = " модулей";
        }
    }
    msg += (only + "из ");
    for (var i = 0 ; i < quant.length ; i++) {
        msg += (quant[i] + "-ого");
        if (i < quant.length - 2) {
            msg += ", ";
        }
        if (i == quant.length - 2) {
            msg += " и ";
        }
    }
    msg += mods;
    document.getElementById('currentmods').innerText=msg;
    for (var i = 0 ; i < 12 ; i++) {
        if (modules[i] == 1) {
            mds += String.fromCharCode('a'.charCodeAt(0) + i);
        }
    }
    document.getElementById('ex1btn').href = "cards.html?mods=" + mds;
    document.getElementById('ex2btn').href = "exercise_page.html?task=translate&lang=ru&mods=" + mds;
    document.getElementById('ex3btn').href = "exercise_page.html?task=translate&lang=eng&mods=" + mds;
    document.getElementById('ex4btn').href = "exercise_page.html?task=choose&lang=eng&mods=" + mds;
    document.getElementById('ex5btn').href = "exercise_page.html?task=choose&lang=ru&mods=" + mds;
    document.getElementById('ex6btn').href = "exercise_page.html?task=fill&lang=eng&mods=" + mds;
    //alert(mds);
}