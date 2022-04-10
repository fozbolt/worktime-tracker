import pyodbc 
import pandas as pd

cnxn = 0
cursor = 0

try:
    conn_str = (
            r'DRIVER={SQL Server};'
            r'SERVER=(local);'
            r'DATABASE=worktime_tracker_db;'
            r'Trusted_Connection=yes;'
            r'pool_timeout:30;'
        )

    cnxn = pyodbc.connect(conn_str)

    cursor = cnxn.cursor()
    
except Exception as e:
    print(e)
    

try:
    sql_query = pd.read_sql_query(''' 
                                select * from worktime_tracker_db.dbo.Times
                                '''
                                ,cnxn) 
except Exception as e:
    print(e)


df = pd.DataFrame(sql_query)
df.to_csv ('exported_data_from_sql.csv', index = False) 
#or overwrite original working space
#df.to_csv ('worktime-tracker-data.csv', index = False) 

cursor.close()
cnxn.close()