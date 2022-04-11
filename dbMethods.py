import time, sys
import convertTime
import dbMethods
import pyodbc

def setProjectName(table):
    projectName=''
    valid = False
    while projectName=='' or valid==False:
        projectName = input('Create unique name for project or type "exit: ')
        #check if project name already exist
        valid = True
        
        for row in table:
            if projectName == row[1].strip(' '):
                valid = False
                print('Project with this name already exists.')
                break
        if projectName == 'exit': quit()   
        
    return projectName



def getProjects(cursor):
    return cursor.execute("SELECT * From Times")



def openHelp():
    print('1) for list of projects type "ls"\n2) for deleting a project type "del"\n3) to manually add time to previous project type "add"\n4) for exit type "exit":')
    
    
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
  


def addTimeManually(table, cursor, conn):
    key=''
    projectFound = False
    previous_time = 0
    
    while (key=='' and projectFound == False) or key!='exit':
        key = input('To manually add time, enter the name of existing project, for help type "help": ')
        if key!= 'exit' and key!= 'ls':
            for index, row in enumerate(table):
                if key == row[1].strip(' '):
                    projectFound = True
                    print('Fethed previous time: ', row[2])
                    #convert to seconds to sum it up and then back to timestring
                    previous_time = convertTime.getSeconds(row[2]) + convertTime.getSeconds(manualUserInput())
                    previous_time = convertTime.getHours(previous_time)
                    
                    return key,previous_time
                
        #refactor this with switch or something
        if projectFound == True:
            print('Additional time successfully added')
            return getProjects(cursor)
        elif key=='ls': 
            if len(table) == 0:
                print('There are no existing projects in database at the moment. Type "exit" and create new project')
            else:
                for row in table:
                    print(row)
        elif key=='help':
            openHelp()
    
        elif key=='exit':
            return setProjectName(table)
        else: 
            print('Project not found. Try Again.')


def manualUserInput():
    time=''
    validFormat=False
    while time=='' or validFormat==False:
        time = input('Enter time that you want to add to fetched previous time ("HH:MM:SS" fromat): ')    
        validFormat = checkFormat(time)
        
    return time   



def checkFormat(time_string):
    try:
        time.strptime(time_string, '%H:%M:%S')
    except ValueError:
        return False
    
    return True


      

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
            print(cursor)
            table = dbMethods.getProjects(cursor)
            table = table.fetchall()
            #rewriteIDs()
        elif key=='exit':
            return setProjectName(table)
        elif key =='add':
            return addTimeManually(table, cursor, conn)
      
        else: 
            print('Project not found. Try Again.')


def stopwatch(previous_time):
    '''alert:
    -this method has two stopwatch-like functions, one is with start-end time and one is with incrementation
    reason behind this is that because of principles that standard stopwatch calculates time after its stopping,
    incrementation is way easier for dynamic result presentation, but incrementation is less precise so i put both methods
    to work each for its own purpose
    '''
    curr_time = convertTime.getSeconds(previous_time)
    curr_dynamic_timer = curr_time
    while True:
      
        try:
            input("Press Enter to continue and ctrl+C to exit the stopwatch")
            start_time=time.time()
            print("Timer has started")
            while True:
                # print("Time elapsed:",round(time.time()-start_time,0),'secs',end='\n')
                txt = convertTime.getHours(curr_dynamic_timer)+ chr(13)
                sys.stdout.write(txt)
                sys.stdout.flush()
                time.sleep(1)
                curr_dynamic_timer = curr_dynamic_timer + 1
                
        except KeyboardInterrupt:
            print("Timer has stopped")
            end_time=time.time()
            #add previous time (if chosen) to current time
            previous_time = convertTime.getSeconds(previous_time)
            curr_time=round(float(previous_time) + round(end_time-start_time,2),2)
            print("The time elapsed:",convertTime.getHours(curr_time))
            break
    
    return curr_time