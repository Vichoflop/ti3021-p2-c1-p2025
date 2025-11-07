import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

username= os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(user = username, password = password, dsn = dsn)

def create_table():
    ddl = (
        "CREATE TABLE vjcr_personas ("
        "rut VARCHAR2(50) PRIMARY KEY,"
        "nombres VARCHAR2(200),"
        "apellidos VARCHAR2(200),"
        "fecha_nacimiento DATE,"
        "numero_telefono VARCHAR2(50)"
        ")"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(ddl)
                print("Tabla 'personas' creada.")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la tabla: {err}")


create_table()

from datetime import datetime

def create_persona(rut = None, nombres = None, apellidos = None, fecha_nacimiento = None, cod_area = "+569", numero_telefono = None): 
    sql = (
        "INSERT INTO personas (rut, nombres, apellidos, fecha_nacimiento, cod_area, numero_telefono) "         
        "VALUES (:rut, :nombres, :apellidos, :fecha_nacimiento, :cod_area, :numero_telefono)"     
    )    
    if fecha_nacimiento: 
        bind_fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    else:
        bind_fecha = None     
    with get_connection() as conn:         
        with conn.cursor() as cur:            
            cur.execute(sql, {                 
            "rut": rut,                 
            "nombres": nombres,                 
            "apellidos": apellidos,                 
            "fecha_nacimiento": bind_fecha,                 
            "cod_area": cod_area,                 
            "numero_telefono": numero_telefono,             
            })             
        conn.commit()             
    print(f"Persona con RUT={rut} creada.") 

create_persona()
    
       