import oracledb 
import os 
from dotenv import load_dotenv 
 
load_dotenv()  

username = os.getenv("user") 
dsn = os.getenv("host") 
password = os.getenv("password") 



with oracledb.connect(user=username, password=password, dsn=dsn) as connection:    
    with connection.cursor() as cursor:        
        sql = "select sysdate from dual"         
        resultado = cursor.execute(sql)
        for row in cursor.execute(sql):
            print(row)
            for column in row:
                print(column)

                
