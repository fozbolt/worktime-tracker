import time
import os
import convertTime

def is_file_empty(filePath):
    try:
        import pathlib as p
        path = p.Path(filePath)
        if '~' in filePath:
            path = path.expanduser()
        if not path.exists() and path.stat().st_size > 0:
            return True
        return False
    except FileNotFoundError:
        return True


def stopwatch(previous_time):
    curr_time = 0
    while True:
        try:
            input("Press Enter to continue and ctrl+C to exit the stopwatch")
            start_time=time.time()
            print("Stopwatch has started")
            while True:
                print("Time elapsed:",round(time.time()-start_time,0),'secs',end='\n')
                time.sleep(1)
        except KeyboardInterrupt:
            print("Timer has stopped")
            end_time=time.time()
            #add previous time (if chosen) to current time
            previous_time = convertTime.getSeconds(previous_time)
            curr_time=round(float(previous_time) + round(end_time-start_time,2),2)
            print("The time elapsed:",curr_time,'secs')
            break
    
    return curr_time


def setProjectName(file,csvreader):
    projectName=''
    valid = False
    while projectName=='' or valid==False:
        projectName = input('Create unique name for project:')
        #check if project name already exist
        valid = True
        file.seek(0)
        for row in csvreader:
                if projectName == row[1].strip(' '):
                    valid = False
                    print('Project with this name already exists.')
         
    return projectName


#ne azurira se prev time i sprema se pod novu variablu(redak)
def findProject(file,csvreader):
    key=''
    projectFound = False
    while (key=='' and projectFound == False) or key!='exit':
        key = input('Enter name of existing project, for list of projects type "ls", for exit type "exit":')
        if key!= 'exit' and key!= 'ls':
            file.seek(0)
            for index, row in enumerate(csvreader):
                if key == row[1].strip(' '):
                    projectFound = True
                    global previous_time
                    previous_time=row[2]
                    
                    return index,previous_time
        #try again
        file.seek(0)
        if key=='ls': 
              for row in csvreader:
                print(row)
        elif key=='exit':
            return setProjectName(file,csvreader)
        else: 
            print('Project not found. Try Again.')
    
    
def getID(filePath, file, csvreader):
    if  os.path.getsize(filePath) == 0: 
        return 0 
    else: 
        file.seek(0)
        return len(list(csvreader))-1

