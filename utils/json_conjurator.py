import tkinter as tk







def action(filename, module_number):
    file = open(filename, 'r', encoding = 'utf-8').readlines()
    new = []
    for c in file:
        new+=[c.lstrip()]

    formated = []
    s = []
    for c in new:
        if c == '':
            formated+= [s]
            s = []
        else:
            s+=[c]



    x = '{'
    y = '}'

    def brackets(s):
        return '"'+s[:-1]+'"'


    print('{"entries":[')

    for c in formated:
        if c:
            print(
            f'''{x}
                "word": {brackets(c[0])},
                "translation": {brackets(c[1])},
                "transcription": {brackets(c[2])},
                "pos": {brackets(c[3])},
                "examples": [{x}
                        "eng": {brackets(c[4])},
                        "ru": {brackets(c[5])}
                {y}],
                "module": {module_number}
            {y},'''
                )
    print(']}')

root = tk.Tk()
root.title('json conjurator')
root.resizable(False, False)

lbl1 = tk.Label(text = 'файл на чтение', font = ('Arial', 18))

ent1 = tk.Entry(width = 25, font = ('Arial', 18))

lbl2 = tk.Label(text = 'номер модуля', font = ('Arial', 18))

ent2 = tk.Entry(width = 25, font = ('Arial', 18))

btn = tk.Button(text = 'OK', font = ('Arial', 18),
                command = lambda: action(ent1.get(), int(ent2.get())))

for c in (lbl1, ent1, lbl2, ent2, btn):
    c.pack()

root.mainloop()









