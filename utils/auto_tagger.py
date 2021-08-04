print('загрузка библиотек...')
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
import pymorphy2 as pm
import tkinter as tk
from pprint import pprint
import json


print('создание необходимых компонентов...')
lemmatizer = WordNetLemmatizer()
morph = pm.MorphAnalyzer()
print('загрузка успешно завершена!\n---------------------------\n\n')


NLTK_WORDNET_TAGS = {
        
        }
##n 
##adv
##n
##prep
##a
##v
##phr
##adj
##n  
##n v

def my_ngramms():
    pass


def get_json_obj(filename):
    return json.load(open(filename, 'r', encoding = 'utf-8'))


def deal_with_brackets(translations):
    for t in translations[:]:
        if '(' in t:
            translations+=[t.replace('(', '').replace(')', '')]
    return translations
        

        
def parse_translation(translation):
    translations = list(map(lambda c: c.lstrip().rstrip().lower(), translation.split(',')))
    return translations
    
def format_str(string, lang):
    string = string.lower() #ключи -- англ, значения -- ру
    issues = {'a':'а','o':'о','c':'с','k':'к','x':'х','y':'у','h':'н','e':'е','b':'в','p':'р','m':'м'}
    if lang == 'ru':
        for letter in issues:
            string = string.replace(letter, issues[letter])
    elif lang == 'eng':
        for letter in issues:
            string = string.replace(issues[letter],letter)
    return string
    
def parse_entry(entry, file):    
    err_eng = 0
    err_ru = 0
    logs = []
    eng = [format_str(word, 'eng') for word in nltk.word_tokenize(entry['examples'][0]['eng'])]
    ru  = [format_str(word, 'ru') for word in nltk.word_tokenize(entry['examples'][0]['ru'])]
    eng_word_normalized = lemmatizer.lemmatize(format_str(entry['word'], 'eng').lstrip().rstrip().lower())
    ru_word_normalized = [format_str(morph.parse(c)[0].normal_form, 'ru') for c in deal_with_brackets(parse_translation(entry['translation']))]
    for word in eng:
        logs += [f'-----   {repr(lemmatizer.lemmatize(word))}, {repr(eng_word_normalized)}, {lemmatizer.lemmatize(word) == eng_word_normalized}   -----']
        if lemmatizer.lemmatize(word) == eng_word_normalized:
            file.write(f"Word \"{word}\" found\nin \"{' '.join(eng)}\"\nin {eng.index(word)+1} position.\n")
            break
    else:
        file.write( f"ERROR: Word \"{entry['word']}\" not found\nin {' '.join(eng)}.\n" )
        err_eng+=1
    for word in ru:
        for parse in morph.parse(word):
            if parse.normal_form in ru_word_normalized:
                file.write(f"Translation \"{word}\" found\nin \"{' '.join(ru)}\"\nin {ru.index(word)+1} position.\n")
                return (err_eng, err_ru)
            logs += [f'-----   {repr(parse.normal_form)}, {ru_word_normalized}, {parse.normal_form in ru_word_normalized}   -----']
    else:
        file.write(f"ERROR: Translation \"{entry['translation']}\" not found\nin {' '.join(ru)}.\n")
        err_ru+=1
    for c in logs:
        file.write(c)
        file.write('\n')
    
    return (err_eng, err_ru)



def main():
    total = [0, 0]
    file = open('logs.txt', 'w', encoding = 'utf-8')
    a = []
    for entry in get_json_obj('words.json')['entries']:
        if entry['pos'] not in a:
        cur = parse_entry(entry, file)
        total[0]+=cur[0]
        total[1]+=cur[1]
        file.write('\n- - - - - - - - - - - - - - - - -\n\n')
    file.close()
    print(f'всего ошибок:\nв английском {total[0]},\nв русском {total[1]}.')
        

if __name__ == '__main__':
    main()


