import words from "../json/words.json" assert { type: "json" };

document.getElementById("flipper").onclick = function() {
    document.getElementById("flipper").classList.toggle("flip")
}