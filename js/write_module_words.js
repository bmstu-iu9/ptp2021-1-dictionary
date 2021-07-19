function write_module_words(n) {
    let card_head = document.querySelector(".card-header");
    let card_body = document.querySelector(".card-body");
    card_head.innerHTML = "Module " + n;
    for (let i = 0; i < words.length; i++) {
        if (words[i].module == n) {
            let word_translation = document.createElement("a");
            word_translation.href = "wordpage.html?wordnumber=" + i;
            word_translation.innerHTML =  words[i].word[0].toUpperCase() +  words[i].word.slice(1) + " - " + words[i].translation;
            word_translation.className = "word-link";
            card_body.appendChild(word_translation);
            let br = document.createElement("br");
            card_body.appendChild(br);
        }
    }
}

write_module_words(11);