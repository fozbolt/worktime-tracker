import time
import csv
import os

def is_file_empty(filePath):
    # Check if file exist and it is empty
    return os.path.exists(filePath) and os.stat(filePath).st_size == 0


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
            curr_time=round(float(previous_time) + round(end_time-start_time,2),2)
            print("The time elapsed:",curr_time,'secs')
            break
    
    return curr_time
    


final_time = 0
previous_time = 0
filePath = 'worktime-tracker-data.csv'
header = ['Times']
file_is_empty = is_file_empty(filePath)
rows = []
choice=''


try:
    if file_is_empty==False:
        file = open('worktime-tracker-data.csv', 'r+')
        print('file reading success')
        csvreader = csv.reader(file)
        #so it doesnt raise a stop iteration error on EOL
        header = next(csvreader,None)       

        for row in csvreader:
            print('tu sam')
            print(row)
            rows.append(row)
            #hardcode for now - we need some flag to know to rewrite value not add two times and write in new row
            previous_time=row[0]
            print('row',  row[0])
            
    else:
        file = open('worktime-tracker-data.csv', 'w+')
        print('file open success')
except:
    print('Error while opening csv file')
    #print(error)


if file_is_empty==False:
    choice = input('Load previous time or start new(type p for previous or n for new:')
    
    while choice.lower() not in ['p', 'n']:
        choice = input('Load previous time or start new(type p for previous or n for new:')
    
    if choice=='n' or choice=='N':
        previous_time = 0
   

final_time = stopwatch(previous_time)
writer = csv.writer(file, lineterminator='\n')

if file_is_empty==True: 
    writer.writerow(header)
writer.writerow([final_time])

file.close()


