
print('загрузка библиотек...')
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet

import pymorphy2 as pm
import re
import json
import time
import itertools
import Levenshtein 





print('создание необходимых компонентов...')
lemmatizer = WordNetLemmatizer()
porter = PorterStemmer()
snowball = SnowballStemmer('russian')

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
        #возвращает список лемм слова
        self.change_similar_letters()
        if self.language == 'eng':
            normal_forms = [' '.join([lemmatizer.lemmatize(w, pos) for w in self.content.split()]) for pos in (wordnet.NOUN,wordnet.VERB,wordnet.ADJ,wordnet.ADV)]
        elif self.language == 'ru':
            raw_forms = [[parse.normal_form for parse in morph.parse(word)] for word in self.content.split()]
            normal_forms = raw_forms[0]
            del raw_forms[0]
            while raw_forms:
                cur = normal_forms[:]
                normal_forms = []
                for f in raw_forms[0]:
                    for c in cur:
                        normal_forms += [c+' '+f]
                del raw_forms[0]
        return tuple(set(normal_forms))




class Sentence(String):

    def __init__(self, content, language):
        String.__init__(self, content, language)
        self.res = None

    def nsplit(self, n = 1):
        #дробит строку на n-граммы
        if not self.res:
            self.res = self.content
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

    def njoin(self):
        self.content = self.res
        self.res = None

    def tag_content(self, word2tag):
        pass
        

    def __repr__(self):
        return f'Sentence "{self.content}",\n language = "{self.language}",\n len = {self.length},\nngrammed = {bool(self.res)}'






def parse_sentence(word, sentence, file):
    #ведет поиск сначала по леммам, потом по расстоянию Левенштейна
    res = sentence.content
    sentence.nsplit(word.length)

    word_normalized = word.get_normal_forms()

    for ngramm in sentence.content:
        for element in ngramm.get_normal_forms():
            if element in word_normalized:
                sentence.njoin()
                sentence.content = sentence.content.replace(ngramm.content, r'<<b>'+ngramm.content+r'<d>>')
                sentence.content = sentence.content.replace(ngramm.content.capitalize(), r'<<b>'+ngramm.content.capitalize()+r'<d>>')
                if '<<b>' not in sentence.content:
                    file.write('\n~~~~~~~~~~~~~~~~~~~~\nFOUND WHILE PARSING, BUT NOT AT RAW SENTENCE:\n')
                    file.write(ngramm.content+ ' not found at "' +sentence.content+'"\n~~~~~~~~~~~~~~~~~~~~\n\n')
                return sentence.content

    for ngramm in sentence.content:
        for ng in ngramm.get_normal_forms():
            for w in word_normalized:
                if  Levenshtein.distance(ng, w) < 3:
                    sentence.njoin()
                    sentence.content = sentence.content.replace(ngramm.content, r'<<b>'+ngramm.content+r'<d>>')
                    sentence.content = sentence.content.replace(ngramm.content.capitalize(), r'<<b>'+ngramm.content.capitalize()+r'<d>>')
                    if '<<b>' not in sentence.content:
                        file.write('\n~~~~~~~~~~~~~~~~~~~~\nFOUND WHILE PARSING, BUT NOT AT RAW SENTENCE:\n')
                        file.write(ngramm.content+ ' not found at "' +sentence.content+'"\n~~~~~~~~~~~~~~~~~~~~\n\n')
                    file.write(f'\n- - - - -\nLEVENSHTEIN: "{word.content}" найдено как "{ng}"\n- - - - -\n')
                    return sentence.content
                
    return False
    



        

def parse_entry(entry, file, a):
    #парсит словарную статью
    eng_sentence = Sentence(entry['examples'][0]['eng'], 'eng')
    ru_sentence  = Sentence(entry['examples'][0]['ru'], 'ru')

    word = Word(entry['word'], 'eng')

    translation = [Word(c, 'ru') for c in entry['translation'].lstrip().rstrip().split(',')]

    new_examples = {'eng':entry['examples'][0]['eng'],'ru':entry['examples'][0]['ru']}
    
    for i in range(len(translation[:])):
        translation += [translation[i].open_brackets()]
    translation = [c for c in translation if c != None]

    eng_result_of_parse = parse_sentence(word, eng_sentence, file)
    if not eng_result_of_parse:
        file.write(f'{word.get_normal_forms()}\nnot found at\n"{" ".join([c.content for c in eng_sentence.content])}"\n\n')
        a[0]+=1
    else:
        new_examples['eng'] = eng_result_of_parse

        
    for c in translation:
        ru_result_of_parse = parse_sentence(c, ru_sentence, file)
        if ru_result_of_parse:
            new_examples['ru'] = ru_result_of_parse
            break
    else:
        ru_sentence.njoin()
        file.write(f'{[t.get_normal_forms() for t in translation]}\nnot found at\n"{ru_sentence.content}"\n\n')
        a[1]+=1
    return (new_examples, a)
    



def main():
    start = time.time()
    file = open(f'autotagger_logs.txt', 'w', encoding = 'utf-8')
    tagged_file = open('tagged_words.txt', 'w', encoding = 'utf-8')
    a = [0, 0]
    for entry in get_json_obj('words.json')['entries']:
        res_of_parse = parse_entry(entry, file, a)
        a = res_of_parse[1]
        tagged_file.write(entry['word']+'\n'+entry['translation']+'\n'+entry['transcription']+'\n'+entry['pos']+'\n'+
                          res_of_parse[0]['eng']+'\n'+res_of_parse[0]['ru']+'\n\n')
        
    file.close()
    tagged_file.close()
    print(f'Всего не найдено {a[0]} английских и {a[1]} русских слов')
    print(f'затрачено {time.time()-start} сек на работу алгоритма')

    
    
    

        
        
        
    
        

if __name__ == '__main__':
    main()

