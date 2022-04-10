import pyodbc
import dbMethods
   
def connect(): 
    # conn_str = (
    #     r'DRIVER={SQL Server};'
    #     r'SERVER=(local);'
    #     r'Trusted_Connection=yes;'
    #     r'pool_timeout:30;'
    # )
    # cnxn = pyodbc.connect(conn_str, autocommit=True)
    # cur = cnxn.cursor()

    # try:
    #     cur.execute(""" 
    #                 (
    #                 IF EXISTS(SELECT * FROM master.sys.databases 
    #                 WHERE name='SqlHintsDB')
    #                 BEGIN
    #                 CREATE DATABASE [worktime_tracker_db]
    #                 SELECT 'New Database is Created'
    #                 END
    #                 """)
    #     #cnxn.commit()
    #     print('Database created')
    #     cnxn.close()
    #     cur.close()
        
    # except: #Exception as ex:
    #     print('ERROR acured')



    #dummy connection msg
    print('Connecting to database')
    #assuming db exist(is already created) locally
    conn_str = (
        r'DRIVER={SQL Server};'
        r'SERVER=(local);'
        r'DATABASE=worktime_tracker_db;'
        r'Trusted_Connection=yes;'
        r'pool_timeout:30;'
    )
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    table = []

    try:
        table = dbMethods.getProjects(cursor)
        table = table.fetchall()
    except:
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
        
    return cursor, table, cnxn