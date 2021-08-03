import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from urllib.request import urlopen
from datetime import date


def engine_create():
    db_string = "postgres://postgres:postgres1@localhost:5432/currencyValuesP"
    eng = create_engine(db_string)
    return eng


def main_table_upload_data_from_excel_nbp(path: str, currencies: str):
    data = pd.read_excel(path)
    data = data.drop(index=0)
    main_table = pd.DataFrame(data, columns = ['Data'] + currencies)
    for currency in currencies:
        main_table = main_table.rename(columns={currency: currency[2:5]+'/PLN'})

    main_table = main_table.rename(columns={'Data': 'date_id'}).melt(id_vars=['date_id'], var_name='rate_id')

    max_id = get_max_id_from_database_table('maintable', 'index')
    if max_id > 0:
        main_table.index += (max_id + 1)
    else:
        main_table.index += 1

    engine = engine_create()
    dates_df = pd.read_sql_table(table_name='dates', con=engine, index_col='date_id')
    main_table['date_id'] = main_table['date_id'].map(lambda x: dates_df[dates_df['date'] == x].index.values.astype(int)[0])

    rates_df = pd.read_sql_table(table_name='rates', con = engine, index_col='rate_id')
    rates_df = rates_df[rates_df['bank_name'] == 'NBP']
    main_table['rate_id'] = main_table['rate_id'].map(lambda x: rates_df[rates_df['rate'] == x].index.values.astype(int)[0])

    # engine = engine_create()
    print(main_table)
    main_table.to_sql('maintable', engine, if_exists='append')


def rate_upload_data_from_excel(path: str, currencies):
    data = pd.read_excel(path)
    data = data.drop(index=0)
    main_table = pd.DataFrame(data, columns=['Data'] + currencies)
    for currency in currencies:
        main_table = main_table.rename(columns={currency: currency[2:5] + '/PLN'})

    main_table = main_table.rename(columns={'Data': 'date_id'}).melt(id_vars=['date_id'], var_name='rate_id')

    rates = pd.DataFrame(main_table['rate_id'].unique(), columns = ['rate'])
    rates.insert(loc = 0, column = 'bank_name', value='NBP')
    rates.index.name = 'rate_id'
    rates.index += 1
    engine = engine_create()
    rates.to_sql('rates', engine, if_exists='append')


def date_upload_data_from_excel(path: str):
    data = pd.read_excel(path)
    data = data.drop(index = 0)

    # ---date---
    date = pd.DataFrame(data, columns = ['Data'])
    date = date.rename(columns={'Data': 'date'})
    date.index.name = 'date_id'

    print(date)
    max_id = get_max_id_from_database_table('dates', 'date_id')

    if max_id > 0:
        date.index += max_id

    engine = engine_create()
    date.to_sql('dates', engine, if_exists='append')


def rate_upload_record_from_dict(d: dict):
    rate = pd.DataFrame.from_dict(data=d)
    rate.index.name = 'rate_id'
    rate.index += get_max_id_from_database_table('rates', 'rate_id')
    engine = engine_create()
    rate.to_sql('rates', engine, if_exists='append')


def get_max_id_from_database_table(table_name: str, table_id_name: int) -> int:
    # try:
    engine = engine_create()
    # except Exception as e:
    output = engine.execute(f"SELECT MAX({table_id_name}) from {table_name}").fetchall()[0][0]

    if output is None:
        output = 0

    print(output)
    return output


def check_if_record_already_exists_in_database_table(table_name: str):
    pass


def upload_today_maintable(url, currencies):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    main_table_df = pd.DataFrame(columns = ['date_id', 'rate_id', 'value'])
    main_table_df.index.name = 'index'



    for currency in currencies:
        value_start_index = html.find(currency) + len(currency) + len('</td> <td class="bgt2 right">')
        currency_value = html[value_start_index:(value_start_index + 6)]
        today_date = date.today().strftime("%d.%m.%Y")
        main_table_df = main_table_df.append({'date_id': today_date, 'rate_id': currency[2:5]+'/PLN', 'value': currency_value}, ignore_index=True)

    max_id = get_max_id_from_database_table('maintable', 'index')
    if max_id > 0:
        main_table_df.index += (max_id + 1)
    else:
        main_table_df.index += 1

    main_table_df.index.name = 'index'

    engine = engine_create()
    dates_df = pd.read_sql_table(table_name='dates', con=engine, index_col='date_id')
    main_table_df['date_id'] = main_table_df['date_id'].map(lambda x: dates_df[dates_df['date'] == x].index.values.astype(int)[0])

    rates_df = pd.read_sql_table(table_name='rates', con=engine, index_col='rate_id')
    rates_df = rates_df[rates_df['bank_name'] == 'NBP']
    main_table_df['rate_id'] = main_table_df['rate_id'].map(lambda x: rates_df[rates_df['rate'] == x].index.values.astype(int)[0])

    main_table_df['value'] = main_table_df['value'].str.replace(',', '.')
    pd.to_numeric(main_table_df['value'])
    print(main_table_df)
    main_table_df.to_sql('maintable', engine, if_exists='append')






def upload_today_date():
    today_date = date.today().strftime("%d.%m.%Y")
    today_date_df = pd.DataFrame({'date': [today_date]}, columns = ['date'])
    today_date_df.index.name = 'date_id'
    max_id = get_max_id_from_database_table('dates', 'date_id')
    if max_id > 0:
        today_date_df.index += (max_id + 1)
    else:
        today_date_df.index = 1

    engine = engine_create()
    today_date_df.to_sql('dates', engine, if_exists='append')


