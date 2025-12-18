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
        try:
            return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
        except oracledb.DatabaseError as error:
            print(f"Error connecting to the database: {error}")
            raise

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
            except Exception as e:
                print(f"Error creating table: {e}")

    def query(self, sql: str, parameters: Optional[dict] = None):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    ejecucion = cur.execute(sql, parameters or {})
                    if sql.strip().upper().startswith("SELECT"):
                        return [fila for fila in ejecucion]
                conn.commit()
        except oracledb.DatabaseError as error:
            print(f"Database query error: {error}")
            return None


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
        except ValueError:
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
        res = db.query("SELECT MAX(id) FROM USERS")
        next_id = 1
        if res and res[0] and res[0][0] is not None:
            next_id = int(res[0][0]) + 1

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12)).hex()

        db.query(
            sql="INSERT INTO USERS(id, username, password) VALUES (:id, :username, :password)",
            parameters={"id": next_id, "username": username, "password": hashed}
        )
        print("Usuario registrado con éxito")


class Finance:
    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url

    def get_indicator(self, indicator: str, fecha: str = None) -> Optional[float]:
        try:
            if not fecha:
                dd= datetime.datetime.now().day
                mm = datetime.datetime.now().month
                yyyy= datetime.datetime.now().year
                fecha = f"{dd:02d}-{mm:02d}-{yyyy}"
            url = f"{self.base_url}/{indicator}/{fecha}"
            print(url)
            respuesta = requests.get(url).json()
            print(respuesta)
            return respuesta["serie"][0]["valor"]
        except Exception as e:
            print(f"Error fetching indicator: {e}")
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
    try:
        res = db.query("SELECT MAX(id) FROM Consulta_users")
        next_id = 1
        if res and res[0] and res[0][0] is not None:
            next_id = int(res[0][0]) + 1

        db.query(
            "INSERT INTO Consulta_users(id, user_id, username, fecha_consulta, opcion) VALUES(:id, :user_id, :username, :fecha_consulta, :opcion)",
            {"id": next_id, "user_id": user_id, "username": username, "fecha_consulta": datetime.datetime.now().isoformat(), "opcion": opcion}
        )
    except Exception as e:
        print(f"Error recording query: {e}")


def Consulta_users(db: Database, user_id: int = None):
    """Muestra los registros de consultas.
    Si se entrega `user_id`, muestra solo las consultas de ese usuario; si no, muestra todas.
    """
    try:
        if user_id is not None:
            rows = db.query(
                "SELECT id, user_id, username, fecha_consulta, opcion FROM Consulta_users WHERE user_id = :uid ORDER BY id",
                {"uid": user_id}
            )
        else:
            rows = db.query("SELECT id, user_id, username, fecha_consulta, opcion FROM Consulta_users ORDER BY id")

        if not rows:
            print("No hay consultas registradas.")
            return

        print("\n-- Registro de Consultas --")
        for r in rows:
            print(f"ID: {r[0]} | UserID: {r[1]} | Usuario: {r[2]} | Fecha: {r[3]} | Opción: {r[4]}")
        print("-- Fin del registro --\n")
    except Exception as e:
        print(f"Error fetching consultas: {e}")


def validate_date_input(date_str: str) -> Optional[datetime.date]:
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print("Fecha inválida. Use el formato YYYY-MM-DD.")
        return None


if __name__ == "__main__":
    # Load database credentials
    load_dotenv()  # Ensure this is called to load environment variables
    oracle_user = os.getenv("ORACLE_USER")
    oracle_dsn = os.getenv("ORACLE_DSN")
    oracle_password = os.getenv("ORACLE_PASSWORD")

    # Debugging: Print loaded credentials
    print("ORACLE_USER:", oracle_user)
    print("ORACLE_DSN:", oracle_dsn)
    print("ORACLE_PASSWORD:", oracle_password)

    # Validate credentials
    if not all([oracle_user, oracle_dsn, oracle_password]):
        print("Error: Missing database credentials. Please check your .env file.")
        exit(1)

    db = Database(
        username=oracle_user,
        dsn=oracle_dsn,
        password=oracle_password
    )

    try:
        db.create_all_tables()
    except Exception as e:
        print(f"Error initializing database: {e}")

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
            Auth.register(db, usuario, contrasena)
        elif opt == '2':
            usuario = input("Usuario: ").strip()
            contrasena = input("Contraseña: ")
            logged = Auth.login(db, usuario, contrasena)
            if not logged:
                continue
            user_id, username = logged
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
                print("| 7. Consultas de Usuario                |")
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
                if o == '7':
                    Consulta_users(db, user_id)
                    continue
                if o not in mapping:
                    print("Opción inválida")
                    continue
                key, func, display = mapping[o]
                tipo = input('¿Consulta por rango? (s/n): ').strip().lower()
                if tipo in ['s', 'si', 'sí']:
                    start = input('Fecha inicio (YYYY-MM-DD): ').strip()
                    end = input('Fecha fin (YYYY-MM-DD): ').strip()
                    sdate = validate_date_input(start)
                    edate = validate_date_input(end)
                    if not sdate or not edate:
                        continue
                    cur = sdate
                    while cur <= edate:
                        fecha_i = cur.strftime('%Y-%m-%d')
                        valor = finance.get_indicator(key, fecha_i)
                        print(f'El valor de "{display}" "{fecha_i}" es de "{valor}"')
                        record_query(db, user_id, username, display)
                        cur += datetime.timedelta(days=1)
                else:
                    fecha = input('Fecha (YYYY-MM-DD) o enter para hoy: ').strip()
                    valor = finance.get_indicator(key, fecha)
                    print(f'El valor de "{display}" "{fecha}" es de "{valor}"')
                    record_query(db, user_id, username, display)
        elif opt == '0':
            break
        else:
            print("Opción inválida")


