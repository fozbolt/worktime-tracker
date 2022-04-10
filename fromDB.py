import pyodbc 
import dbMethods
import convertTime
from datetime import datetime
import uuid
import dbConnection

def runTimer():
    cursor,table,cnxn = dbConnection.connect()
    
    previous_time = '00:00:00'
    projectID = uuid.uuid1()
    projectName= ''
    dateCreated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dateUpdated = datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
    choice='n'

    if len(table) != 0:
        choice = input('Load previous time or start new(type p for previous or n for new): ')
        while choice.lower() not in ['p', 'n']:
            choice = input('Load previous time or start new(type p for previous or n for new): ')
            
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