import pyodbc 
import pandas as pd

conn_str = (
        r'DRIVER={SQL Server};'
        r'SERVER=(local);'
        r'DATABASE=worktime_tracker_db;'
        r'Trusted_Connection=yes;'
        r'pool_timeout:30;'
    )

cnxn = pyodbc.connect(conn_str)

cursor = cnxn.cursor()
    
    
sql_query = pd.read_sql_query(''' 
                              select * from test_database.dbo.product
                              '''
                              ,conn) # here, the 'conn' is the variable that contains your database connection information from step 2

df = pd.DataFrame(sql_query)
df.to_csv (r'C:\Users\Ron\Desktop\exported_data.csv', index = False) # place 'r' before the path name