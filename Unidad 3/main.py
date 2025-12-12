#conexion a base de datos
import oracledb
import os
from dotenv import load_dotenv

#Haseheo de contraseñas
import bcrypt

#Consumo de API
import requests

#parametros opcionales
from typing import Optional

#Cargar las variables desde el archivo.env
load_dotenv()

#Cargar fechas
import datetime

class Database:
    def __init__(self, username, password, dsn):
        self.username = username
        self.password = password
        self.dsn = dsn
    def get_connection(self):
        return oracledb.connect(user = self.username, password = self.password, dsn = self.dsn)
    def create_all_tables(self):
        pass
    def query(self, sql: str, parametros: Optional[dict]):
        print(f"Ejecutando query: \n{sql} \n {parametros}")
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    resultados = cur.execute(statement=sql, parameters=parametros)
                    for fila in resultados:
                        print(fila)
                conn.commit()
        except oracledb.DatabaseError as error:
            print(error)
        

class Auth:
    @staticmethod
    def login(db:Database, username: str, password: str):
        pass
    @staticmethod
    def register(db:Database, username: str, password: str):
        pass

class Finance:
    def __init__(self,base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url
    def get_indicador(self, indicador: str, fecha: str = None):
        try:
            if not fecha:
                dd =datetime.datetime.now().day
                mm =datetime.datetime.now().month
                yyyy =datetime.datetime.now().year
                fecha = f"{dd}-{mm}-{yyyy}"
            url = f"{self.base_url}7{indicador}/{fecha}"
            respuesta = requests.get(url).json
            print(respuesta["Serie"][0]["valor"])
        except:
            print("Hubo un error con la solicitud")
    def get_usd(self, fecha:str = None):
        valor = self.get_indicador("dolar", fecha)
        print(f"El valor del dolar en CLP es: {valor}")
    def get_eur(self, fecha:str = None):
        valor = self.get_indicador("euro", fecha)
        print(f"El valor del Euro en CLP es: {valor}")
    def get_uf(self, fecha:str = None):
        valor = self.get_indicador("UF", fecha)
        print(f"El valor del UF en CLP es: {valor}")
    def get_ivp(self, fecha:str = None):
        valor = self.get_indicador("ivp", fecha)
        print(f"El valor del IVP en CLP es: {valor}")
    def get_ipc(self, fecha:str = None):
        valor = self.get_indicador("ipc", fecha)
        print(f"El valor del IPC en CLP es: {valor}")
    def get_utm(self, fecha:str = None):
        valor = self.get_indicador("utm", fecha)
        print(f"El valor del UTM en CLP es: {valor}")
       

if __name__ == "__main__":
    db = Database(
        username= os.getenv("ORACLE_USER"),
        password= os.getenv("ORACLE_PASSWORD"),
        dsn= os.getenv("ORACLE_DSN")
    )
    print(db.query("SELECT sysdate FROM dual"));





