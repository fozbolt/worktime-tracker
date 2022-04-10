import pandas as pd
import pyodbc 

data = pd.read_csv ('worktime-tracker-data.csv')   
df = pd.DataFrame(data)

cnxn = 0
cursor = 0

#print(df)

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
    
#create table if it doesnt exist, db must be created manually for now
try:
    cursor.execute('''
        CREATE TABLE Times (
                ID UNIQUEIDENTIFIER  PRIMARY KEY,
                projectName VARCHAR(36) NOT NULL,
                time  VARCHAR(12) NOT NULL,
                dateUpdated DATETIME NOT NULL,
                dateCreated DATETIME NOT NULL
             );
        ''')
    cnxn.commit()
except: 
    pass

try:
    #insert dataframe into table
    for row in df.itertuples():
        cursor.execute(
            """
            INSERT INTO Times
            (ID,projectName,time,dateUpdated,dateCreated)
            VALUES (?,?,?,?,?)
            """,
            (
            row.ID,
            row.projectName,
            row.time,
            row.dateUpdated,
            row.dateCreated
            )
        )
        cnxn.commit()

        cursor.close()
    cnxn.commit()

except Exception as e:
    print(e)
    

cnxn.close()