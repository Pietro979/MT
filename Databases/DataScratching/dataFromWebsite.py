# This is a script used for downloading data from internet.

from urllib.request import urlopen

url = "https://www.nbp.pl/home.aspx?f=/kursy/kursya.html"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

print(html)

# EURO
euro_start_index = html.find('1 EUR') + len('1 EUR') + len('</td> <td class="bgt2 right">')
cena_euro = html[euro_start_index:(euro_start_index+6)]

# DOLAR AMERYKANSKI
dolar_start_index = html.find('1 USD') + len('1 USD') + len('</td> <td class="bgt2 right">')
cena_dolar = html[dolar_start_index:(dolar_start_index+6)]

# HRYWNA UKRAINSKA
hrywna_start_index = html.find('1 UAH') + len('1 UAH') + len('</td> <td class="bgt2 right">')
cena_hrywna = html[hrywna_start_index:(hrywna_start_index+6)]

# LIRA TURECKA
lira_start_index = html.find('1 TRY') + len('1 TRY') + len('</td> <td class="bgt2 right">')
cena_lira = html[lira_start_index:(lira_start_index+6)]

cena_lira = cena_lira.replace(',', '.')
cena_euro = cena_euro.replace(',', '.')
cena_hrywna = cena_hrywna.replace(',', '.')
cena_dolar = cena_dolar.replace(',', '.')

float(cena_lira)
float(cena_euro)
float(cena_hrywna)
float(cena_dolar)

print('Cena 1 Euro: ' + cena_euro)
print('Cena 1 Dolar: ' + cena_dolar)
print('Cena 1 Hrywna: ' + cena_hrywna)
print('Cena 1 Lira: ' + cena_lira)