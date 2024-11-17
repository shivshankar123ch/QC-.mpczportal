
import psycopg2

import pandas as pds

from sqlalchemy import create_engine
import cx_Oracle 
# from CA.views import transaction_upload

 

# Create an engine instance
alchemyEngine = create_engine('postgresql+psycopg2://postgres:12345@localhost/qc_local', pool_recycle=3600);
dbConnection    = alchemyEngine.connect();
 
df  = pds.read_sql("select * from \"CA_collection_agent\"", dbConnection);

df2 = df.drop(df.columns[[0, 17 ,18 ,19]], axis=1)
# df2.columns = df2.columns.str.upper()
df2.to_sql('CA_collection_agent',con=dbConnection, if_exists='append', index = False)

# df2.to_excel('data.xlsx', sheet_name='new_sheet_name', index = False)
# data_upload = transaction_upload()

dbConnection.close();