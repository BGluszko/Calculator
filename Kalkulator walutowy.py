import requests
import xmltodict
from tkinter import *
import tkinter.ttk as ttk
import sys

respond = requests.get("https://www.nbp.pl/kursy/xml/LastA.xml")

if respond.status_code != 200:  # w przypadku błędu przy pobieraniu ze strony
    f = open('kursy_walut.txt', 'r')  # pobieramy dane z zapisanego wcześniej pliku tekstowego
    r = f.read()
    f.close()
    curr_dict = xmltodict.parse(r)

else:
    curr_xml = respond.content
    with open('kursy_walut.txt', 'wb') as f:  # tworzymy nowy plik z nowymi danymi
        f.write(curr_xml)
        f.close()
    curr_dict = xmltodict.parse(curr_xml)  # zamieniamy na słownik

lista = dict(dict(curr_dict)['tabela_kursow'])['pozycja']

dicts = [{'nazwa_waluty': 'złoty',  # dodajemy PLN żeby później było łatwiej
             'przelicznik': '1',
             'kod_waluty': 'PLN',
             'kurs_sredni': '1,0000'}]
for i in range(len(lista)):
    dicts.append(dict(lista[i]))  # zamieniamy OrderedDict na zwykły dict i tworzymy listę słowników

przeliczniki = []
for i in range(len(dicts)):
    przeliczniki.append(dicts[i]['przelicznik'])

kody = []
for i in range(len(dicts)):
    kody.append(dicts[i]['kod_waluty'])

kursy = []
for i in range(len(dicts)):
    kursy.append(dicts[i]['kurs_sredni'].replace(",", "."))


def count():
    try:
        kwota = float(entry.get())
        kod1 = combobox1.get()
        kod2 = combobox2.get()

        if kod1 == kod2:
            label.config(text=kwota)

        else:
            for i in range(len(kody)):
                if kody[i] == kod1:
                    indeks1 = i
            kurs1 = float(kursy[indeks1])
            przelicznik1 = float(przeliczniki[indeks1])

            for n in range(len(kody)):
                if kody[n] == kod2:
                    indeks2 = n
            kurs2 = float(kursy[indeks2])
            przelicznik2 = float(przeliczniki[indeks2])

            pln = (kwota * kurs1) / przelicznik1
            wynik1 = (przelicznik2 * pln) / kurs2
            wynik2 = round(wynik1, 2)
            label.config(text=wynik2)

    except:
        label.config(text = "Podana kwota nie jest liczbą!")


def quit():
    sys.exit()

root = Tk()
root.geometry('500x400')
topFrame = Frame(root)
bottomFrame = Frame(root)
root.title("Walutomierz")

Button(root, text="Count",command=count,height=4,width=7,bg="black",fg="white").place(x=100,y=200)
Button(root, text="Quit",command=quit,height=4,width=7,bg="black",fg="white").place(x=300,y=200)
Label(root, text="Kwota").place(x=40,y=90)
entry=Entry(root)
entry.pack()
entry.place(x=120,y=90)
Label(root, text="Waluta źródłowa: ").place(x=10,y=10)
combobox1 = ttk.Combobox(root)
combobox1['values'] = kody
combobox1.current(0)
combobox1.place(x=120,y=10)
Label(root, text="Waluta docelowa: ").place(x=10,y=50)
combobox2 = ttk.Combobox(root)
combobox2['values'] = kody
combobox2.current(0)
combobox2.place(x=120,y=50)
label=Label(root, text=" ")
label.pack()
label.place(x=120,y=130)
Label(root, text="Wynik").place(x=40,y=130)
root.mainloop()