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
                "username VARCHAR2(32) UNIQUE,"
                "password VARCHAR2(512)"
                ")"
            ),
            (
                "CREATE TABLE Consulta_users("
                "id INTEGER PRIMARY KEY,"
                "user_id INTEGER,"
                "username VARCHAR2(32),"
                "fecha_consulta VARCHAR2(64),"
                "fecha_dato VARCHAR2(64),"
                "opcion VARCHAR2(64),"
                "valor VARCHAR2(64)"
                ")"
            )
        ]

        for table in tables:
            try:
                self.query(table)
                print(f"✓ Tabla creada exitosamente")
            except Exception as e:
                print(f"La tabla ya existe o error: {e}")
    
    def migrate_consulta_table(self):
        """Agrega las columnas nuevas si la tabla existe pero le faltan columnas"""
        try:
            # Intenta agregar las columnas nuevas
            self.query("ALTER TABLE Consulta_users ADD fecha_dato VARCHAR2(64)")
            print("✓ Columna 'fecha_dato' agregada")
        except:
            pass  # La columna ya existe
        
        try:
            self.query("ALTER TABLE Consulta_users ADD valor VARCHAR2(64)")
            print("✓ Columna 'valor' agregada")
        except:
            pass  # La columna ya existe
    
    def drop_all_tables(self):
        """Elimina todas las tablas (¡CUIDADO! Borra todos los datos)"""
        tables = ["Consulta_users", "USERS"]
        for table in tables:
            try:
                self.query(f"DROP TABLE {table}")
                print(f"✓ Tabla {table} eliminada")
            except Exception as e:
                pass  # La tabla no existe

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
            print("❌ No hay coincidencias")
            return None

        stored = resultado[0][2]
        try:
            hashed_password = bytes.fromhex(stored)
        except ValueError:
            print("❌ Formato de contraseña inválido")
            return None

        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            print("✓ Logeado correctamente")
            return (resultado[0][0], resultado[0][1])
        else:
            print("❌ Contraseña incorrecta")
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
        print("✓ Usuario registrado con éxito")


class Finance:
    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url

    def get_indicator(self, indicator: str, fecha: str = None) -> Optional[dict]:
        """
        Obtiene un indicador específico.
        Retorna un diccionario con valor, fecha y nombre, o None si falla.
        """
        try:
            if not fecha:
                dd = datetime.datetime.now().day
                mm = datetime.datetime.now().month
                yyyy = datetime.datetime.now().year
                fecha = f"{dd:02d}-{mm:02d}-{yyyy}"
            
            url = f"{self.base_url}/{indicator}/{fecha}"
            respuesta = requests.get(url)
            respuesta.raise_for_status()
            data = respuesta.json()
            
            if "serie" in data and len(data["serie"]) > 0:
                return {
                    "valor": data["serie"][0]["valor"],
                    "fecha": data["serie"][0]["fecha"][:10],  # Solo la fecha YYYY-MM-DD
                    "nombre": data.get("nombre", indicator.upper())
                }
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud HTTP: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"Error al procesar los datos: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None

    def get_usd(self, fecha: str = None):
        result = self.get_indicator("dolar", fecha)
        return result["valor"] if result else None

    def get_eur(self, fecha: str = None):
        result = self.get_indicator("euro", fecha)
        return result["valor"] if result else None

    def get_uf(self, fecha: str = None):
        result = self.get_indicator("uf", fecha)
        return result["valor"] if result else None

    def get_ivp(self, fecha: str = None):
        result = self.get_indicator("ivp", fecha)
        return result["valor"] if result else None

    def get_ipc(self, fecha: str = None):
        result = self.get_indicator("ipc", fecha)
        return result["valor"] if result else None

    def get_utm(self, fecha: str = None):
        result = self.get_indicator("utm", fecha)
        return result["valor"] if result else None


def record_query(db: Database, user_id: int, username: str, opcion: str, fecha_dato: str = None, valor: float = None):
    """
    Registra una consulta del usuario en la base de datos.
    
    Args:
        db: Instancia de la base de datos
        user_id: ID del usuario
        username: Nombre del usuario
        opcion: Tipo de indicador consultado (Dólar, Euro, etc.)
        fecha_dato: Fecha del dato consultado (opcional)
        valor: Valor obtenido (opcional)
    """
    try:
        res = db.query("SELECT MAX(id) FROM Consulta_users")
        next_id = 1
        if res and res[0] and res[0][0] is not None:
            next_id = int(res[0][0]) + 1

        fecha_consulta = datetime.datetime.now().isoformat()
        fecha_dato_str = fecha_dato if fecha_dato else "N/A"
        valor_str = str(valor) if valor is not None else "N/A"

        db.query(
            "INSERT INTO Consulta_users(id, user_id, username, fecha_consulta, fecha_dato, opcion, valor) "
            "VALUES(:id, :user_id, :username, :fecha_consulta, :fecha_dato, :opcion, :valor)",
            {
                "id": next_id, 
                "user_id": user_id, 
                "username": username, 
                "fecha_consulta": fecha_consulta, 
                "fecha_dato": fecha_dato_str,
                "opcion": opcion,
                "valor": valor_str
            }
        )
    except Exception as e:
        print(f"Error recording query: {e}")


def consulta_users(db: Database, user_id: int = None):
    """
    Muestra los registros de consultas.
    Si se entrega `user_id`, muestra solo las consultas de ese usuario; si no, muestra todas.
    
    Args:
        db: Instancia de la base de datos
        user_id: ID del usuario (opcional). Si es None, muestra todas las consultas.
    
    Returns:
        list: Lista de diccionarios con las consultas, o lista vacía si no hay registros.
    """
    try:
        if user_id is not None:
            rows = db.query(
                "SELECT id, user_id, username, fecha_consulta, fecha_dato, opcion, valor "
                "FROM Consulta_users WHERE user_id = :user_id_param ORDER BY id DESC",
                {"user_id_param": user_id}
            )
        else:
            rows = db.query(
                "SELECT id, user_id, username, fecha_consulta, fecha_dato, opcion, valor "
                "FROM Consulta_users ORDER BY id DESC"
            )

        if not rows:
            print("\n📋 No hay consultas registradas.\n")
            return []

        # Convertir tuplas a diccionarios
        consultas = []
        for row in rows:
            consulta = {
                'id': row[0],
                'user_id': row[1],
                'username': row[2],
                'fecha_consulta': row[3],
                'fecha_dato': row[4],
                'opcion': row[5],
                'valor': row[6]
            }
            consultas.append(consulta)

        # Mostrar resultados
        print("\n" + "="*70)
        print("📊 HISTORIAL DE CONSULTAS".center(70))
        print("="*70)
        
        for i, c in enumerate(consultas, 1):
            # Formatear fecha de consulta
            try:
                fecha_consulta_obj = datetime.datetime.fromisoformat(c['fecha_consulta'])
                fecha_consulta_fmt = fecha_consulta_obj.strftime('%d/%m/%Y %H:%M:%S')
            except:
                fecha_consulta_fmt = c['fecha_consulta']
            
            print(f"\n🔍 Consulta #{i}")
            print(f"   ID: {c['id']} | Usuario: {c['username']} (ID: {c['user_id']})")
            print(f"   Indicador: {c['opcion']}")
            print(f"   Fecha consultada: {fecha_consulta_fmt}")
            if c['fecha_dato'] != 'N/A':
                print(f"   Fecha del dato: {c['fecha_dato']}")
            if c['valor'] != 'N/A':
                # Formatear valor con separador de miles
                try:
                    valor_float = float(c['valor'])
                    print(f"   Valor: ${valor_float:,.2f}")
                except:
                    print(f"   Valor: {c['valor']}")
            print("-" * 70)
        
        print(f"\n📈 Total de consultas: {len(consultas)}\n")
        
        return consultas
        
    except Exception as e:
        print(f"❌ Error al obtener consultas: {e}")
        return []


def validate_date_input(date_str: str) -> Optional[datetime.date]:
    """Valida que la fecha esté en formato correcto."""
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print("❌ Fecha inválida. Use el formato YYYY-MM-DD.")
        return None


if __name__ == "__main__":
    # Load database credentials
    load_dotenv()
    oracle_user = os.getenv("ORACLE_USER")
    oracle_dsn = os.getenv("ORACLE_DSN")
    oracle_password = os.getenv("ORACLE_PASSWORD")

    # Validate credentials
    if not all([oracle_user, oracle_dsn, oracle_password]):
        print("❌ Error: Faltan credenciales de la base de datos. Revise su archivo .env")
        exit(1)

    db = Database(
        username=oracle_user,
        dsn=oracle_dsn,
        password=oracle_password
    )

    print("\n🔧 Inicializando base de datos...")
    
    # Migrar tabla existente (mantiene datos)
    try:
        db.migrate_consulta_table()
        db.create_all_tables()  # Crea las que no existen
        print("✓ Base de datos lista\n")
    except Exception as e:
        print(f"Error initializing database: {e}")
    
    # Opción para recrear todo desde cero (descomentar si necesitas empezar de cero)
    # print("⚠️  ADVERTENCIA: Se eliminarán todos los datos")
    # respuesta = input("¿Recrear tablas desde cero? (escribe SI para confirmar): ")
    # if respuesta == "SI":
    #     db.drop_all_tables()
    #     db.create_all_tables()
    #     print("✓ Tablas recreadas\n")

    finance = Finance()

    while True:
        print("\n==========================================")
        print("|         💰 Menú Principal              |")
        print("==========================================")
        print("| 1. Registrar                           |")
        print("| 2. Login                               |")
        print("| 0. Salir                               |")
        print("==========================================")
        opt = input("Seleccione una opción: ").strip()
        
        if opt == '1':
            usuario = input("Nombre de usuario: ").strip()
            if not usuario:
                print("❌ El nombre no debe estar vacío")
                continue
            contrasena = input("Contraseña: ")
            if not contrasena:
                print("❌ La contraseña no debe estar vacía")
                continue
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
                print(f"|   📊 Menú Consultas - {username:<12}|")
                print("==========================================")
                print("| 1. Dólar (USD)                         |")
                print("| 2. Euro (EUR)                          |")
                print("| 3. UF                                  |")
                print("| 4. IVP                                 |")
                print("| 5. IPC                                 |")
                print("| 6. UTM                                 |")
                print("| 7. Ver Historial de Consultas          |")
                print("| 0. Cerrar Sesión                       |")
                print("==========================================")
                o = input("Seleccione opción: ").strip()
                
                mapping = {
                    '1': ('dolar', 'Dólar'),
                    '2': ('euro', 'Euro'),
                    '3': ('uf', 'UF'),
                    '4': ('ivp', 'IVP'),
                    '5': ('ipc', 'IPC'),
                    '6': ('utm', 'UTM')
                }
                
                if o == '0':
                    print(f"👋 Hasta luego, {username}!")
                    break
                    
                if o == '7':
                    consulta_users(db, user_id)
                    # Registrar que el usuario vio su historial
                    record_query(db, user_id, username, "Ver Historial")
                    input("\nPresione Enter para continuar...")
                    continue
                    
                if o not in mapping:
                    print("❌ Opción inválida")
                    continue
                    
                key, display = mapping[o]
                tipo = input('¿Consulta por rango de fechas? (s/n): ').strip().lower()
                
                if tipo in ['s', 'si', 'sí', 'yes', 'y']:
                    start = input('Fecha inicio (YYYY-MM-DD): ').strip()
                    end = input('Fecha fin (YYYY-MM-DD): ').strip()
                    sdate = validate_date_input(start)
                    edate = validate_date_input(end)
                    
                    if not sdate or not edate:
                        continue
                        
                    if sdate > edate:
                        print("❌ La fecha de inicio debe ser anterior a la fecha de fin")
                        continue
                    
                    print(f"\n📈 Consultando {display} del {start} al {end}...")
                    print("-" * 50)
                    
                    cur = sdate
                    consultas_exitosas = 0
                    valores_obtenidos = []
                    
                    while cur <= edate:
                        fecha_str = cur.strftime('%d-%m-%Y')
                        resultado = finance.get_indicator(key, fecha_str)
                        
                        if resultado and resultado.get("valor") is not None:
                            valor = resultado["valor"]
                            fecha_dato = resultado["fecha"]
                            print(f'📅 {cur.strftime("%d/%m/%Y")} | {display}: ${valor:,.2f}')
                            record_query(db, user_id, username, display, fecha_dato, valor)
                            consultas_exitosas += 1
                            valores_obtenidos.append(valor)
                        else:
                            print(f'⚠️  {cur.strftime("%d/%m/%Y")} | Sin datos disponibles')
                            
                        cur += datetime.timedelta(days=1)
                    
                    print("-" * 50)
                    if valores_obtenidos:
                        promedio = sum(valores_obtenidos) / len(valores_obtenidos)
                        print(f"📊 Promedio: ${promedio:,.2f}")
                        print(f"📈 Valor máximo: ${max(valores_obtenidos):,.2f}")
                        print(f"📉 Valor mínimo: ${min(valores_obtenidos):,.2f}")
                    print(f"✓ Se registraron {consultas_exitosas} consultas en su historial\n")
                    input("\nPresione Enter para continuar...")
                    
                else:
                    fecha_input = input('Fecha (YYYY-MM-DD) o presione Enter para hoy: ').strip()
                    
                    if fecha_input:
                        fecha_validada = validate_date_input(fecha_input)
                        if not fecha_validada:
                            continue
                        fecha_str = fecha_validada.strftime('%d-%m-%Y')
                        fecha_display = fecha_input
                    else:
                        fecha_str = None
                        fecha_display = "hoy"
                    
                    resultado = finance.get_indicator(key, fecha_str)
                    
                    if resultado and resultado.get("valor") is not None:
                        valor = resultado["valor"]
                        fecha_dato = resultado["fecha"]
                        print(f'\n💵 El valor de {display} para {fecha_display} es: ${valor:,.2f}')
                        print(f'📅 Fecha del dato: {fecha_dato}\n')
                        record_query(db, user_id, username, display, fecha_dato, valor)
                    else:
                        print(f'\n❌ No se pudo obtener el valor de {display}\n')
                    
                    input("\nPresione Enter para continuar...")
                        
        elif opt == '0':
            print("👋 ¡Hasta pronto!")
            break
        else:
            print("❌ Opción inválida")
