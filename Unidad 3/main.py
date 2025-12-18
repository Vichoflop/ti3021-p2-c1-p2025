import bcrypt
import requests
import oracledb
import os
from dotenv import load_dotenv
from typing import Optional
import datetime

load_dotenv()


class Database:
    def __init__(self, username, dsn, password):
        self.username = username
        self.dsn = dsn
        self.password = password

    def get_connection(self):
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)

    def create_all_tables(self):
        tables = [
            (
                "CREATE TABLE USERS("
                "id INTEGER PRIMARY KEY,"
                "username VARCHAR(32) UNIQUE,"
                "password VARCHAR(512)"
                ")"
            ),
            (
                "CREATE TABLE Consulta_users("
                "id INTEGER PRIMARY KEY,"
                "user_id INTEGER,"
                "username VARCHAR(32),"
                "fecha_consulta VARCHAR(64),"
                "opcion VARCHAR(64)"
                ")"
            )
        ]

        for table in tables:
            try:
                self.query(table)
            except Exception:
                # si ya existe u otro error, ignorar para no romper
                pass

    def query(self, sql: str, parameters: Optional[dict] = None):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    ejecucion = cur.execute(sql, parameters or {})
                    if sql.strip().upper().startswith("SELECT"):
                        resultado = []
                        for fila in ejecucion:
                            resultado.append(fila)
                        return resultado
                conn.commit()
        except oracledb.DatabaseError as error:
            print(error)


class Auth:
    @staticmethod
    def login(db: Database, username: str, password: str):
        resultado = db.query(
            sql="SELECT id, username, password FROM USERS WHERE username = :username",
            parameters={"username": username}
        )

        if not resultado:
            print("No hay coincidencias")
            return None

        stored = resultado[0][2]
        try:
            hashed_password = bytes.fromhex(stored)
        except Exception:
            print("Formato de contraseña inválido")
            return None

        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            print("Logeado correctamente")
            return (resultado[0][0], resultado[0][1])
        else:
            print("Contraseña incorrecta")
            return None

    @staticmethod
    def register(db: Database, username: str, password: str):
        # generar id siguiente
        res = db.query("SELECT MAX(id) FROM USERS")
        next_id = 1
        try:
            if res and res[0] and res[0][0] is not None:
                next_id = int(res[0][0]) + 1
        except Exception:
            next_id = 1

        # hashear contraseña de forma segura
        password_bytes = password.encode("utf-8")
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(12)).hex()

        db.query(
            sql="INSERT INTO USERS(id, username, password) VALUES (:id, :username, :password)",
            parameters={"id": next_id, "username": username, "password": hashed}
        )
        print("usuario registrado con exito")


class Finance:
    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url

    def get_indicator(self, indicator: str, fecha: str = None) -> float:
        try:
            if not fecha:
                dd = datetime.datetime.now().day
                mm = datetime.datetime.now().month
                yyyy = datetime.datetime.now().year
                fecha = f"{dd}-{mm}-{yyyy}"
            url = f"{self.base_url}/{indicator}/{fecha}"
            respuesta = requests.get(url).json()
            return respuesta["serie"][0]["valor"]
        except Exception:
            print("Hubo un error con la solicitud")
            return None

    def get_usd(self, fecha: str = None):
        return self.get_indicator("dolar", fecha)

    def get_eur(self, fecha: str = None):
        return self.get_indicator("euro", fecha)

    def get_uf(self, fecha: str = None):
        return self.get_indicator("uf", fecha)

    def get_ivp(self, fecha: str = None):
        return self.get_indicator("ivp", fecha)

    def get_ipc(self, fecha: str = None):
        return self.get_indicator("ipc", fecha)

    def get_utm(self, fecha: str = None):
        return self.get_indicator("utm", fecha)


def record_query(db: Database, user_id: int, username: str, opcion: str):
    # insertar registro de consulta en Consulta_users
    try:
        res = db.query("SELECT MAX(id) FROM Consulta_users")
        next_id = 1
        try:
            if res and res[0] and res[0][0] is not None:
                next_id = int(res[0][0]) + 1
        except Exception:
            next_id = 1

        db.query(
            "INSERT INTO Consulta_users(id, user_id, username, fecha_consulta, opcion) VALUES(:id, :user_id, :username, :fecha_consulta, :opcion)",
            {"id": next_id, "user_id": user_id, "username": username, "fecha_consulta": datetime.datetime.now().isoformat(), "opcion": opcion}
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    db = Database(
        username=os.getenv("ORACLE_USER"),
        dsn=os.getenv("ORACLE_DSN"),
        password=os.getenv("ORACLE_PASSWORD")
    )

    # crear tablas si no existen
    try:
        db.create_all_tables()
    except Exception:
        pass

    finance = Finance()

    while True:
        print("\n==========================================")
        print("|         ⚆_⚆ Menú Principal             |")
        print("==========================================")
        print("| 1. Registrar                           |")
        print("| 2. Login                               |")
        print("| 0. Salir                               |")
        print("==========================================")
        opt = input("Seleccione una opción: ").strip()
        if opt == '1':
            usuario = input("Nombre de usuario: ").strip()
            if not usuario:
                print("El nombre no debe estar vacío")
                continue
            contrasena = input("Contraseña: ")
            # registrar con contraseña segura (hash)
            Auth.register(db, usuario, contrasena)
        elif opt == '2':
            usuario = input("Usuario: ").strip()
            contrasena = input("Contraseña: ")
            logged = Auth.login(db, usuario, contrasena)
            if not logged:
                continue
            user_id, username = logged
            # sub menú
            while True:
                print("\n==========================================")
                print(f"|         ⚆_⚆ Menú Consultas - {username}|")
                print("==========================================")
                print("| 1. Dólar                               |")
                print("| 2. Euro                                |")
                print("| 3. UF                                  |")
                print("| 4. IVP                                 |")
                print("| 5. IPC                                 |")
                print("| 6. UTM                                 |")
                print("| 0. Volver                              |")
                print("==========================================")
                o = input("Seleccione opción del submenú: ").strip()
                mapping = {
                    '1': ('dolar', finance.get_usd, 'Dólar'),
                    '2': ('euro', finance.get_eur, 'Euro'),
                    '3': ('uf', finance.get_uf, 'UF'),
                    '4': ('ivp', finance.get_ivp, 'IVP'),
                    '5': ('ipc', finance.get_ipc, 'IPC'),
                    '6': ('utm', finance.get_utm, 'UTM')
                }
                if o == '0':
                    break
                if o not in mapping:
                    print("Opción inválida")
                    continue
                key, func, display = mapping[o]
                tipo = input('¿Consulta por rango? (s/n): ').strip().lower()
                if tipo == 's' or tipo == 'si' or tipo == 'sí':
                    start = input('Fecha inicio (YYYY-MM-DD): ').strip()
                    end = input('Fecha fin (YYYY-MM-DD): ').strip()
                    # iterar por rango (simple, no validaciones extensas)
                    try:
                        sdate = datetime.datetime.strptime(start, '%Y-%m-%d').date()
                        edate = datetime.datetime.strptime(end, '%Y-%m-%d').date()
                    except Exception:
                        print('Fechas inválidas')
                        continue
                    cur = sdate
                    while cur <= edate:
                        fecha_i = cur.strftime('%Y-%m-%d')
                        valor = None
                        try:
                            valor = finance.get_indicator(key, fecha_i)
                        except Exception:
                            valor = None
                        # mostrar resultado según requerimiento
                        print(f'El valor de "{display}" "{start} a {end}" es de "{valor}"')
                        # registrar consulta
                        record_query(db, user_id, username, display)
                        cur = cur + datetime.timedelta(days=1)
                else:
                    fecha = input('Fecha (YYYY-MM-DD) o enter para hoy: ').strip()
                    if not fecha:
                        fecha = datetime.datetime.now().strftime('%d-%m-%Y')
                    valor = None
                    try:
                        valor = finance.get_indicator(key, fecha)
                    except Exception:
                        valor = None
                    print(f'El valor de "{display}" "{fecha}" es de "{valor}"')
                    record_query(db, user_id, username, display)
        elif opt == '0':
            break
        else:
            print("Opción inválida")

            