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


NLTK_WORDNET_POS_TAGS = (
    wordnet.NOUN,
    wordnet.VERB,
    wordnet.ADJ,
    wordnet.ADV
    )



def my_ngramm(string, n):
    string = nltk.word_tokenize(string)
    ngrammed_sentence = []
    ngramm = ''
    while len(string) >= n:
        for i in range(n):
            ngramm = ngramm + string[i] + ' '
        ngrammed_sentence += [ngramm.rstrip()]
        ngramm = ''
        del string[0]
    return ngrammed_sentence


def get_json_obj(filename):
    return json.load(open(filename, 'r', encoding = 'utf-8'))


def deal_with_brackets(translations):
    for i in range(len(translations)):
        current = translations[i]
        if '(' in current:
            translations[i] = re.sub(r'\([^()]*\)', '', current)
            translations+=[current.replace('(', '').replace(')', '')]
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



def parse_entry_ru(entry, file):
    logs = []
    ru  = [format_str(word, 'ru') for word in nltk.word_tokenize(entry['examples'][0]['ru'])]
    ru_word_normalized = [format_str(morph.parse(c)[0].normal_form, 'ru') for c in deal_with_brackets(parse_translation(entry['translation']))]
    for word in ru:
        for parse in morph.parse(word):
            logs += [f'-----   {repr(parse.normal_form)}, {ru_word_normalized}, {parse.normal_form in ru_word_normalized}   -----']
            if parse.normal_form in ru_word_normalized:
                file.write(f"Translation \"{word}\" found\nin \"{' '.join(ru)}\"\nin {ru.index(word)+1} position.\n")
                return 0
            
    else:
        file.write(f"ERROR: Translation \"{entry['translation']}\" not found\nin {' '.join(ru)}.\n")
    for c in logs:
        file.write(c)
        file.write('\n')
    return 1




def main():
    total = [0, 0]
    file = open('logs.txt', 'w', encoding = 'utf-8')
    a = []
    for entry in get_json_obj('words.json')['entries']:
        try:
            total[0]+=parse_entry_eng(entry, file)
            total[1]+=parse_entry_ru(entry, file)
        except Exception:
            file.write(f'WORDNET ERROR: tag {entry["pos"][0]}({entry["pos"]}) not found.')
        file.write('\n- - - - - - - - - - - - - - - - -\n\n')
    file.close()
    print(f'всего ошибок:\nв английском {total[0]},\nв русском {total[1]}.')
        

if __name__ == '__main__':
    main()


