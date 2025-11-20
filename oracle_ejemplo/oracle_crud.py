from typing import Optional
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
        "LIBROS ("
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

def create_Usuarios():
    pass

def create_Estudiantes():
    pass

def create_Docentes():
    pass

def create_Investigadores():
    pass

def create_Libros():
    pass

def create_Prestamos():
    pass

def create_DataSetsDescargados():
    pass

def create_Biblioteca():
    pass


def read_Usuarios():
    sql = (
        "Select * from Usuarios"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print("Consulta a la tabla Usuarios")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")




def read_Usuarios_by_id(id):
    sql = (
        "Select * from Usuarios where id = :id"
    )

    parametros = {"id": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print("Consulta a la tabla Usuarios")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_Estudiantes():
    sql = (
        "Select * from Estudiantes"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print("Consulta a la tabla Estudiantes")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_Estudiantes_by_id(id):
    sql = (
        "Select * from Estudiantes where id = :id"
    )

    parametros = {"id": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print("Consulta a la tabla Estudiantes")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")




def read_Docentes():
    sql = (
        "Select * from Docentes"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print("Consulta a la tabla Docentes")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_Docentes_by_id(id):
    sql = (
        "Select * from Docentes where id = :id"
    )

    parametros = {"id": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print("Consulta a la tabla Docentes")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_Investigadores():
    sql = (
        "Select * from Investigadores"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print("Consulta a la tabla Investigadores")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_Investigadores_by_id(id):
    sql = (
        "Select * from Investigadores where id = :id"
    )

    parametros = {"id": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print("Consulta a la tabla Investigadores")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_Libros():
    sql = (
        "Select * from Libros"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print("Consulta a la tabla Libros")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_Libros_by_id(id):
    sql = (
        "Select * from Libros where id = :id"
    )

    parametros = {"id": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print("Consulta a la tabla Libros")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_Prestamos():
    sql = (
        "Select * from Prestamos"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print("Consulta a la tabla Prestamos")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_Prestamos_by_id(id):
    sql = (
        "Select * from Prestamos where id = :id"
    )

    parametros = {"id": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print("Consulta a la tabla Prestamos")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_DataSetsDescargados():
    sql = (
        "Select * from DataSetsDescargados"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print("Consulta a la tabla DataSetsDescargados")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_DataSetsDescargados_by_id(id):
    sql = (
        "Select * from DataSetsDescargados where id = :id"
    )

    parametros = {"id": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print("Consulta a la tabla DataSetsDescargados")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_Biblioteca():
    sql = (
        "Select * from Bilioteca"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print("Consulta a la tabla Biblioteca")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")



def read_Biblioteca_by_id(id):
    sql = (
        "Select * from Biblioteca where id = :id"
    )

    parametros = {"id": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print("Consulta a la tabla Biblioteca")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {e}")


def update_Usuarios(id_usuario, nombres: Optional[str] = None, apellidos: Optional[str] = None, rut: Optional[str] = None, correo: Optional[str] = None ):
    Modificaciones = []     
    parametros = {"id": id_usuario}     
    if nombres is not None:         
        Modificaciones.append("nombres =: nombres")         
        parametros["nombres"] = nombres     
    if apellidos is not None:         
        Modificaciones.append("apellidos =: apellidos")         
        parametros["apellidos"] = apellidos     
    if rut is not None:         
        Modificaciones.append("rut =: rut")         
        parametros["rut"] = rut     
    if correo is not None:         
        Modificaciones.append("correo = :correo")         
        parametros["correo"] = correo           
    if not Modificaciones:         
        print("No hay campos para actualizar.")         
        return      
    
    sql = "UPDATE personas SET " + ", ".join(Modificaciones) + " WHERE id =: id" 


def update_Estudiantes():
    pass

def update_Docentes():
    pass

def update_Investigadores():
    pass

def update_Libros():
    pass

def update_Prestamos():
    pass

def update_DataSetsDescargados():
    pass

def update_Biblioteca():
    pass


