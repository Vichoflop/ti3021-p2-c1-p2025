from typing import Optional
import oracledb
import os
from dotenv import load_dotenv
from datetime import datetime

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
            connection.commit()
    except oracledb.DatabaseError as error:
        print(f"No se pudo crear la tabla: {error}")

tables = [
    (
        "CREATE TABLE Usuarios ("
        "id_usuario INTEGER PRIMARY KEY,"
        "nombres VARCHAR2(64),"
        "apellidos VARCHAR2(64),"
        "correo varchar2(50)"
    ),
    (
        "CREATE TABLE Estudiantes ("
        "id_estudiante INTEGER PRIMARY KEY,"
        "id_usuario INTEGER,"
        "PrestamosActivos INTEGER NOT NULL,"
        "EstadoDeuda VARCHAR2(50) NOT NULL,"
        "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)"
        ")"
    ),
    (
        "CREATE TABLE Docentes ("
        "id_docente INTEGER PRIMARY KEY,"
        "id_usuario INTEGER,"
        "MaterialExclusivoAccedido VARCHAR2(50) NOT NULL,"
        "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)"
        ")"
    ),
    (
        "CREATE TABLE Investigadores ("
        "id_investigador INTEGER PRIMARY KEY,"
        "NivelAcceso VARCHAR2(50) NOT NULL"
        ")"
    ),
    (
        "CREATE TABLE Libros ("
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
        "CREATE TABLE Prestamos ("
        "Id_prestamo INTEGER PRIMARY KEY,"
        "id_estudiante INTEGER NOT NULL,"
        "Id_libro INTEGER NOT NULL,"
        "cantidad INTEGER NOT NULL,"
        "fecha_prestamo DATE,"
        "fecha_devolucion DATE,"
        "FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante),"
        "FOREIGN KEY (id_libro) REFERENCES Libro(id_libro)"
        ")"
    ),
    (
        "CREATE TABLE DataSetsDescargados ("
        "id_Data_Set_Descargado INTEGER PRIMARY KEY,"
        "id_investigador INTEGER NOT NULL,"
        "Nombre VARCHAR2(50) NOT NULL,"
       " Cantidad INTEGER NOT NULL,"
        "FOREIGN KEY (id_investigador) REFERENCES Investigadores(id_investigador)"
        ")"
    ),
    (
        "CREATE TABLE Biblioteca ("
        "id_biblioteca INTEGER PRIMARY KEY,"
        "CantidadMaterial INTEGER NOT NULL,"
        "GestionPrestamo INTEGER NOT NULL"
        ")"
    )
]

for query in tables:
    create_schema(query)

def create_Usuarios(
        id_usuario: int,
        nombres: str,
        apellidos: str,
        rut: str,
        correo: str
):
    sql = (
        "INSERT INTO Usuarios (id_usuario, nombres, apellidos,correo) "
        "VALUES (:id_usuario, :nombres, :apellidos, :correo)"
    )
    parametros = {
        "id_usuario": id_usuario,
        "nombres": nombres,
        "apellidos": apellidos,
        "correo": correo
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla Usuarios")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")


create_Usuarios(1, "Juan", "Pérez", "juan@example.com")
create_Usuarios(2, "María", "González", "maria@example.com")
create_Usuarios(3, "Pedro", "Lagos", "pedro@example.com")
create_Usuarios(4, "Ana", "Rojas", "ana@example.com")
create_Usuarios(5, "Luis", "Martínez", "luis@example.com")


def create_Estudiantes(
        id_estudiante: int,
        id_usuario: int,
        PrestamosActivos: int,
        EstadoDeuda: str
):
    sql = (
        "INSERT INTO Estudiantes (id_estudiante, id_usuario, PrestamosActivos, EstadoDeuda) "
        "VALUES (:id_estudiante, :id_usuario, :PrestamosActivos, :EstadoDeuda)"
    )
    parametros = {
        "id_estudiante": id_estudiante,
        "id_usuario": id_usuario,
        "PrestamosActivos": PrestamosActivos,
        "EstadoDeuda": EstadoDeuda
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla Estudiantes")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")


create_Estudiantes(1, 1, 2, "Sin deuda")
create_Estudiantes(2, 2, 1, "Sin deuda")
create_Estudiantes(3, 3, 0, "Sin deuda")
create_Estudiantes(4, 4, 3, "Con deuda")
create_Estudiantes(5, 5, 1, "Sin deuda")


def create_Docentes(
        id_docente: int,
        id_usuario: int,
        MaterialExclusivoAccedido: str
):
    sql = (
        "INSERT INTO Docentes (id_docente, id_usuario, MaterialExclusivoAccedido) "
        "VALUES (:id_docente, :id_usuario, :MaterialExclusivoAccedido)"
    )
    parametros = {
        "id_docente": id_docente,
        "id_usuario": id_usuario,
        "MaterialExclusivoAccedido": MaterialExclusivoAccedido
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla Docentes")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")
    

create_Docentes(1, 1, "Guia de Trigonometria")
create_Docentes(2, 2, "Guia de Base de Datos")
create_Docentes(3, 3, "Guia de Programacion")
create_Docentes(4, 4, "Guia de Redes")
create_Docentes(5, 5, "Guia de Sistemas Operativos")


def create_Investigadores(
        id_investigador: int,
        id_usuario: int,
        NivelAcceso: str
):
    sql = (
        "INSERT INTO Investigadores (id_investigador,id_usuario, NivelAcceso) "
        "VALUES (:id_investigador, :id_usuario, :NivelAcceso)"
    )
    parametros = {
        "id_investigador": id_investigador,
        "id_usuario": id_usuario,
        "NivelAcceso": NivelAcceso
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla Investigadores")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")
    

create_Investigadores(1, 1, "Alto")
create_Investigadores(2, 2, "Medio")
create_Investigadores(3, 3, "Alto")
create_Investigadores(4, 4, "Medio")
create_Investigadores(5, 5, "Bajo")


def create_Libros(
        id_libro: int,
        id_estudiante: int,
        nombre: str,
        autor: str,
        anio_publicacion: int,
        CantidadPaginas: int,
        Cantidad: int,
        Descripcion: str
):
    sql = (
        "INSERT INTO Libros (id_libro, id_estudiante, nombre, autor, anio_publicacion, CantidadPaginas, Cantidad, Descripcion) "
        "VALUES (:id_libro, :id_estudiante, :nombre, :autor, :anio_publicacion, :CantidadPaginas, :Cantidad, :Descripcion)"
    )
    parametros = {
        "id_libro": id_libro,
        "id_estudiante": id_estudiante,
        "nombre": nombre,
        "autor": autor,
        "anio_publicacion": anio_publicacion,
        "CantidadPaginas": CantidadPaginas,
        "Cantidad": Cantidad,
        "Descripcion": Descripcion
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla Libros")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")
    

create_Libros(1, 1, "El Principito", "Antoine de Saint-Exupéry", 1943, 96, 5, "Clásico infantil")
create_Libros(2, 2, "1984", "George Orwell", 1949, 328, 3, "Distopía política")
create_Libros(3, 3, "Cien Años de Soledad", "García Márquez", 1967, 417, 4, "Realismo mágico")
create_Libros(4, 4, "Harry Potter 1", "J.K. Rowling", 1997, 223, 7, "Fantasía")
create_Libros(5, 5, "La Odisea", "Homero", -800, 500, 2, "Épica griega")


def create_Prestamos(
        id_prestamo: int,
        id_estudiante: int,
        id_libro: int,
        cantidad: int,
        fecha_prestamo: str,
        fecha_devolucion: str
):
    sql = (
        "INSERT INTO Prestamos (id_prestamo, id_estudiante, id_libro, cantidad, fecha_prestamo, fecha_devolucion) "
        "VALUES (:id_prestamo, :id_estudiante, :id_libro, :cantidad, :fecha_prestamo, :fecha_devolucion)"
    )
    parametros = {
        "id_prestamo": id_prestamo,
        "id_estudiante": id_estudiante,
        "id_libro": id_libro,
        "cantidad": cantidad,
        "fecha_prestamo": fecha_prestamo,
        "fecha_devolucion": fecha_devolucion
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla Prestamos")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")
    

create_Prestamos(1, 1, 1, 1, "2025-01-10", "2025-01-20")
create_Prestamos(2, 2, 2, 1, "2025-01-11", "2025-01-25")
create_Prestamos(3, 3, 3, 2, "2025-01-12", "2025-01-22")
create_Prestamos(4, 4, 4, 1, "2025-01-15", "2025-01-30")
create_Prestamos(5, 5, 5, 1, "2025-01-18", "2025-01-28")


def create_DataSetsDescargados(
        id_Data_Set_Descargado: int,
        id_investigador: int,
        Nombre: str,
        Cantidad: int
):
    sql = (
        "INSERT INTO DataSetsDescargados (id_Data_Set_Descargado, id_investigador, Nombre, Cantidad) "
        "VALUES (:id_Data_Set_Descargado, :id_investigador, :Nombre, :Cantidad)"
    )
    parametros = {
        "id_Data_Set_Descargado": id_Data_Set_Descargado,
        "id_investigador": id_investigador,
        "Nombre": Nombre,
        "Cantidad": Cantidad
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla DataSetsDescargados")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")
    

create_DataSetsDescargados(1, 1, "Genoma Humano", 3)
create_DataSetsDescargados(2, 2, "Clima Global", 5)
create_DataSetsDescargados(3, 3, "Sismos Chile", 2)
create_DataSetsDescargados(4, 4, "Ventas Retail", 4)
create_DataSetsDescargados(5, 5, "Salud Pública", 1)


def create_Biblioteca(
        id_biblioteca: int,
        CantidadMaterial: int,
        GestionPrestamo: int
):
    sql = (
        "INSERT INTO Biblioteca (id_Biblioteca, CantidadMaterial, GestionPrestamo) "
        "VALUES (:id_Biblioteca, :CantidadMaterial, :GestionPrestamo)"
    )
    parametros = {
        "id_Biblioteca": id_biblioteca,
        "CantidadMaterial": CantidadMaterial,
        "GestionPrestamo": GestionPrestamo
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla Biblioteca")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")
    

create_Biblioteca(1, 2000, 300)
create_Biblioteca(2, 1500, 250)
create_Biblioteca(3, 1800, 270)
create_Biblioteca(4, 2200, 320)
create_Biblioteca(5, 2500, 350)



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
        print(f"Error al insertar datos: {err}")




def read_Usuarios_by_id(id_usuario):
    sql = "SELECT * FROM Usuarios WHERE id_usuario = :id"
    parametros = {"id": id_usuario}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql, parametros)
                print("Consulta a la tabla Usuarios")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")



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
        print(f"Error al insertar datos: {err}")



def read_Estudiantes_by_id(id_estudiante):
    sql = "SELECT * FROM Estudiantes WHERE id_estudiante = :id"
    parametros = {"id": id_estudiante}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql, parametros)
                print("Consulta a la tabla Estudiantes")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")





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
        print(f"Error al insertar datos: {err}")



def read_Docentes_by_id(id_docente):
    sql = "SELECT * FROM Docentes WHERE id_docente = :id"
    parametros = {"id": id_docente}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql, parametros)
                print("Consulta a la tabla Docentes")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")


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
        print(f"Error al insertar datos: {err}")



def read_Investigadores_by_id(id_investigador):
    sql = "SELECT * FROM Investigadores WHERE id_investigador = :id"
    parametros = {"id": id_investigador}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql, parametros)
                print("Consulta a la tabla Investigadores")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")



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
        print(f"Error al insertar datos: {err}")



def read_Libros_by_id(id_libro):
    sql = "SELECT * FROM Libros WHERE id_libro = :id"
    parametros = {"id": id_libro}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql, parametros)
                print("Consulta a la tabla Libros")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")


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
        print(f"Error al insertar datos: {err}")



def read_Prestamos_by_id(id_prestamo):
    sql = "SELECT * FROM Prestamos WHERE id_prestamo = :id"
    parametros = {"id": id_prestamo}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql, parametros)
                print("Consulta a la tabla Prestamos")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")



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
        print(f"Error al insertar datos: {err}")



def read_DataSetsDescargados_by_id(id_Data_Set_Descargado):
    sql = (
        "Select * from DataSetsDescargados where id_Data_Set_Descargado = :id"
    )

    parametros = {"id_Data_Set_Descargado": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print("Consulta a la tabla DataSetsDescargados")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")



def read_Biblioteca():
    sql = (
        "Select * from Biblioteca"
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
        print(f"Error al insertar datos: {err}")



def read_Biblioteca_by_id(id_biblioteca):
    sql = (
        "Select * from Biblioteca where id_biblioteca = :id"
    )

    parametros = {"id_biblioteca": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print("Consulta a la tabla Biblioteca")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")


def update_Usuarios(id_usuario, nombres: Optional[str] = None, apellidos: Optional[str] = None, correo: Optional[str] = None ):
    Modificaciones = []     
    parametros = {"id": id_usuario}     
    if nombres is not None:         
        Modificaciones.append("nombres =: nombres")         
        parametros["nombres"] = nombres     
    if apellidos is not None:         
        Modificaciones.append("apellidos =: apellidos")         
        parametros["apellidos"] = apellidos                 
    if correo is not None:         
        Modificaciones.append("correo = :correo")         
        parametros["correo"] = correo           
    if not Modificaciones:         
        print("No hay campos para actualizar.")         
        return      
    
    sql = "UPDATE Usuarios SET " + ", ".join(Modificaciones) + " WHERE id_usuario = :id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Usuario con ID={id_usuario} actualizado.") 


def update_Estudiantes(id_estudiante,PrestamosActivos: Optional[int] = None,EstadoDeuda: Optional[str] = None):
    modificaciones = []     
    parametros = {"id": id_estudiante}
    if PrestamosActivos is not None:         
        modificaciones.append("PrestamosActivos =: PrestamosActivos")         
        parametros["PrestamosActivos"] = PrestamosActivos
    if EstadoDeuda is not None:         
        modificaciones.append("EstadoDeuda =: EstadoDeuda")         
        parametros["EstadoDeuda"] = EstadoDeuda
    if not modificaciones:         
        print("No hay campos para actualizar.")         
        return

    sql = "UPDATE Estudiantes SET " + ", ".join(modificaciones) + " WHERE id_estudiante =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Estudiante con ID={id_estudiante} actualizado.")
   
    

def update_Docentes(id_docente,MaterialExclusivoAccedido: Optional[str] = None):
    modificaciones = []     
    parametros = {"id": id_docente}
    if MaterialExclusivoAccedido is not None:         
        modificaciones.append("MaterialExclusivoAccedido =: MaterialExclusivoAccedido")         
        parametros["MaterialExclusivoAccedido"] = MaterialExclusivoAccedido
    if not modificaciones:         
        print("No hay campos para actualizar.")         
        return

    sql = "UPDATE Docentes SET " + ", ".join(modificaciones) + " WHERE id_docente =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Docente con ID={id_docente} actualizado.")


def update_Investigadores(id_investigador,NivelAcceso: Optional[str] = None):
    modificaciones = []
    parametros = {"id": id_investigador}
    if NivelAcceso is not None:         
        modificaciones.append("NivelAcceso =: NivelAcceso")         
        parametros["NivelAcceso"] = NivelAcceso
    if not modificaciones:         
        print("No hay campos para actualizar.")         
        return

    sql = "UPDATE Investigadores SET " + ", ".join(modificaciones) + " WHERE id_investigador =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Investigador con ID={id_investigador} actualizado.")
    

def update_Libros(
    id_libro,nombre: Optional[str] = None, 
    autor: Optional[str] = None, 
    anio_publicacion: Optional[int] = None, 
    CantidadPaginas: Optional[int] = None, 
    Cantidad: Optional[int] = None, 
    Descripcion: Optional[str] = None
    ):
    modificaciones = []     
    parametros = {"id": id_libro}
    if nombre is not None:         
        modificaciones.append("nombre =: nombre")         
        parametros["nombre"] = nombre
    if autor is not None:         
        modificaciones.append("autor =: autor")         
        parametros["autor"] = autor
    if anio_publicacion is not None:         
        modificaciones.append("anio_publicacion =: anio_publicacion")         
        parametros["anio_publicacion"] = anio_publicacion 
    if CantidadPaginas is not None:         
        modificaciones.append("CantidadPaginas =: CantidadPaginas")         
        parametros["CantidadPaginas"] = CantidadPaginas
    if Cantidad is not None:         
        modificaciones.append("Cantidad =: Cantidad")         
        parametros["Cantidad"] = Cantidad
    if Descripcion is not None:         
        modificaciones.append("Descripcion =: Descripcion")         
        parametros["Descripcion"] = Descripcion
    if not modificaciones:         
        print("No hay campos para actualizar.")         
        return
    
    sql = "UPDATE Libros SET " + ", ".join(modificaciones) + " WHERE id_libro =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Libro con ID={id_libro} actualizado.")



def update_Prestamos(id_prestamo :int,cantidad: Optional[int] = None,fecha_prestamo: Optional[str] = None,fecha_devolucion: Optional[str] = None):
    modificaciones = []     
    parametros = {"id": id_prestamo}
    if cantidad is not None:         
        modificaciones.append("cantidad =: cantidad")         
        parametros["cantidad"] = cantidad
    if fecha_prestamo is not None:         
        modificaciones.append("fecha_prestamo =: fecha_prestamo")         
        parametros["fecha_prestamo"] = datetime.strptime(fecha_prestamo, "%Y-%m-%d") 
    if fecha_devolucion is not None:         
        modificaciones.append("fecha_devolucion =: fecha_devolucion")         
        parametros["fecha_devolucion"] = datetime.strptime(fecha_devolucion, "%Y-%m-%d") 
    if not modificaciones:         
        print("No hay campos para actualizar.")         
        return

    sql = "UPDATE Prestamos SET " + ", ".join(modificaciones) + " WHERE id_prestamo =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Prestamo con ID={id_prestamo} actualizado.")



def update_DataSetsDescargados(id_Data_Set_Descargado: int,Nombre: Optional[str] = None,Cantidad: Optional[int] = None):
    modificaciones = []     
    parametros = {"id": id_Data_Set_Descargado}
    if Nombre is not None:         
        modificaciones.append("Nombre =: Nombre")         
        parametros["Nombre"] = Nombre
    if Cantidad is not None:         
        modificaciones.append("Cantidad =: Cantidad")         
        parametros["Cantidad"] = Cantidad
    if not modificaciones:         
        print("No hay campos para actualizar.")         
        return

    sql = "UPDATE DataSetsDescargados SET " + ", ".join(modificaciones) + " WHERE id_Data_Set_Descargado =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"DataSetDescargado con ID={id_Data_Set_Descargado} actualizado.")
    

def update_Biblioteca(id_biblioteca: int,CantidadMaterial: Optional[int] = None,GestionPrestamo: Optional[int] = None):
    modificaciones = []     
    parametros = {"id": id_biblioteca}
    if CantidadMaterial is not None:         
        modificaciones.append("CantidadMaterial =: CantidadMaterial")         
        parametros["CantidadMaterial"] = CantidadMaterial
    if GestionPrestamo is not None:         
        modificaciones.append("GestionPrestamo =: GestionPrestamo")         
        parametros["GestionPrestamo"] = GestionPrestamo
    if not modificaciones:         
        print("No hay campos para actualizar.")         
        return

    sql = "UPDATE Biblioteca SET " + ", ".join(modificaciones) + " WHERE id_biblioteca =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Biblioteca con ID={id_biblioteca} actualizado.")


def delete_Usuario(id_usuario:int):
    sql ={
        "DELETE FROM Usuarios WHERE id_usuario = :id"
    }

    parametros = {"id": id_usuario}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar datos: {err} \n {sql} \n {parametros}")



def delete_Estudiante(id_estudiante:int):
    sql ={
        "DELETE FROM Usuarios WHERE id_estudiante = :id"
    }

    parametros = {"id": id_estudiante}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar datos: {err} \n {sql} \n {parametros}")



def delete_Docente(id_docente:int):
    sql ={
        "DELETE FROM Usuarios WHERE id_docente = :id"
    }

    parametros = {"id": id_docente}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar datos: {err} \n {sql} \n {parametros}")



def delete_investigador(id_investigador:int):
    sql ={
        "DELETE FROM Usuarios WHERE id_investigador = :id"
    }

    parametros = {"id": id_investigador}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar datos: {err} \n {sql} \n {parametros}")



def delete_Libro(id_libro:int):
    sql ={
        "DELETE FROM Usuarios WHERE id_libro = :id"
    }

    parametros = {"id": id_libro}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar datos: {err} \n {sql} \n {parametros}")




def delete_prestamo(id_prestamo:int):
    sql ={
        "DELETE FROM Usuarios WHERE id_prestamo = :id"
    }

    parametros = {"id": id_prestamo}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar datos: {err} \n {sql} \n {parametros}")




def delete_Data_Set_Descargado(id_Data_Set_Descargado:int):
    sql ={
        "DELETE FROM Usuarios WHERE id_Data_Set_Descargado = :id"
    }

    parametros = {"id": id_Data_Set_Descargado}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar datos: {err} \n {sql} \n {parametros}")




def delete_Biblioteca(id_biblioteca:int):
    sql ={
        "DELETE FROM Usuarios WHERE id_biblioteca = :id"
    }

    parametros = {"id": id_biblioteca}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar datos: {err} \n {sql} \n {parametros}")

def menu_Usuarios():
    while True:
        """
            ==========================================
            |          Menu Usuarios          |
            ==========================================
            |----------------------------------------|
            ==========================================
            |1.Insertar Usuarios                     | 
            |----------------------------------------|
            |2. TABLA USUARIOS                       |
            |----------------------------------------|
            |3. TABLA ESTUDIANTES                    |
            |----------------------------------------|
            |4. TABLA DOCENTES                       |
            |----------------------------------------|
            |5. TABLA INVESTIGADORES                 |
            |----------------------------------------|
            |6. TABLA LIBROS                         |
            |----------------------------------------|
            |7. TABLA PRESTAMOS                      |
            |----------------------------------------|
            |8. TABLA DataSetsDescargados            |
            |----------------------------------------|
            |9. TABLA BIBLIOTECA                     |
            |----------------------------------------|
            |0. SALIR                                |  
            |----------------------------------------|                                                        
            ==========================================
            """
        

import os 
def main():
    while True:
        os.system("cis")
        print(
            """
            ==========================================
            |          CRUD CON ORACLESLQ            |
            ==========================================
            |----------------------------------------|
            ==========================================
            |1.APLICAR ESQUEMA EN LA BASE DE DATOS   | 
            |----------------------------------------|
            |2. TABLA USUARIOS                       |
            |----------------------------------------|
            |3. TABLA ESTUDIANTES                    |
            |----------------------------------------|
            |4. TABLA DOCENTES                       |
            |----------------------------------------|
            |5. TABLA INVESTIGADORES                 |
            |----------------------------------------|
            |6. TABLA LIBROS                         |
            |----------------------------------------|
            |7. TABLA PRESTAMOS                      |
            |----------------------------------------|
            |8. TABLA DataSetsDescargados            |
            |----------------------------------------|
            |9. TABLA BIBLIOTECA                     |
            |----------------------------------------|
            |0. SALIR                                |  
            |----------------------------------------|                                                        
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-9, 0 para salir] : ")

        if opcion == "0":
            print("Adios :)")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            pass
        elif opcion == "2":
            pass
        elif opcion == "3":
            pass
        elif opcion == "4":
            pass
        elif opcion == "5":
            pass
        elif opcion == "6":
            pass
        elif opcion == "7":
            pass
        elif opcion == "8":
            pass
        elif opcion == "9":
            pass
        else:
            print("Opcion invalida")
            print("Presiona ENTER para continuar...")
            break


if __name__ == "__main__":
    main()