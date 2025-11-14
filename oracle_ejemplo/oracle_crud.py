import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

username= os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(user = username, password = password, dsn = dsn)

def create_schema(query):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                print(f"Tabla creada \n {query}")
    except oracledb.DatabaseError as error:
        print(f"No se pudo crear la tabla: {error}")

tables = [
    (
        "CREATE TABLE"
        "Usuarios ("
        "id_usuario INTEGER PRIMARY KEY,"
        "nombres VARCHAR2(64),"
        "apellidos VARCHAR2(64),"
        "Rut Varchar2(12),"
        "correo varchar2(50)"
        ")"
    ),
    (
        "CREATE TABLE"
        "Estudiantes ("
        "id_estudiante INTEGER PRIMARY KEY,"
        "id_usuario INTEGER,"
        "PrestamosActivos INTEGER NOT NULL,"
        "EstadoDeuda VARCHAR2(50) NOT NULL,"
        "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)"
        ")"
    ),
    (
        "CREATE TABLE"
        "Docentes ("
        "id_docente INTEGER PRIMARY KEY,"
        "id_usuario INTEGER,"
        "MaterialExclusivoAccedido VARCHAR2(50) NOT NULL,"
        "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)"
        ")"
    ),
    (
        "CREATE TABLE"
        "Investigadores ("
        "id_investigador INTEGER PRIMARY KEY,"
        "NivelAcceso VARCHAR2(50) NOT NULL"
        ")"
    ),
    (
        "CREATE TABLE"
        "lIBROS ("
        "id_libro INTEGER PRIMARY KEY,"
        "id_estudiante INTEGER,"
        "nombre VARCHAR2(50),"
        "autor VARCHAR2(50),"
        "anio_publicacion NUMBER(4),"
        "CantidadPaginas INTEGER,"
        "Cantidad INTEGER,"
        "Descripcion VARCHAR2(100),"
        "FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante)"
        ")"
    ),
    (
        "CREATE TABLE"
        "PRESTAMOS ("
        "Id_prestamo INTEGER PRIMARY KEY,"
        "id_estudiante INTEGER NOT NULL,"
        "Id_libro INTEGER NOT NULL,"
        "cantidad INTEGER NOT NULL,"
        "fecha_prestamo DATE,"
        "fecha_devolucion DATE,"
        "FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante),"
        "FOREIGN KEY (Id_libro) REFERENCES Libro(id_libro)"
        ")"
    ),
    (
        "CREATE TABLE"
        "DataSetsDescargados ("
        "id_Data_Set_Descargado INTEGER PRIMARY KEY,"
        "id_investigador INTEGER NOT NULL,"
        "Nombre VARCHAR2(50) NOT NULL,"
       " Cantidad INTEGER NOT NULL,"
        "FOREIGN KEY (id_investigador) REFERENCES Investigadores(id_investigador)"
        ")"
    ),
    (
        "CREATE TABLE"
        "BIBLIOTECA ("
        "id_Biblioteca INTEGER PRIMARY KEY,"
        "CantidadMaterial INTEGER NOT NULL,"
        "GestionPrestamo INTEGER NOT NULL"
        ")"
    )
]

for query in tables:
    create_schema(query)



