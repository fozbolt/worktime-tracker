import pyodbc 
import dbMethods
import convertTime
from datetime import datetime
import uuid

def runTimer():
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
    choice = ''
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
                    
    
    previous_time = '00:00:00'
    projectID = uuid.uuid1()
    projectName= ''
    dateCreated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dateUpdated = datetime.now().strftime("%d/%m/%Y %H:%M:%S") 

    if len(table) != 0:
        choice = input('Load previous time or start new(type p for previous or n for new:')
        while choice.lower() not in ['p', 'n']:
            choice = input('Load previous time or start new(type p for previous or n for new:')
            
        if choice.lower()=='n':
                previous_time = '00:00:00'
                projectName = dbMethods.setProjectName(table)
            
        elif choice.lower()=='p':
            result=dbMethods.findProject(table,cursor, cnxn)
            #if user has chosen exit in findproject() it returns a string not an index because it goes to setProjectName()
            
            if isinstance(result, str): 
                projectName=result
                choice='n'
                
            else:
                projectName = result[0]
                previous_time = result[1]
                dateUpdated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    else:
        print('Database is empty, create your first project timer')
        projectName = dbMethods.setProjectName(table)
        
        
        
    
    final_time = dbMethods.stopwatch(previous_time)
    final_time = convertTime.getHours(final_time)

    if choice.lower()=='n':
        cursor.execute(
            """
            INSERT INTO Times
            (ID,projectName,time,dateUpdated,dateCreated)
            VALUES (?,?,?,?,?)
            """,
            (
            projectID,
            projectName,
            final_time,
            dateUpdated,
            dateCreated
            )
        )
        cnxn.commit()

        cursor.close()
        
    elif choice.lower()=='p':
        cursor.execute(
            """
            UPDATE Times 
            SET time = ?, dateUpdated = ? WHERE projectName = ?
            """,
            ( final_time, dateUpdated, projectName )
        )
        cnxn.commit()

        cursor.close()
        
        
    cnxn.close()
    
runTimer()