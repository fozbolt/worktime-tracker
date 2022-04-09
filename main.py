from secrets import choice
import fromDB
import fromFile
 
choice = input('Run timer in SQL or File mode (type "1" for sql or "2" for file mode): ')
        
while choice.lower() not in ['1', '2']:
    choice = input('Run timer in SQL or File mode (type "1" for sql or "2" for file mode): ')
    
if choice=='1':
    fromDB.runTimer()
elif choice=='2':
    fromFile.runTimer()


print('Timer closed')