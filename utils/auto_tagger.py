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
import time


print('создание необходимых компонентов...')
lemmatizer = WordNetLemmatizer()
morph = pm.MorphAnalyzer()
print('загрузка успешно завершена!\n---------------------------\n\n')







def get_json_obj(filename):
    #возвращает json объект
    return json.load(open(filename, 'r', encoding = 'utf-8'))




class String:

    def __init__(self, content, language):
        self.content = content
        self.language = language
        

    def __repr__(self):
        return f'String "{self.content}", language = "{self.language}", {self.parse_functions}'

    def open_brackets(self):
        #меняет self.content на слово с раскрытыми скобками и возвращает новый объект своего класса с раскрытыми скобками
        #если скобок нет, возвращает None
        if '(' in self.content:
            newString = String(re.sub(r'\([^()]*\)', '', self.content), self.language) 
            self.content = [self.content.replace('(', '').replace(')', '')]
            return newString
        return None

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

    



class Word(String):

    def __init__(self, content, language):
        String.__init__(self, content, language)
        self.length = 1
        

    def __repr__(self):
        return f'Word "{self.content}", language = "{self.language}"'

    def get_normal_forms(self):
        self.change_similar_letters()
        if self.language == 'eng':
            parse_func = tuple([lemmatizer.lemmatize(self.content, pos) for pos in (wordnet.NOUN,wordnet.VERB,wordnet.ADJ,wordnet.ADV)])
        elif self.language == 'ru':
            parse_func = tuple([c.normal_form for c in morph.parse(self.content)])
        return parse_func




class Phrase(Word):

    def __init__(self, content, language, length):
        Word.__init__(self, content, language)
        self.length = length
        
    def __repr__(self):
        return f'Phrase "{self.content}", language = "{self.language}"'



class Sentence(String):

    def __init__(self, content, language):
        String.__init__(self, content, language)
        self.status = 'common'

    def nsplit(self, n = 1):
        #дробит строку на n-граммы
        if self.status == 'common': 
            content = nltk.word_tokenize(self.content)
            ngrammed_sentence = []
            ngramm = ''
            while len(content) >= n:
                for i in range(n):
                    ngramm = ngramm + content[i] + ' '
                ngrammed_sentence += [ngramm]
                ngramm = ''
                del content[0]
            ngrammed_sentence = list(map(lambda c: c.lstrip().rstrip().lower(), ngrammed_sentence))
            self.content = tuple([Word(c, self.language) if n == 1 else Phrase(c, self.language, n) for c in ngrammed_sentence])
            self.status = 'ngrammed'

    def njoin(self):
        pass








    

def phrase_check(string):
    return string.lstrip().rstrip().count(' ') > 0






def parse_sentence(word, sentence, file):
    global NLTK_WORDNET_POS_TAGS
    logs = []
    
    sentence.nsplit(word.length)
    

    for ngramm in sentence.content:
        for element in ngramm.get_normal_forms():
            if element in word.get_normal_forms():
                print(f'{word.content} found at \n{sentence.content}')
    






        

def parse_entry(entry, file):
    if phrase_check(entry['word']):
        word = Phrase(entry['word'], 'eng', len(entry['word'].split()))
    else:
        word = Word(entry['word'], 'eng')

    translations = [Phrase(c, 'ru', len(c.split())) if phrase_check(c) else Word(c, 'ru') for c in entry['translation'].split(',')]
    for i in range(len(translations)):
        translations += [translations[i].open_brackets()]

    translations = [c for c in translations if c != None]
    sentence_eng = Sentence(entry['examples'][0]['eng'], 'eng')
    sentence_ru  = Sentence(entry['examples'][0]['ru'], 'ru')

    parse_sentence(word, sentence_eng, file)
    for c in translations:
        parse_sentence(c, sentence_ru, file)



def main():
    file = open('logs.txt', 'w', encoding = 'utf-8')


    for entry in get_json_obj('words.json')['entries']:
        parse_entry(entry, file)
        
        

        
    file.close()
    
        

if __name__ == '__main__':
    main()
