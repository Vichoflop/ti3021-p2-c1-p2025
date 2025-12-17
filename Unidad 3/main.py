#conexion a base de datos
try:
    import oracledb
except Exception:
    oracledb = None
import os
from dotenv import load_dotenv

#Haseheo de contraseñas
import bcrypt

#Consumo de API
import requests
import sys

#parametros opcionales
from typing import Optional

#Cargar las variables desde el archivo.env
load_dotenv()

#Cargar fechas
import datetime
import json
from pathlib import Path
import re

class Database:
    def __init__(self, username, dsn, password):
        self.username = username
        self.dsn = dsn
        self.password = password
    def get_connection(self):
        if oracledb is None:
            raise RuntimeError("oracledb no está disponible. Instale la dependencia o use el almacenamiento local.")
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
    def create_all_tables(self):
        tables = [
            (
                "CREATE TABLE USERS("
                "id INTEGER PRIMARY KEY,"
                "username VARCHAR(32) UNIQUE,"
                "password VARCHAR(128)"
                ")"
            )
        ]

        for table in tables:
            self.query(table)

    def query(self, sql: str, parameters: Optional[dict] = None):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    ejecucion = cur.execute(sql, parameters)
                    if sql.startswith("SELECT"):
                        resultado = []
                        for fila in ejecucion:
                            resultado.append(fila)
                        return resultado
                conn.commit()
        except oracledb.DatabaseError as error:
            print(error)

class Auth:
    @staticmethod
    def login(db: Database, username: str, password: str) -> bool:
        """Intenta autenticar contra la base de datos. Devuelve True si OK, False si falla."""
        password = password.encode("UTF-8")

        resultado = db.query(
            sql= "SELECT * FROM USERS WHERE username = :username",
            parameters={"username":username}
        )

        if not resultado:
            print("No hay coincidencias")
            return False
        try:
            hashed_password = bytes.fromhex(resultado[0][2])
        except Exception:
            print("Formato de password inválido en la base de datos.")
            return False

        if bcrypt.checkpw(password, hashed_password):
            print("Logeado correctamente")
            return True
        else:
            print("Contraseña incorrecta")
            return False

    @staticmethod
    def register(db: Database, id: int, username: str, password: str):
        print("registrando usuario")
        password = password.encode("UTF-8")
        salt = bcrypt.gensalt(12)
        hash_password = bcrypt.hashpw(password,salt)

        usuario = {
            "id": id,
            "username": username,
            "password": hash_password
        }

        db.query(
            sql= "INSERT INTO USERS(id,username,password) VALUES (:id, :username, :password)",
            parameters=usuario
        )
        print("usuario registrado con exito")

class Finance:
    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url
    def _call_api(self, indicator: str, fecha: str):
        url = f"{self.base_url}/{indicator}/{fecha}"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_indicator(self, indicator: str, fecha: str = None):
        """Devuelve el valor del indicador para la fecha (YYYY-MM-DD) o None si falla."""
        try:
            if not fecha:
                fecha = datetime.datetime.now().strftime("%Y-%m-%d")
            data = self._call_api(indicator, fecha)
            # la API devuelve una 'serie' con elementos; tomamos el primero si existe
            serie = data.get("serie", [])
            if not serie:
                return None
            return serie[0].get("valor")
        except Exception:
            return None

    def get_indicator_range(self, indicator: str, start_date: str, end_date: str):
        """Devuelve lista de {fecha, valor} entre start_date y end_date (incluidos)."""
        try:
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        except Exception:
            raise ValueError("Fechas deben estar en formato YYYY-MM-DD")
        if start > end:
            raise ValueError("start_date debe ser anterior o igual a end_date")

        results = []
        cur = start
        while cur <= end:
            fecha = cur.strftime("%Y-%m-%d")
            valor = self.get_indicator(indicator, fecha)
            results.append({"fecha": fecha, "valor": valor})
            cur = cur + datetime.timedelta(days=1)
        return results

    # Métodos específicos que devuelven valores (no imprimen)
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

if __name__ == "__main__":
    # Archivo local para almacenar usuarios cuando no se use la BD
    USERS_FILE = Path(__file__).parent / "users.json"

    def load_users():
        if not USERS_FILE.exists():
            return {}
        try:
            data = json.loads(USERS_FILE.read_text(encoding="utf-8"))
            # Asegurarse estructura por usuario
            if isinstance(data, dict):
                for u, v in list(data.items()):
                    if isinstance(v, str):
                        # formato antiguo: solo hash -> migrar
                        data[u] = {"password": v, "created_at": None, "role": "user", "failed_attempts": 0, "locked_until": None}
                    else:
                        v.setdefault("role", "user")
                        v.setdefault("failed_attempts", 0)
                        v.setdefault("locked_until", None)
                return data
            return {}
        except Exception:
            return {}

    def save_users(users: dict):
        USERS_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")

    # Archivo para registrar las consultas de indicadores (log local)
    LOG_FILE = Path(__file__).parent / "indicators_log.json"

    def load_indicator_log():
        if not LOG_FILE.exists():
            return []
        try:
            return json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []

    def save_indicator_log(entries):
        LOG_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")

    def record_indicator_log(indicator_name: str, fecha_valor: str, valor, username: str, provider: str = "mindicador.cl"):
        entries = load_indicator_log()
        next_id = 1
        if entries:
            try:
                next_id = max((e.get("id", 0) for e in entries)) + 1
            except Exception:
                next_id = len(entries) + 1
        entry = {
            "id": next_id,
            "indicator": indicator_name,
            "fecha_valor": fecha_valor,
            "valor": valor,
            "fecha_consulta": datetime.datetime.now().isoformat(),
            "username": username,
            "provider": provider
        }
        entries.append(entry)
        save_indicator_log(entries)

    def is_password_strong(password: str) -> bool:
        # Reglas de fuerza mínima: 8+ caracteres, mayúscula, minúscula, número y caracter especial
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[^A-Za-z0-9]", password):
            return False
        return True

    def register_user(current_user: str = None):
        users = load_users()
        while True:
            username = input("Ingrese nombre de usuario: ").strip()
            if username == "":
                print("El nombre de usuario no puede estar vacío.")
                continue
            if username in users:
                print("El usuario ya existe. Elija otro nombre.")
                continue
            break

        while True:
            password = input("Ingrese contraseña: ")
            if not is_password_strong(password):
                print("Contraseña débil. Debe tener al menos 8 caracteres, incluir mayúscula, minúscula, número y símbolo.")
                continue
            password_confirm = input("Confirme la contraseña: ")
            if password != password_confirm:
                print("Las contraseñas no coinciden.")
                continue
            break

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))
        # determinar rol: si no hay usuarios existentes, primer usuario será admin
        if len(users) == 0:
            role = "admin"
            print("Se crea el primer usuario: rol asignado = admin")
        else:
            # si es llamado por un admin autenticado, permitir elegir rol
            role = "user"
            if current_user:
                cu = users.get(current_user, {})
                if cu.get("role") == "admin":
                    chosen = input("Asignar rol al nuevo usuario ('user' o 'admin') [user]: ").strip().lower()
                    if chosen in ("user", "admin"):
                        role = chosen

        users[username] = {
            "password": hashed.hex(),
            "created_at": datetime.datetime.now().isoformat(),
            "role": role,
            "failed_attempts": 0,
            "locked_until": None
        }
        save_users(users)
        print(f"Usuario '{username}' registrado con éxito (role={role}).")
        return username

    def login_user() -> str:
        users = load_users()
        username = input("Usuario: ").strip()
        if username not in users:
            print("Usuario no encontrado.")
            return ""
        user = users[username]

        # Intentos de contraseña en esta sesión
        MAX_SESSION_ATTEMPTS = 3
        for attempt in range(1, MAX_SESSION_ATTEMPTS + 1):
            password = input("Contraseña: ")
            try:
                hashed = bytes.fromhex(user["password"])
            except Exception:
                print("Error en el formato de la contraseña almacenada.")
                return ""

            if bcrypt.checkpw(password.encode("utf-8"), hashed):
                print(f"Bienvenido {username}")
                # resetear contadores de la cuenta
                user["failed_attempts"] = 0
                user["locked_until"] = None
                save_users(users)
                return username
            else:
                remaining = MAX_SESSION_ATTEMPTS - attempt
                if remaining > 0:
                    print(f"Contraseña incorrecta. Intentos restantes: {remaining}")
                else:
                    print("Ha excedido el número máximo de intentos. Finalizando programa.")
                    sys.exit(0)
        return ""

    def user_menu(username: str):
        finance = Finance()
        users = load_users()
        role = users.get(username, {}).get("role", "user")

        def ask_single_or_range():
            # Pregunta simple: 's' para rango, cualquier otra para fecha única
            ans = input("¿Desea consultar un rango de fechas? (s/n): ").strip().lower()
            if ans == 's' or ans == 'si' or ans == 'sí':
                return '2'
            return '1'

        def read_date(prompt):
            d = input(prompt).strip()
            if d == "":
                return None
            try:
                datetime.datetime.strptime(d, "%Y-%m-%d")
                return d
            except Exception:
                print("Formato inválido. Use YYYY-MM-DD")
                return None

        while True:
            print("\n--- Menú de usuario ---")
            print("1. Ver valor del Dólar ")
            print("2. Ver valor del Euro")
            print("3. Ver valor de la UF")
            print("4. Ver valor del IVP")
            print("5. Ver valor del IPC")
            print("6. Ver valor del UTM")
            if role == "admin":
                print("7. Crear nuevo usuario (admin)")
            print("0. Cerrar sesión")
            opcion = input("Seleccione una opción: ").strip()

            if opcion in ("1","2","3","4","5","6"):
                mapping = {
                    "1": ("dolar", finance.get_usd),
                    "2": ("euro", finance.get_eur),
                    "3": ("uf", finance.get_uf),
                    "4": ("ivp", finance.get_ivp),
                    "5": ("ipc", finance.get_ipc),
                    "6": ("utm", finance.get_utm),
                }
                display_names = {
                    "dolar": "Dólar Observado",
                    "euro": "Euro",
                    "uf": "Unidad de Fomento (UF)",
                    "ivp": "Índice de Valor Promedio (IVP)",
                    "ipc": "Índice de Precios al Consumidor (IPC)",
                    "utm": "Unidad Tributaria Mensual (UTM)"
                }
                indicator_key, func = mapping[opcion]
                mode = ask_single_or_range()
                if mode == "1":
                    # Si no se desea rango, usar automáticamente la fecha de hoy
                    d = datetime.datetime.now().strftime("%Y-%m-%d")
                    valor = func(d)
                    if valor is None:
                        print(f'El valor de "{display_names.get(indicator_key)}" el día "{d}" fue "No disponible"')
                    else:
                        print(f'El valor de "{display_names.get(indicator_key)}" el día "{d}" fue "{valor}"')
                    # Registrar la consulta en el log local
                    try:
                        record_indicator_log(indicator_key, d, valor, username)
                    except Exception:
                        pass
                elif mode == "2":
                    s = None
                    e = None
                    while s is None:
                        s = read_date("Ingrese fecha inicio (YYYY-MM-DD): ")
                    while e is None:
                        e = read_date("Ingrese fecha fin (YYYY-MM-DD): ")
                    try:
                        lista = finance.get_indicator_range(indicator_key, s, e)
                        for item in lista:
                            val = item.get("valor")
                            fecha_item = item.get('fecha')
                            if val is None:
                                print(f'El valor de "{display_names.get(indicator_key)}" el día "{fecha_item}" fue "No disponible"')
                            else:
                                print(f'El valor de "{display_names.get(indicator_key)}" el día "{fecha_item}" fue "{val}"')
                            # Registrar cada resultado en el log local
                            try:
                                record_indicator_log(indicator_key, fecha_item, val, username)
                            except Exception:
                                pass
                    except Exception as ex:
                        print(f"Error en consulta por rango: {ex}")
                else:
                    print("Modo inválido")
            elif opcion == "7" and role == "admin":
                newu = register_user(current_user=username)
                if newu:
                    print(f"Usuario {newu} creado.")
            elif opcion == "0":
                print("Cerrando sesión...")
                break
            else:
                print("Opción inválida.")

    # Menú principal
    while True:
        print("\n=== Menú Principal ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            user = register_user()
            if user:
                user_menu(user)
        elif opcion == "2":
            user = login_user()
            if user:
                user_menu(user)
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")