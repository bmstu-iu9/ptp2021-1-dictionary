var i = 0;
var j = 0;
//document.write('<tr>');
for (i in words) {
    document.write('<td><a href="pages/wordpage.html?wordnumber=' + i + '" title="Показать информацию об этом слове">' + words[i].word + ' (' + words[i].pos + ')</a></td>');
}
//document.write('</tr');

