import time
import convertTime
import dbMethods
import pyodbc

def setProjectName(table):
    projectName=''
    valid = False
    while projectName=='' or valid==False:
        projectName = input('Create unique name for project: ')
        #check if project name already exist
        valid = True
        
        for row in table:
            if projectName == row[1].strip(' '):
                valid = False
                print('Project with this name already exists.')
                break
        
    return projectName


#what with this choice?
def getProjects(cursor):
    return cursor.execute("SELECT * From Times")



def openHelp():
    print('1) for list of projects type "ls"\n2) for deleting a project type "del"\n3) for exit type "exit":')
    
    
def deleteProject(table, cursor, conn):
    key=''
    projectFound = False
    
    while (key=='' and projectFound == False) or key!='exit':
        key = input('Enter a name of project to delete, type "ls" for project list or "exit" for return: ')
        if key!= 'exit' and key!= 'ls':
            for row in (table):
                if key == row[1].strip(' '):
                    projectFound = True
                    cursor.execute('''
                                    DELETE FROM Times 
                                    WHERE projectName = ?
                                    ''', key)
                    
                    conn.commit()
            
        #try again
        if projectFound == True: 
            print('File successfully deleted') 
            return getProjects(cursor)
        elif key=='exit': 
            print('Exited successfully')
        elif key=='ls': 
            for row in table:
                print(row)   
        else: print('File not found')  
  

        

def findProject(table, cursor, conn):
    key=''
    projectFound = False
    while (key=='' and projectFound == False) or key!='exit':
        key = input('Enter name of existing project, for help type "help": ')
        if key!= 'exit' and key!= 'ls':
            for index, row in enumerate(table):
                if key == row[1].strip(' '):
                    projectFound = True
                    previous_time=row[2]
                    
                    return key,previous_time
                
        #refactor this with switch or something
        if key=='ls': 
            if len(table) == 0:
                print('There are no existing projects in database at the moment. Type "exit" and create new project')
            else:
                for row in table:
                    print(row)
        elif key=='help':
            openHelp()
        elif key=='del':
            #fetch updated db after deletion
            cursor = deleteProject(table, cursor, conn)
            table = dbMethods.getProjects(cursor)
            table = table.fetchall()
            #rewriteIDs()
        elif key=='exit':
            return setProjectName(table)
        else: 
            print('Project not found. Try Again.')


def stopwatch(previous_time):
    curr_time = 0
    while True:
        try:
            input("Press Enter to continue and ctrl+C to exit the stopwatch")
            start_time=time.time()
            print("Timer has started")
            while True:
                pass
            #     print("Time elapsed:",round(time.time()-start_time,0),'secs',end='\n')
            #     time.sleep(1)
        except KeyboardInterrupt:
            print("Timer has stopped")
            end_time=time.time()
            #add previous time (if chosen) to current time
            previous_time = convertTime.getSeconds(previous_time)
            curr_time=round(float(previous_time) + round(end_time-start_time,2),2)
            print("The time elapsed:",convertTime.getHours(curr_time))
            break
    
    return curr_time