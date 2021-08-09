var i = 0;
var j = "z";
//document.write('<tr>');
for (i in words) {
	if (j != words[i].word[0]) {
		j = words[i].word[0];
		document.write('<td><a name="' + j + '" href="pages/wordpage.html?wordnumber=' + i + '" title="Показать информацию об этом слове">' + words[i].word + ' (' + words[i].pos + ')</a></td>');
	}
    document.write('<td><a href="pages/wordpage.html?wordnumber=' + i + '" title="Показать информацию об этом слове">' + words[i].word + ' (' + words[i].pos + ')</a></td>');
}
//document.write('</tr');

