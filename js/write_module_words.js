function write_module_words(n) {
    let card = document.querySelector(".card");
    let card_head = document.createElement("div");
    card_head.innerHTML = "Module " + n;
    card_head.className = "card-header";
    card_head.classList.add("text-center");
    card.appendChild(card_head);
    let card_body = document.createElement("div");
    card_body.className = "card-body";
    card.appendChild(card_body);
    for (let i = 0; i < words.length; i++) {
        if (words[i].module == n) {
            let word_translation = document.createElement("a");
            word_translation.href = "#";
            word_translation.innerHTML =  words[i].word[0].toUpperCase() +  words[i].word.slice(1) + " - " + words[i].translation;
            word_translation.className = "word-link";
            card_body.appendChild(word_translation);
            let br = document.createElement("br");
            card_body.appendChild(br);
        }
    }
}

write_module_words(11);