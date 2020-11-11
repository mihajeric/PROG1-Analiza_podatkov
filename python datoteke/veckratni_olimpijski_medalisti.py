import requests
import csv

url = "https://en.wikipedia.org/wiki/List_of_multiple_Olympic_medalists"

response = requests.get(url)
text = response.text

for i in range(0): # odreže stran vse do konca prve tabele, ker hočem drugo
    endOfTable = text.find("</tbody>")
    text = text[endOfTable + 8:]

# Poišče začetek in konec tabele
startOfTable = text.find("<tbody>")
endOfTable = text.find("</tbody>")
tabelaHtml = text[startOfTable:endOfTable]



tabela = []

# Poišče začetek prve vrstice tabele
start = tabelaHtml.find("<tr")
while start >= 0:
    # Poišče konec prve vrstice in jo shrani v spr.
    end = tabelaHtml.find("</tr>")
    vrsticaHtml = tabelaHtml[start:end]
    
    # Odreže začetek prve vrstice, da bo naslednjič kot prvo našel naslednjo
    tabelaHtml = tabelaHtml[end + 5:]
    
    vrstica = []
    for j in range(11):
        # Poišče začetek naslednjega elementa vrstice <td>
        vrsticaHtml = vrsticaHtml[vrsticaHtml.find("<td"):]
        # Odreže <td ... >, da ostane le notranjost + naslednji elementi
        vrsticaHtml = vrsticaHtml[vrsticaHtml.find(">") + 1:]
        # Poišče konec elementa
        end = vrsticaHtml.find("</td>")
        # shrani vsebino od trenutnega začetka vrstice do konca elementa v elementHtml
        elementHtml = vrsticaHtml[:end]

        if elementHtml.find('<a href') >= 0: # pri prvem elementu mora dobiti tekst znotraj linka
            elementHtml = elementHtml[elementHtml.find("<a href"):]
            elementHtml = elementHtml[elementHtml.find(">") + 1 : elementHtml.find("</a>")]
            # ^ Obdrži le vsebino linka
            
            if elementHtml.find("<") >= 0: # nekonsistentno fomratiranje v wikipediji
                elementHtml = "North Macedonia"
            
        vrstica.append(elementHtml.strip())
    tabela.append(vrstica)
    
    # Poišče začetek naslednje vrstice
    start = tabelaHtml.find("<tr")
    

    
tabela = tabela[1:] # zadnja vrstica je prazna, prvi dve tudi
print(tabela)


# shrani v csv
with open("veckratni_olimpijski_medalisti.csv", "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(tabela)
