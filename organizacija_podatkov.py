import pandas as pd
import os

if not os.path.exists('./csv_reorganizirane'):
    os.mkdir('./csv_reorganizirane')


# doda imena stolpcev in shrani kopije

brez = pd.read_csv('./csv datoteke/drzave_brez_medalj.csv', names=['drzava', 'udelezbe_poletne', 'udelezbe_zimske', 'udelezbe_skupaj'])
brez.to_csv('./csv_reorganizirane/drzave_brez_medalj.csv')

cols = ['drzava']
for varianta in ['poletne', 'zimske', 'skupaj']:
    for e in ['udelezbe', 'zlate', 'srebrne', 'bronaste', 'vse']:
        cols.append(e + '_' + varianta)
medalje = pd.read_csv('./csv datoteke/skupno_stevilo_medalj.csv', names=cols, thousands=',')
medalje.to_csv('./csv_reorganizirane/skupno_stevilo_medalj.csv')


# odstrani prazne vrstice

udelezbe = pd.read_csv('./csv datoteke/stevilo_udelezb_drzav_OI.csv', names=['drzava', 'udelezbe_poletne'])
udelezbe = udelezbe[udelezbe.udelezbe_poletne != -1]
udelezbe.to_csv('./csv_reorganizirane/stevilo_udelezb_drzav_OI.csv')

udelezbe = pd.read_csv('./csv datoteke/stevilo_udelezb_drzav_ZOI.csv', names=['drzava', 'udelezbe_zimske'])
udelezbe = udelezbe[udelezbe.udelezbe_zimske != -1]
udelezbe.to_csv('./csv_reorganizirane/stevilo_udelezb_drzav_ZOI.csv')


# ustrezno zamakne atlete, ki si delijo mesto
medalisti = pd.read_csv('./csv datoteke/veckratni_olimpijski_medalisti.csv', names=['rank', 'atlet', 'drzava', 'sport', 'leta', 'igre', 'spol', 'zlate', 'srebrne', 'bronaste', 'skupaj_medalj'])

rows = medalisti.values.tolist()
prev_i = 0
for row in rows:
    if not row[0].isnumeric():
        row.insert(0, prev_i)
        row.pop()
    prev_i = row[0]
    
medalisti = pd.DataFrame(rows, columns=['rank', 'atlet', 'drzava', 'sport', 'leta', 'igre', 'spol', 'zlate', 'srebrne', 'bronaste', 'skupaj_medalj'])
medalisti.zlate = medalisti.zlate.astype('int32')
medalisti.srebrne = medalisti.srebrne.astype('int32')
medalisti.bronaste = medalisti.bronaste.astype('int32')
medalisti = medalisti.drop(labels='skupaj_medalj', axis=1)
medalisti.to_csv('./csv_reorganizirane/veckratni_olimpijski_medalisti.csv')
