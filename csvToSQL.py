import pandas as pd
import pyodbc 

data = pd.read_csv (r'C:\Users\Ron\Desktop\Test\products.csv')   
df = pd.DataFrame(data)

print(df)


conn_str = (
        r'DRIVER={SQL Server};'
        r'SERVER=(local);'
        r'DATABASE=worktime_tracker_db;'
        r'Trusted_Connection=yes;'
        r'pool_timeout:30;'
    )

cnxn = pyodbc.connect(conn_str)

cursor = cnxn.cursor()
    
    
#ako nema tablea vec, za bazu se pretpostavlja da postoji
cursor.execute('''
		CREATE TABLE products (
			product_id int primary key,
			product_name nvarchar(50),
			price int
			)
               ''')


#insert dataframe into table
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO products (product_id, product_name, price)
                VALUES (?,?,?)
                ''',
                row.product_id, 
                row.product_name,
                row.price
                )
conn.commit()