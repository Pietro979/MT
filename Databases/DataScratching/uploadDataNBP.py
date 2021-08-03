import pandas as pd
from uploadProceduresNBP import rate_upload_data_from_excel, date_upload_data_from_excel, main_table_upload_data_from_excel_nbp
from uploadProceduresNBP import urlopen, upload_today_maintable, upload_today_date
from typing import Dict


# dane ze strony:
# https://www.nbp.pl/home.aspx?f=/kursy/arch_a.html
# wgrywać format excel
# EUR, USD, UAH (hrywna), TRY (lira turecka)


currencies = ['1 EUR','1 USD', '1 CHF', '1 UAH', '1 CZK', '1 HRK', '1 RUB', '1 ILS', '1 TRY']

# ------upload from excel--------------
path = "nbp_data/archiwum_tab_a_2021.xls"
# date_upload_data_from_excel(path)
# rate_upload_data_from_excel(path, currencies) # TYLKO RAZ, przy pierwszym excelu
# main_table_upload_data_from_excel_nbp(path, currencies)


# -------upload from webpage------------

url = "https://www.nbp.pl/home.aspx?f=/kursy/kursya.html"

# upload_one_day_record_from_nbp_webpage(url, currencies)
# upload_today_date()
upload_today_maintable(url, currencies)