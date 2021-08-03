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


def get_json_obj(filename):
    return json.load(open(filename, 'r', encoding = 'utf-8'))
    
    
def parse_entry(entry):
    eng = nltk.word_tokenize(entry['examples'][0]['eng'])
    ru  = nltk.word_tokenize(entry['examples'][0]['ru'])
    eng_word_normalized = lemmatizer.lemmatize(entry['word'].lstrip().rstrip().lower())
    ru_word_normalized = morph.parse(entry['translation'].lstrip().rstrip().lower())[0].normal_form
    for word in eng:
        if lemmatizer.lemmatize(word) == eng_word_normalized:
            print(f"Word \"{word}\" found\nin \"{' '.join(eng)}\"\nin {eng.index(word)+1} position.")
            break
    else:
        print( f"ERROR: Word \"{entry['word']}\" not found\nin {' '.join(eng)}." )
    for word in ru:
        if morph.parse(word)[0].normal_form == ru_word_normalized:
            print(f"Translation \"{word}\" found\nin \"{' '.join(ru)}\"\nin {ru.index(word)+1} position.")
            break
    else:
        print(f"ERROR: Translation \"{entry['translation']}\" not found\nin {' '.join(ru)}.")
    print('\n\n  ')



def main():
    for entry in get_json_obj('words.json')['entries']:
        parse_entry(entry)

if __name__ == '__main__':
    main()


