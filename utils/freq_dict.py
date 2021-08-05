print('загрузка библиотек...')
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
import tkinter as tk
print('загрузка успешно завершена!')


lemmatizer = WordNetLemmatizer()


def format_text(text):
    ru = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    text = text.lower()
    for c in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~●'+ru+ru.upper():
        text = text.replace(c, '')
    text = nltk.sent_tokenize(text)
    return text

def freq_words(text):
    d = {}
    text = format_text(text)
    for sentence in text:
        sentence = nltk.word_tokenize(sentence)
        for word in sentence:
            word = lemmatizer.lemmatize(word)
            if word not in d:
                d[word] = 1
            else:
                d[word]+=1
    return d

def freq_dict(text):
    dictionary= {}
    phrase = []
    text = format_text(text)
    for sentence in text:
        sentence = nltk.pos_tag(nltk.word_tokenize(sentence))
        for word in sentence:
            if word[1]  in ('RB','RBR','RBS','POS',
                            'JJ', 'JJR', 'JJS', 'NN',
                            'NNS', 'NNP', 'NNPS', 'PDT'):
                phrase+=[word[0]]
            else:
                phrase = ' '.join(phrase)
                try:
                    dictionary[phrase] += 1
                except KeyError:
                    dictionary[phrase] = 1
                try:
                    dictionary[word[0]] += 1
                except KeyError:
                    dictionary[word[0]] = 1
                phrase = []                
    return dictionary


def dsort(freq):
    values = sorted(freq.values())
    new = {}
    for value in values:
        for key in freq.keys():
            if freq[key] == value:
                new[key] = freq[key]
    return new

def fill_file(filename, freq_type, freq):
    filename = f'({freq_type}) {filename}'
    file = open(filename, 'w', encoding = 'utf-8')
    for key in freq:
        if key:
            file.write(key+' -- '+str(freq[key])+'\n')
    file.close()
    print(f'файл {filename} успешно записан!')

def write_dicts(filename):
    file = open(filename, 'r', encoding = 'utf-8').read()            
    phrases = dsort(freq_dict(file))
    words = dsort(freq_words(file))
    fill_file(filename, 'phrases', phrases)
    fill_file(filename, 'words', words)



root = tk.Tk()
root.title('freq')
root.resizable(False, False)

lbl1 = tk.Label(text = 'файл на чтение', font = ('Arial', 18))

ent1 = tk.Entry(width = 25, font = ('Arial', 18))

btn = tk.Button(text = 'OK', font = ('Arial', 18),
                command = lambda: write_dicts(ent1.get()))

for c in (lbl1, ent1, btn):
    c.pack()

root.mainloop()


##                        Abbreviation	Meaning
##                        CC	coordinating conjunction
##                        CD	cardinal digit
##                        DT	determiner
##                        EX	existential there
##                        FW	foreign word
##                        IN	preposition/subordinating conjunction
##                        JJ	This NLTK POS Tag is an adjective (large)
##                        JJR	adjective, comparative (larger)
##                        JJS	adjective, superlative (largest)
##                        LS	list market
##                        MD	modal (could, will)
##                        NN	noun, singular (cat, tree)
##                        NNS	noun plural (desks)
##                        NNP	proper noun, singular (sarah)
##                        NNPS	proper noun, plural (indians or americans)
##                        PDT	predeterminer (all, both, half)
##                        POS	possessive ending (parent\ 's)
##                        PRP	personal pronoun (hers, herself, him,himself)
##                        PRP$	possessive pronoun (her, his, mine, my, our )
##                        RB	adverb (occasionally, swiftly)
##                        RBR	adverb, comparative (greater)
##                        RBS	adverb, superlative (biggest)
##                        RP	particle (about)
##                        TO	infinite marker (to)
##                        UH	interjection (goodbye)
##                        VB	verb (ask)
##                        VBG	verb gerund (judging)
##                        VBD	verb past tense (pleaded)
##                        VBN	verb past participle (reunified)
##                        VBP	verb, present tense not 3rd person singular(wrap)
##                        VBZ	verb, present tense with 3rd person singular (bases)
##                        WDT	wh-determiner (that, what)
##                        WP	wh- pronoun (who)
##                        WRB	wh- adverb (how)



























