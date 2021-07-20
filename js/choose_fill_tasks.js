function get_random(max) {
    return Math.floor(Math.random() * (max + 1));
}

function choose_task() {
    let ir = get_random(words.length - 1);
    let exercise = document.getElementById("exercise");
    if (lang1 == "eng") {
        exercise.innerHTML = words[ir].word[0].toUpperCase() +  words[ir].word.slice(1);
    } else {
        exercise.innerHTML = words[ir].translation[0].toUpperCase() +  words[ir].translation.slice(1);
    }
    let pos_right = get_random(3);
    let answers = ["", "", "", ""];
	let answers_ind = [ir];
    for (let i = 0; i < 4; i++) {
        if (i == pos_right) {
            if (lang1 == "eng") {
                answers[i] = words[ir].translation;
            } else {
                answers[i] = words[ir].word;
            }
        } else {
            let x = get_random(words.length - 1 - answers_ind.length);
			for (let j = 0; j < answers_ind.length; j++) {
                if (x >= answers_ind[j]) {
                    x++;
                }
            }
            if (lang1 == "eng") {
                answers[i] = words[x].translation;
            } else {
                answers[i] = words[x].word;
            }
			answers_ind.push(x);
            answers_ind.sort(function (a, b) {
                return a - b;
            });
        }
    }
    let labels = document.querySelectorAll(".form-check-label");
    for (let i = 0; i < 4; i++) {
        labels[i].innerHTML = answers[i][0].toUpperCase() +  answers[i].slice(1);
    }
    let radio_buttons = document.querySelectorAll(".form-check-input");
    for (let i = 0; i < 4; i++) {
        let radio_button = radio_buttons[i];
        radio_button.checked = false;
    }
    for (let i = 0; i < 4; i++) {
        let radio_button = radio_buttons[i];
        radio_button.onclick = function () {
            if (answers[i].trim().toLowerCase() != answers[pos_right].trim().toLowerCase()) {
                alert("неверно, правильный ответ: " + answers[pos_right]);
            }
            choose_task();
        }
    }
}

function fill_task() {
    let ir = get_random(words.length - 1);
    let word = words[ir].word.trim();
    let s = words[ir].examples[0].eng;
    word_arr = word.split(" ");
    let re = new RegExp("\\b" + word + "\\b", "i");
    if (s.search(re) == -1) {
        re = new RegExp("\\b" + word + "[a-z]+\\b", "i");
    }
    if ((s.search(re) == -1) && (word[word.length - 1] == "y")) {
        re = new RegExp("\\b" + word.slice(0, word.length - 1) + "ied\\b", "i");
    }
    if (s.search(re) != -1) {
        word = s.match(re)[0];
        s = s.replace(re, "______");
    }
    word = word.split(" ");
    for (let i = 0; i < word.length; i++) {
        word[i] = word[i].toLowerCase();
        if (word_arr[i][0] == word_arr[i][0].toUpperCase()) {
            word[i] = word[i][0].toUpperCase() + word[i].slice(1, word[i].length)
        }
    }
    word = word.join(" ");
    let exercise = document.getElementById("exercise");
    exercise.innerHTML = s;
    let pos_right = get_random(3);
    let answers = ["", "", "", ""];
	let answers_ind = [ir];
    for (let i = 0; i < 4; i++) {
        if (i == pos_right) {
            answers[i] = word;
        } else {
            let x = get_random(words.length - 1 - answers_ind.length);
			for (let j = 0; j < answers_ind.length; j++) {
                if (x >= answers_ind[j]) {
                    x++;
                }
            }
            answers_ind.push(x);
            answers_ind.sort(function (a, b) {
                return a - b;
            });
            answers[i] = words[x].word;
        }
    }
    let labels = document.querySelectorAll(".form-check-label");
    for (let i = 0; i < 4; i++) {
        labels[i].innerHTML = answers[i][0].toUpperCase() +  answers[i].slice(1);
    }
    let radio_buttons = document.querySelectorAll(".form-check-input");
    for (let i = 0; i < 4; i++) {
        let radio_button = radio_buttons[i];
        radio_button.checked = false;
    }
    for (let i = 0; i < 4; i++) {
        let radio_button = radio_buttons[i];
        radio_button.onclick = function () {
            if (answers[i].trim().toLowerCase() != answers[pos_right].trim().toLowerCase()) {
                alert("неверно, правильный ответ: " + answers[pos_right]);
            }
            fill_task();
        }
    }
}

let url1 = new URL(document.location.href);
let task1 = url1.searchParams.get("task");
let lang1 = url1.searchParams.get("lang");
let input = document.querySelector('.form');
if ((task1 == "choose") || (task1 == "fill")) { 
    input.style.display = "none"; 
}
if (task1 == "choose") {
    choose_task();
} else if (task1 == "fill") {
    fill_task();
}