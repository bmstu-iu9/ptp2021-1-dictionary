var xhr = new XMLHttpRequest();
xhr.onreadystatechange = process;
url = document.location.origin + "/include/stroka.html";
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
  }
}

