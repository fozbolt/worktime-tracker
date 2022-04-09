import csv
import os
from datetime import datetime
import fileMethods
import convertTime
import uuid

def runTimer():
    projectName = ''
    projectIndex = ''
    choice=''
    final_time = 0
    previous_time = '00:00:00'
    filePath = 'worktime-tracker-data.csv'
    headerOriginal = ['ID', 'project_name','time', 'date_updated', 'date_created']
    dateCreated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dateUpdated = datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
    file_is_empty = fileMethods.is_file_empty(filePath)
    csvreader = ''



    try:
        if file_is_empty==True:
            file = open(filePath, 'w+',encoding="utf-8")
            print('file open success')
            
        else:
            file = open(filePath, 'r+',encoding="utf-8")
            print('file reading success')
        
        csvreader = csv.reader(file)
    except:
        print('Error while opening csv file')
        quit()
    


    #If file is not empty give user a choice to start from previous project time or create new project
    if  os.path.getsize(filePath)!=0:
        choice = input('Load previous time or start new(type "p" for previous or "n" for new: ')
        
        while choice.lower() not in ['p', 'n']:
            choice = input('Load previous time or start new(type "p" for previous or "n" for new: ')
        
        if choice.lower()=='n':
            previous_time = '00:00:00'
            projectName = fileMethods.setProjectName(file,csvreader)
        
        elif choice.lower()=='p':
            result=fileMethods.findProject(file,csvreader)
            #if user has chosen exit in findproject() it returns a string not an index because it goes to setProjectName()
            if isinstance(result, str): 
                projectName=result
                choice='n'
            else:
                projectIndex = result[0]
                previous_time = result[1]
                dateUpdated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
        
            
    #If file is empty create new project name
    else:
        projectName = fileMethods.setProjectName(file,csvreader)
        
        
    final_time = fileMethods.stopwatch(previous_time)
    final_time = convertTime.getHours(final_time)
    writer = csv.writer(file, lineterminator='\n')

    if os.path.getsize(filePath) == 0: 
        writer.writerow(headerOriginal)
        
        
        
    #update for existing project
    if choice.lower()=='p':  
        file.seek(0)
        next(csvreader) #skip header  
        lines = list(csvreader)
        #lines[projectIndex-1][1] = projectName
        lines[projectIndex-1][2] = final_time
        lines[projectIndex-1][3] = dateUpdated
        
        #overwrite everything with array
        writer = csv.writer(open(filePath, 'w', encoding="utf-8"), lineterminator='\n')
        writer.writerow(headerOriginal)
        writer.writerows(lines)

    #insert new project
    else: 
        writer.writerow([uuid.uuid1(), projectName, final_time, dateUpdated, dateCreated])

    file.close()
