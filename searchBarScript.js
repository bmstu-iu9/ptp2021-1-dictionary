'use strict';

import words from "./words.json" assert { type: "json" }; /*now that's quite something*/




function searchMatchingElements(pattern){
  if (pattern == '') {
    console.log('функция searchMatchingElements сработала выдав пустой список');
    return [];
  }
  let arrOfMatches = [];
  words.entries.forEach(element => {
    if(RegExp("^"+pattern, "i").test(element.word)){
      arrOfMatches.push(element.word);
  }
  });
  console.log('функция searchMatchingElements сработала');
  return arrOfMatches;
}


function clearPreviouslySuggestedElements(){
  let mySuggestions = document.getElementById("mySuggestions"); 
  let previouslySuggestedElements = mySuggestions.childNodes;
  for (; previouslySuggestedElements.length > 0 ;) {
    mySuggestions.removeChild(previouslySuggestedElements[0]);
  }
  console.log('функция clear сработала');
}


function suggestElements(arrOfMatches){
  clearPreviouslySuggestedElements();
  let mySuggestions = document.getElementById("mySuggestions"); 
    arrOfMatches.forEach(element => {
      let myLink = document.createElement("a");
      myLink.innerHTML = element;
      myLink.href = "#";
      let myBreak = document.createElement("br");      
      mySuggestions.appendChild(myLink);
      mySuggestions.appendChild(myBreak);
    });
    console.log('функция suggestElements сработала');
}


function getMyInputValue(){
  let myInput = document.getElementById("myInput");
  let myValue = myInput.value;
  console.log(myValue);
  console.log('функция getValue сработала');
  return myValue;
}


function myAction(){
  suggestElements(searchMatchingElements(getMyInputValue()));
  console.log('функция myAction сработала');
}



document.getElementById('myInput').onkeyup = myAction;