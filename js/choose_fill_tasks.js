var word_articles = [];
let url1 = new URL(document.location.href);
let task1 = url1.searchParams.get("task");
let lang1 = url1.searchParams.get("lang");
//let mds1 = url1.searchParams.get('mods');
//alert(mds1);
//filter(mds1);
//alert(word_articles);
let input = document.querySelector('.form');
word_articles = inwords;
if ((task1 == "choose") || (task1 == "fill")) { 
    input.style.display = "none";
    choose_and_fill_tasks();
}

function get_random(max) {
    return Math.floor(Math.random() * (max + 1));
}

function write_exercise(exercise) {
    let ex = document.getElementById("exercise");
    ex.innerHTML = exercise[0].toUpperCase() +  exercise.slice(1);
}

function fillmodule(mod) {
    var ret = [];
    for (var i = 0 ; i < word_articles.length ; i++) {
        if (word_articles[i].module == mod) {
            ret.push(i);
        }
    }
    return ret;
}

function sortpos(inp, ps) {
    var ret = [];
    //alert(inp);
    for (var i = 0 ; i < inp.length ; i++) {
        if (word_articles[inp[i]].pos == ps) {
            ret.push(inp[i]);
        }
    }
    //alert(ret);
    return ret;
}

function notduplicate(num, nums) {
    for (var i = 0 ; i < nums.length ; i++) {
        //alert(nums[i] + " <=> " + num);
        if (nums[i] == num) {
            return false;
        }
    }
    return true;
}

function fillanswers(from, to) {
    //alert(to);
    //alert(from);
    for (var i = 0 ; i < 4 ; i++) {
        if (to[i] != -1) { continue; } else {
            var rand = Math.floor(Math.random() * from.length);
            if (notduplicate(from[rand], to)) {
                to[i] = from[rand];
            } else {
                i--;
            }
        }
    }
    //alert(to);
    return to;
}

function make_answers_ind(ir) {
    let pos_right = get_random(3);
    let answers_ind = [-1, -1, -1, -1];
    answers_ind[pos_right] = ir;
    //document.writeln("Всего слов: " + word_articles.length)
    var viable = fillmodule(word_articles[ir].module);
    //document.writeln("Слов из этого же модуля: " + viable.length);
    viable = sortpos(viable, word_articles[ir].pos);
    //document.writeln("Слов из этого модуля с такой же часть речи: " + viable.length);
    //alert(viable);
    if (viable.length < 4) {
        ir = get_random(word_articles.length - 1);
        let a1 = make_answers_ind(ir);
        return a1;
        //alert("Подходящих слов всего лишь " + viable.length +", так что я спасу нас обоих от головной боли, не прогружая эту страницу дальше");
    } else {
        answers_ind = fillanswers(viable, answers_ind);
    }
    //alert(answers_ind);
    return [pos_right, answers_ind];
}

function make_answers(answers_ind) {
    let answers = ["", "", "", ""];
    for (let i = 0; i < 4; i++) {
        if ((task1 == "choose") && (lang1 == "ru")) {
            answers[i] = word_articles[answers_ind[i]].translation;
        } else {
            answers[i] = word_articles[answers_ind[i]].word
        }
    }
    return answers;
}

function write_answers(answers) {
    let labels = document.querySelectorAll(".form-check-label");
    for (let i = 0; i < 4; i++) {
        labels[i].innerHTML = answers[i][0].toUpperCase() +  answers[i].slice(1);
    }
}

function switch_off_radio_button() {
    let radio_buttons = document.querySelectorAll(".form-check-input");
    for (let i = 0; i < 4; i++) {
        let radio_button = radio_buttons[i];
        radio_button.checked = false;
    }
}

function check_answer_on_click(pos_right, answers) {
    let radio_buttons = document.querySelectorAll(".form-check-input");
    for (let i = 0; i < 4; i++) {
        let radio_button = radio_buttons[i];
        radio_button.onclick = function () {
            if (answers[i].trim().toLowerCase() != answers[pos_right].trim().toLowerCase()) {
                alert("неверно, правильный ответ: " + answers[pos_right]);
            }
            choose_and_fill_tasks();
        }
    }
}

function search_word_in_example(word, s) {
    let word_arr = word.split(" ");
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
    } else {
        let w1 = "";
        for (let i = 0; i < word_arr.length - 1; i++) {
            w1 += ("\\b" + word_arr[i] + "[a-z]*\\b|");
            if (word_arr[i][word_arr[i].length - 1] == "y") {
                w1 += ("\\b" + word_arr[i].slice(0, word_arr[i].length - 1) + "ied\\b|");
            }
        }
        w1 += "\\b" + word_arr[word_arr.length - 1] + "[a-z]*\\b"
        if (word_arr[word_arr.length - 1][word_arr[word_arr.length - 1].length - 1] == "y") {
            w1 += ("|\\b" + word_arr[word_arr.length - 1].slice(0, word_arr[word_arr.length - 1].length - 1) + "ied\\b");
        }
        let re1 = new RegExp(w1, "gi");
        let s_words = Array.from(s.matchAll(re1));
        let s_words1 = [];
        let corr_ans = "";
        for (let i = 0; i < s_words.length - word_arr.length + 1; i++) {
            let k = 0;
            for (let j = 0; j < word_arr.length; j++) {
                let w2 = "\\b" + word_arr[j] + "[a-z]*\\b";
                if (word_arr[j][word_arr[j].length - 1] == "y") {
                    w2 += ("|\\b" + word_arr[j].slice(0, word_arr[j].length - 1) + "ied\\b");
                }
                let re2 = new RegExp(w2, "i");
                if (s_words[i + j][0].search(re2) != -1) {
                    k++;
                }
            }
            if (k == word_arr.length) {
                for (let j = 0; j < word_arr.length; j++) {
                    s_words1.push(s_words[i + j]);
                    corr_ans += (s_words[i + j][0] + " ");
                }
            }
        }
        corr_ans = corr_ans.trim();
        if (corr_ans == "") {
            return [word, s];
        }
        let x = s_words1[0].index;
        let y = s_words1[s_words1.length - 1].index + s_words1[s_words1.length - 1][0].length;
        let s1 = s.slice(x, y);
        s1 = s1.replace(re1, "______");
        s = s.slice(0, x) + s1 + s.slice(y, s.length);
        let re3 = /(______\s)+______/g;
        s = s.replace(re3, "______");
        word = corr_ans;
    }
    word = word.split(" ");
    for (let i = 0; i < word.length; i++) {
        word[i] = word[i].toLowerCase();
        if (word_arr[i][0] == word_arr[i][0].toUpperCase()) {
            word[i] = word[i][0].toUpperCase() + word[i].slice(1, word[i].length)
        }
    }
    word = word.join(" ");
    return [word, s];
}

function search_word_in_s(word, s) {
    let found_word = "";
    let ind = s.indexOf("<<b>");
    while (ind != -1) {
        let ind1 = s.indexOf("<d>>");
        found_word += s.slice(ind + 4, ind1);
        found_word += " ";
        s = s.slice(0, ind) + "______" + s.slice(ind1 + 4, s.length);
        ind = s.indexOf("<<b>");
    }
    found_word = found_word.trim();
    if (found_word != "") {
        return [found_word, s];
    } else {
        return [word, s];
    }
}

function choose_and_fill_tasks() {
    let ir = get_random(word_articles.length - 1);
    let word = word_articles[ir].word.trim();
    if (task1 == "choose") {
        if (lang1 == "ru") {
            write_exercise(word_articles[ir].word);
        } else {
            write_exercise(word_articles[ir].translation);
        }
    } else {
        let s = word_articles[ir].examples[0].eng;
        let a;
        if (s.indexOf("<<b>") != -1) {
            a = search_word_in_s(word, s);
        } else {
            a = search_word_in_example(word, s);
        }
        word = a[0];
        s = a[1];
        write_exercise(s);
    }
    let a1 = make_answers_ind(ir);
    let pos_right = a1[0];
    let answers_ind = a1[1];
    let answers = make_answers(answers_ind);
    if (task1 == "fill") {
        answers[pos_right] = word;
    }
    write_answers(answers);
    switch_off_radio_button();
    check_answer_on_click(pos_right, answers);
}
