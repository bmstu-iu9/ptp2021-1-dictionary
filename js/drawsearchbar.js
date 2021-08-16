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
  words.forEach(element => {
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
	  let index = words.findIndex(obj => obj.word==element);
	  myLink.href = "/ptp2021-1-dictionary/pages/wordpage.html?wordnumber=" + index;
	  //myLink.href = "pages/wordpage.html?wordnumber=" + index;
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

var xhr = new XMLHttpRequest();
xhr.onreadystatechange = process;
url = document.location.origin + "/ptp2021-1-dictionary/include/stroka.html";
//url = document.location.origin + "/include/stroka.html";
//alert(url);
xhr.open("GET", url, true);
xhr.send();
function process()
{
  if (xhr.readyState == 4) {
    var resp = xhr.responseText;
    let div=document.createElement('div');
    div.innerHTML=resp.toString();
    document.body.prepend(div);
    document.getElementById('content').style.display='';
    document.getElementById('myInput').onkeyup = myAction;
  }
}
