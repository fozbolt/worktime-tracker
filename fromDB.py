import time
import pyodbc 

def runTimer():
    conn_str = (
        r'DRIVER={SQL Server};'
        r'SERVER=(local);'
        r'DATABASE=worktime_tracker_db;'
        r'Trusted_Connection=yes;'
        r'pool_timeout:30;'
    )
    cnxn = pyodbc.connect(conn_str)

    cursor = cnxn.cursor()

    #Simple connection test
    # cursor.execute("SELECT @@version;") 
    # row = cursor.fetchone() 
    # while row: 
    #     print(row[0])
    #     row = cursor.fetchone()

    final_time = 0

    choice = input('Load previous time or start new(type p for previous or n for new:')
    while choice.lower() not in ['p', 'n']:
        choice = input('Load previous time or start new(type p for previous or n for new:')


    previous_time = 0
    if choice=='p' or choice=='P':
        cursor.execute("SELECT * From Times")
        #ovako uzima zadnjeg, kasnije modificira da uzmemo trazenog
        for row in cursor.fetchall():
            previous_time = row[0]
            break


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
            final_time=round(float(previous_time) + round(end_time-start_time,2),2)
            print("The time elapsed:",final_time,'secs')
            break
        
        
    print(final_time)


    cursor.execute(
        """
        INSERT INTO Times
        (Time)
        VALUES (?)
        """,
        (final_time
        )
    )
    cnxn.commit()



    cursor.close()
    cnxn.close()