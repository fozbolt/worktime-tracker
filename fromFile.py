import time
import csv
import os
from datetime import datetime
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


def setProjectName():
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
def findProject():
    key=''
    projectFound = False
    while (key=='' and projectFound == False) or key!='exit':
        key = input('Enter name of existing project, for list of projects type "ls", for exit type "exit":')
        if key!= 'exit' and key!= 'ls':
            file.seek(0)
            for index, row in enumerate(csvreader):
                if key == row[1].strip(' '):
                    projectFound = True
                    global previous_time, projectName
                    previous_time=row[2]
                    projectName = key
                    
                    return index
        #try again
        file.seek(0)
        if key=='ls': 
              for row in csvreader:
                print(row)
        elif key=='exit':
            #change choice to 'new project'
            global choice
            choice='n'
            return setProjectName()
        else: print('Project not found. Try Again.')
    
    
def getID():
    if  os.path.getsize(filePath) == 0: 
        return 0 
    else: 
        file.seek(0)
        return len(list(csvreader))-1



projectName = ''
projectIndex = ''
choice=''
final_time = 0
previous_time = '00:00:00'
filePath = 'worktime-tracker-data.csv'
headerOriginal = ['ID', 'project_name','time', 'date_updated', 'date_created']
dateCreated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
dateUpdated = datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
file_is_empty = is_file_empty(filePath)
csvreader = ''



try:
    if file_is_empty==True:
        file = open(filePath, 'w+')
        print('file open success')
        
    else:
        file = open(filePath, 'r+')
        print('file reading success')
    
    csvreader = csv.reader(file)
except:
    print('Error while opening csv file')
    quit()
 


#If file is not empty give user a choice to start from previous project time or create new project
if  os.path.getsize(filePath)!=0:
    choice = input('Load previous time or start new(type "p" for previous or "n" for new:')
    
    while choice.lower() not in ['p', 'n']:
        choice = input('Load previous time or start new(type "p" for previous or "n" for new:')
    
    if choice.lower()=='n':
        previous_time = '00:00:00'
        projectName = setProjectName()
       
    elif choice.lower()=='p':
        projectIndex=findProject()
        dateUpdated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #if user has chosen exit in findproject() it returns a string not an index
        if isinstance(projectIndex, str): projectName=projectIndex
        
#If file is empty create new project name
else:
    projectName = setProjectName()
    
    
final_time = stopwatch(previous_time)
final_time = convertTime.getHours(final_time)
writer = csv.writer(file, lineterminator='\n')

if os.path.getsize(filePath) == 0: 
    writer.writerow(headerOriginal)
    


#update for existing project
if choice.lower()=='p':  
    file.seek(0)
    next(csvreader) #skip header  
    lines = list(csvreader)
    lines[projectIndex-1][1] = projectName
    lines[projectIndex-1][2] = final_time
    lines[projectIndex-1][3] = dateUpdated
    
    #overwrite everything with array
    writer = csv.writer(open(filePath, 'w'), lineterminator='\n')
    writer.writerow(headerOriginal)
    writer.writerows(lines)

#insert new project
else: 
    writer.writerow([getID(), projectName, final_time, dateUpdated, dateCreated])

file.close()
