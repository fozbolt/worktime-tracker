# worktime-tracker

## CLI timer for tracking time spend on different projects with option to manage data from database or csv (+ feature to convert csv to sql and vise versa)

Create .exe:
 - pip install pyodbc or pymysql
 - pip install pyinstaller
 - pyinstaller --onefile main.py
 - -possible needed to modify your PyInstaller command to include the pyodbc module: pyinstaller --onefile --hidden-import=pyodbc main.py  or pymysql
 - run: ./dist/main

Connect to dummy db:
 - install msql server if on windows or mariadb if on mac then comment out code for the unused one in dbConnection.py

to-do:
- sql batch .exe run
- connect only once - DB
- find and handle remaining errors and outliers
- add deleteAll method to DB and file
- GUI
