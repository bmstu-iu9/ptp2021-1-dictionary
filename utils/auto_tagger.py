print('загрузка библиотек...')
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
import pymorphy2 as pm
import tkinter as tk
import re
from pprint import pprint
from string import punctuation
import json


print('создание необходимых компонентов...')
lemmatizer = WordNetLemmatizer()
morph = pm.MorphAnalyzer()
print('загрузка успешно завершена!\n---------------------------\n\n')


NLTK_WORDNET_POS_TAGS = (
    wordnet.NOUN,
    wordnet.VERB,
    wordnet.ADJ,
    wordnet.ADV
    )




def get_json_obj(filename):
    #возвращает json объект
    return json.load(open(filename, 'r', encoding = 'utf-8'))




class String:

    def __init__(self, content, language):
        self.content = content
        self.language = language
        if self.language == 'eng':
            self.parse_func = 'lemmatizer.lemmatize(SELF, POS)'
        elif self.language == 'ru':
            self.parse_func = 'morph.parse(SELF)'

    def __repr__(self):
        return f'String "{self.content}", language = "{self.language}", {self.parse_functions}'

    def open_brackets(self):
        #меняет self.content на слово с раскрытыми скобками и возвращает новый объект своего класса с раскрытыми скобками
        #если скобок нет, возвращает None
        if '(' in self.content:
            newString = String(re.sub(r'\([^()]*\)', '', self.content), self.language) 
            self.content = [current.replace('(', '').replace(')', '')]
        return newString 

    def change_similar_letters(self):
        #меняет английские буквы в строке на похожие русские в зависимости от выбранного языка
        string = self.content.lower() #ключи -- англ, значения -- ру
        issues = {'a':'а','o':'о','c':'с','k':'к','x':'х','y':'у','h':'н','e':'е','b':'в','p':'р','m':'м'}
        if self.language == 'ru':
            for letter in issues:
                string = string.replace(letter, issues[letter])
        elif self.language == 'eng':
            for letter in issues:
                string = string.replace(issues[letter],letter)
        self.content = string

    
        

    
class Sentence(String):
    def __init__(self, content, language):
        String.__init__(self, content, language)

    def nsplit(self, n = 1):
        #дробит строку на n-граммы
        content = nltk.word_tokenize(string)
        ngrammed = []
        ngramm = ''
        while len(content) >= n:
            for i in range(n):
                ngramm = ngramm + string[i] + ' '
            ngrammed_sentence += [ngramm]
            ngramm = ''
            del content[0]
        self.content = list(map(lambda c: c.lstrip().rstrip().lower(), content))




class Word(String):

    def __init__(self, content, language):
        String.__init__(self, content, language)
        self.length = 1

    def __repr__(self):
        return f'Word "{self.content}", language = "{self.language}"'




class Phrase(String):

    def __init__(self, content, language, length):
        String.__init__(self, content, language)
        self.length = length
        
    def __repr__(self):
        return f'Phrase "{self.content}", language = "{self.language}"'

    

def phrase_check(string):
    return string.lstrip().rstrip().count(' ') > 0






def parse(word, sentence, file):
    if word.language == 'eng':
        global NLTK_WORDNET_POS_TAGS
    logs = []
    sentence.nsplit(word.length)
    pass




def parse_entry_eng(entry, file):
    global NLTK_WORDNET_POS_TAGS
    logs = []
    eng = [format_str(word, 'eng') for word in nltk.word_tokenize(entry['examples'][0]['eng'])]    
    eng_word_normalized = lemmatizer.lemmatize(format_str(entry['word'], 'eng').lstrip().rstrip().lower(), entry['pos'].rstrip()[0])
    for word in eng:
        logs += [f'-----   {repr(lemmatizer.lemmatize(word))}, {repr(eng_word_normalized)}, {lemmatizer.lemmatize(word) == eng_word_normalized}   -----']
        for tag in NLTK_WORDNET_POS_TAGS:
            if lemmatizer.lemmatize(word, tag) == eng_word_normalized:
                file.write(f"Word \"{word}\" found\nin \"{' '.join(eng)}\"\nin {eng.index(word)+1} position.\n")
                return 0
    else:
        file.write( f"ERROR: Word \"{entry['word']}\" not found\nin {' '.join(eng)}.\n" )
    for c in logs:
        file.write(c)
        file.write('\n')
    return 1

        








def main():
    file = open('logs.txt', 'w', encoding = 'utf-8')


    for entry in get_json_obj('words.json')['entries']:
        if phrase_check(entry['word']):
            word = Phrase(entry['word'], 'eng', len(entry['word'].split()))
        else:
            word = Word(entry['word'], 'eng')
        translations = [Phrase(c, 'ru', len(c.split())) if phrase_check(c) else Word(c, 'ru') for c in entry['translation'].split(',')]
        for i in range(len(translations)):
            translations += c.open_brackets()
        sentence_eng = Sentence(entry['examples'][0]['eng'])
        sentence_ru  = Sentence(entry['examples'][0]['ru'])

        parse(word, sentence_eng, file)
        for c in translations:
            parse(c, sentence_ru, file)


        
    file.close()
    
        

if __name__ == '__main__':
    main()
