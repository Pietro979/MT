import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import select
from sqlalchemy import insert
from datetime import datetime

import uploadProceduresNBP

# engine = createProcedures.engine_create()

# metadata = MetaData()

# stmt = 'select * from rates'
# results = engine.execute(stmt).fetchall()[0]
# print(results)

engine = uploadProceduresNBP.engine_create()
# query = 'SELECT date_id, date FROM dates'

# results = engine.execute(query).fetchall()
# list = [result[1] for result in results]
#
# # now = datetime.now()
# # str_list = now.strftime("%Y")
# list_dates = [element.strftime("%Y-%m-%d") for element in list]
#
# data = ['2012-03-02','2012-03-04']
#
# data_dict = {element: data.index(element) for element in data}
# print(data_dict)
dates_df = pd.read_sql_table(table_name='dates', con=engine, index_col='date_id')
print(dates_df)

