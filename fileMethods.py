import time
import os
import convertTime
import csv 
import sys

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


def setProjectName(file,csvreader):
    projectName=''
    valid = False
    while projectName=='' or valid==False:
        projectName = input('Create unique name for project or type "exit: ')
        #check if project name already exist
        valid = True
        file.seek(0)
        for row in csvreader:
            if projectName == row[1].strip(' '):
                valid = False
                print('Project with this name already exists.')
        if projectName == 'exit': quit()
    return projectName


def openHelp():
    print('1) for list of projects type "ls"\n2) for deleting a project type "del"\n3) to manually add time to previous project type "add"\n4) for exit type "exit":')

# def rewriteIDs():
#     #again not optimal because of another file opening
#     #https://gist.github.com/ertanyildiz/0a69f4a955d8a0fe01b0c5069e7aec64
    
#     with open('worktime-tracker-data.csv') as inp, open('worktime-tracker-data.csv', 'w') as out:
#         reader = csv.reader(inp)
#         writer = csv.writer(out, delimiter=',')
#         #No need to use `insert(), `append()` simply use `+` to concatenate two lists.
#         writer.writerow(['ID'] + next(reader,None))
#         #Iterate over enumerate object of reader and pass the starting index as 1.
#         writer.writerows([i] + row for i, row in enumerate(reader, 1))
    
    
def deleteProject(file,csvreader):
    #this function is not optimal because it opens files again
    key=''
    projectFound = False
    
    while (key=='' and projectFound == False) or key!='exit':
        key = input('Enter a name of project to delete, type "ls" for project list or "exit" for return: ')
        if key!= 'exit' and key!= 'ls':
            file.seek(0)
            lines = list(csvreader)
            writer = csv.writer(open('worktime-tracker-data.csv', 'w', encoding="utf-8"), lineterminator='\n')
            for row in (lines):
                if key == row[1].strip(' '):
                    projectFound = True
                elif key != row[1].strip(' '):
                    writer.writerow(row)
        #try again
        file.seek(0)
        if projectFound == True: 
            print('File successfully deleted') 
            key='exit'  
        elif key=='exit': 
            print('Exited successfully')
        elif key=='ls': 
            for row in csvreader:
                print(row) 
        else: 
            key=''
            print('File not found')  



#ne azurira se prev time i sprema se pod novu variablu(redak)
def findProject(file,csvreader):
    key=''
    projectFound = False
    while (key=='' and projectFound == False) or key!='exit':
        key = input('Enter name of existing project, for help type "help": ')
        if key!= 'exit' and key!= 'ls':
            file.seek(0)
            for index, row in enumerate(csvreader):
                if key == row[1].strip(' '):
                    projectFound = True
                    previous_time=row[2]
             
                    return index,previous_time
        #try again
        file.seek(0)
        #refactor this with switch or something
        if key=='ls': 
            lst = []
            for row in csvreader:
                lst.append(row)
                print(row)
            if len(lst) < 2: #1 is header row
                print('There are no existing projects in database at the moment. Type "exit" and create new project')
        elif key=='help':
            openHelp()
        elif key=='del':
            deleteProject(file,csvreader)
            #rewriteIDs()
        elif key=='add':
            return addTimeManually(file,csvreader)
        elif key=='exit':
            return setProjectName(file,csvreader)
        else: 
            print('Project not found. Try Again.')
    


def addTimeManually(file,csvreader):
    #this function is not optimal because it opens files again
    key=''
    projectFound = False
    previous_time = 0
    
    while (key=='' and projectFound == False) or key!='exit':
        key = input('To manually add time, enter the name of existing project, for help type "help": ')
        if key!= 'exit' and key!= 'ls':
            file.seek(0)
            for index, row in enumerate(csvreader):
                if key == row[1].strip(' '):
                    projectFound = True
                    print('Fethed previous time: ', row[2])
                    #convert to seconds to sum it up and then back to timestring
                    previous_time = convertTime.getSeconds(row[2]) + convertTime.getSeconds(manualUserInput())
                    previous_time = convertTime.getHours(previous_time)
                    
                    return index,previous_time
        #try again
        file.seek(0)
        if projectFound == True: 
            #it doesnt go to this because we return it earlier, but i'll leave it for now
            print('Time added successfully. New time: ', previous_time) 
            key='exit'  
        elif key=='exit': 
            print('Exited successfully')
        elif key=='ls': 
            for row in csvreader:
                print(row)
        elif key=='help':
            openHelp()
        else: 
            key=''
            print('File not found')  


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

     
            
def getID(filePath, file, csvreader):
    if  os.path.getsize(filePath) == 0: 
        return 0 
    else: 
        file.seek(0)
        return len(list(csvreader))-1

