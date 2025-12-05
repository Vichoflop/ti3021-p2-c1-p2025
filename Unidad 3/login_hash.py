#Dependencias: pip install oracledb python-dotenv bcrypt
import oracledb
from dotenv import load_dotenv
import os 
import bcrypt


load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(
        user = username,
        password = password,
        dsn = dsn
    )

def create_table_users():
    query = (
        "CREATE TABLE USERS("
        "ID INT PRIMARY KEY,"
        "username VARCHAR2(100) NOT NULL UNIQUE,"
        "password VARCHAR2(100) NOT NULL"
        ")"
    )

incoming_password = input("Ingresa una contraseña: ").encode("UTF-8")
salt = bcrypt.gensalt(rounds=12)
hashed_password = bcrypt.hashpw(incoming_password, salt)

print(f"Contraseña obtenida: {incoming_password}")
print(f"Contraseña hasheada: {hashed_password}")
print(f"Largo del hasheo: {len.hashed_password}")


def create_schema(query):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        # Ignorar error si la tabla no existe (ORA-00942)
        if "ORA-00942" not in str(e):
            print(f"Error en base de datos: {e}")


create_table_users()
query = (
    "INSERT INTO USERS( id, username, password)"
    "VALUES(:id, :username, :password)"
)

parametros = (
    
)