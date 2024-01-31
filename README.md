# worktime-tracker

## CLI timer for tracking time spend on different projects with option to manage data from database or csv

Create .exe:
 - pip install pyodbc
 - pip install pyinstaller
 - pyinstaller --onefile main.py
 - -possible needed to modify your PyInstaller command to include the pyodbc module: pyinstaller --onefile --hidden-import=pyodbc main.py
 - run: ./dist/main

to-do:
- sql batch .exe run
- connect only once - DB
- find and handle remaining errors and outliers
- add deleteAll method to DB and file
- GUI
