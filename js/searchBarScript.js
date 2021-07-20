'use strict';

import words from "../json/words.json" assert { type: "json" }; /*now that's quite something*/



//  функция searchMatchingElements.
//  если pattern -- пустая строка, возвращает пустой массив.
//  иначе ищет строгие соответствия в массиве words при помощи регулярного выражения.
//  не чувствительна к регистру (флаг i в регулярном выражении).
//  возвращает массив совпадений.
//  оптимизировать еще больше не стану тк в объекте в 2000 слов показывает скорость менее милисекунды.
//  нам этого более чем достаточно.

function searchMatchingElements(pattern){
  if (pattern == '') {
    return [];
  }
  let arrOfMatches = [];
  words.entries.forEach(element => {
    if(RegExp("^"+pattern, "i").test(element.word)){
      arrOfMatches.push(element.word);
  }
  });
  return arrOfMatches;
}

//  функция clearPreviouslySuggestedElements.
//  очищает div "mySuggestions" от всех элементов

function clearPreviouslySuggestedElements(){
  let mySuggestions = document.getElementById("mySuggestions"); 
  let previouslySuggestedElements = mySuggestions.childNodes;
  for (; previouslySuggestedElements.length > 0 ;) {
    mySuggestions.removeChild(previouslySuggestedElements[0]);
  }
}

//  функция suggestElements.
//  заполняет div "mySuggestions" ссылками на словарные статьи.

function suggestElements(arrOfMatches){
  clearPreviouslySuggestedElements();
  let mySuggestions = document.getElementById("mySuggestions"); 
    arrOfMatches.forEach(element => {
      let myLink = document.createElement("a");
      myLink.innerHTML = element;
      myLink.href = "#";
      myLink.style = "margin: 1%;";     
      mySuggestions.appendChild(myLink);
    });
}

//  функция getMyInputValue.
//  достает то, что записано в  поисковой строке.

function getMyInputValue(){
  let myInput = document.getElementById("myInput");
  let myValue = myInput.value;
  return myValue;
}

//  функция myAction.
//  нудна для обработки события нажатия на кнопку.

function myAction(){ 
  suggestElements(searchMatchingElements(getMyInputValue()));  
}



document.getElementById('myInput').onkeyup = myAction;