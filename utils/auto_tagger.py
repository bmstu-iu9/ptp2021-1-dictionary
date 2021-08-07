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
        return f'String "{self.content}", language = "{self.language}"'

    

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
        self.length = len(self.content.split())
        self.content = self.content.lstrip().rstrip().lower()
        

    def __repr__(self):
        return f'Word "{self.content}", language = "{self.language}", len = {self.length}'

    def open_brackets(self):
        #меняет self.content на слово с раскрытыми скобками и возвращает новый объект своего класса с раскрытыми скобками
        #если скобок нет, возвращает None
        if '(' in self.content:
            newWord = Word(re.sub(r'\([^()]*\)', '', self.content), self.language)
            self.content = self.content.replace('(', '').replace(')', '')
            return newWord
        return None

    def get_normal_forms(self):
        self.change_similar_letters()
        if self.language == 'eng':
            normal_forms = tuple([lemmatizer.lemmatize(self.content, pos) for pos in (wordnet.NOUN,wordnet.VERB,wordnet.ADJ,wordnet.ADV)])
        elif self.language == 'ru':
            normal_forms = tuple([c.normal_form for c in morph.parse(self.content)])
        return normal_forms




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
            self.content = tuple([Word(c, self.language) for c in ngrammed_sentence])
            self.status = 'ngrammed'

    def njoin(self):
        self.content = ' '.join([c.content.split()[0] for c in self.content])






def parse_sentence(word, sentence, file):
    logs = []
    res = sentence.content
    sentence.nsplit(word.length)
    file.write('-- -- --ищем-- -- -- '+ word.content+'\n\n')
    file.write('возможные варианты: '+ str(word.get_normal_forms())+ '\n\n')
    for ngramm in sentence.content:
        file.write('рассматриваем '+ngramm.content)
        file.write('варианты для соответствия: '+str(ngramm.get_normal_forms())+ '\n\n')
        for element in ngramm.get_normal_forms():
            if element in word.get_normal_forms():
                file.write(f"Word \"{word.content}\" found\nin \"{res}\"\nin {sentence.content.index(ngramm)+1} position.\n")
                return True
        file.write('соответствий не найдено\n\n')
    return False
    







        

def parse_entry(entry, file, a):
    eng_sentence = Sentence(entry['examples'][0]['eng'], 'eng')
    ru_sentence  = Sentence(entry['examples'][0]['ru'], 'ru')

    word = Word(entry['word'], 'eng')

    translation = [Word(c, 'ru') for c in entry['translation'].lstrip().rstrip().split(',')]
    for i in range(len(translation[:])):
        translation += [translation[i].open_brackets()]
    translation = [c for c in translation if c != None]


    if not parse_sentence(word, eng_sentence, file):
        eng_sentence.njoin()
        file.write(f"-!-!-!-!-!-!-!-\n\nWord \"{word.content}\" not found\nin \"{eng_sentence.content}\"\n\n-!-!-!-!-!-!-!-\n\n\n")
        a[0]+=1
    for c in translation:
        if parse_sentence(c, ru_sentence, file):
            break
    else:
        ru_sentence.njoin()
        file.write(f"-!-!-!-!-!-!-!-\n\nWord \"{[c.content for c in translation]}\" not found\nin \"{ru_sentence.content}\"\n\n-!-!-!-!-!-!-!-\n\n\n")
        a[1]+=1
    return a
    



def main():
    file = open('logs.txt', 'w', encoding = 'utf-8')
    a = [0, 0]
    for entry in get_json_obj('words.json')['entries']:
        parse_entry(entry, file, a)
        
    file.close()
    print(f'Всего не найдено {a[0]} английских и {a[1]} русских слов')
    
    
    
    
        
    
        

if __name__ == '__main__':
    main()
