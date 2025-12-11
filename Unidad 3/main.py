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


class Database:
    def __init__(self, username, password, dsn):
        self.username = username
        self.password = password
        self.dsn = dsn
    #Funciones de conexion reutilizable
    def get_connection(self):
        return oracledb.connect(user = self.username, password = self.password, dsn = self.dsn)
    #Funcion para crear todas las tablas
    def create_all_tables(self):
        pass
    #Funcion para ejecutar estandarizadamente las querys
    def query(self, sql: str, parametros: Optional[dict]):
        print(f"Ejecutando query: \n{sql} \n {parametros}")
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    resultados = cur.execute(statement=sql, parameters=parametros)
                    for fila in resultados:
                        print(fila)
        except oracledb.DatabaseError as error:
            print(error)
        




class Auth:
    @staticmethod
    def login(db:Database, username: str, password: str):
        pass
    @staticmethod
    def register(db:Database, username: str, password: str):
        pass