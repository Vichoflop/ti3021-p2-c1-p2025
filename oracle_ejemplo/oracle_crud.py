from typing import Optional
import oracledb
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

username= os.getenv("user")
dsn = os.getenv("host")
password = os.getenv("password")

def get_connection():
    return oracledb.connect(user = username, password = password, dsn = dsn)

def create_schema(query):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                print(f"{query}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la tabla: {err} \n {query}")

def create_all_tables():

    tables = [
        (
            "CREATE TABLE Usuarios ("
            "id_usuario INTEGER PRIMARY KEY,"
            "nombre VARCHAR2(64),"
            "apellido VARCHAR2(64),"
            "correo VARCHAR2(50)"
            ")"
        ),
        (
            "CREATE TABLE Estudiantes ("
            "id_estudiante INTEGER PRIMARY KEY,"
            "id_usuario INTEGER,"
            "PrestamosActivos INTEGER NOT NULL,"
            "Estado VARCHAR2(100) NOT NULL,"
            "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)"
            ")"
        ),
        (
            "CREATE TABLE Docentes ("
            "id_docente INTEGER PRIMARY KEY,"
            "id_usuario INTEGER,"
            "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),"
            ")"
        ),
        (
            "CREATE TABLE Investigadores ("
            "id_investigador INTEGER PRIMARY KEY,"
            "id_usuario INTEGER,"
            "NivelAcceso VARCHAR2(100) NOT NULL,"
            "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),"
            ")"
        ),
        (
            "CREATE TABLE Libros ("
            "id_libro INTEGER PRIMARY KEY,"
            "id_estudiante INTEGER,"
            "nombre VARCHAR2(100),"
            "autor VARCHAR2(100),"
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
            "FOREIGN KEY (Id_libro) REFERENCES Libros(id_libro)"
            ")"
        ),
        (
            "CREATE TABLE DataSetsDescargados ("
            "id_Data_Set_Descargado INTEGER PRIMARY KEY,"
            "id_investigador INTEGER NOT NULL,"
            "Nombre VARCHAR2(100) NOT NULL,"
            "Cantidad INTEGER NOT NULL,"
            "FOREIGN KEY (id_investigador) REFERENCES Investigadores(id_investigador)"
            ")"
        ),
        (
            "CREATE TABLE MaterialExclusivo ("
            "id_material_exclusivo INTEGER PRIMARY KEY,"
            "id_docente INTEGER NOT NULL,"
            "nombre VARCHAR2(150) NOT NULL,"
            "Descripcion VARCHAR2(300) NOT NULL,"
            "FOREIGN KEY (id_docente) REFERENCES Docentes(id_docente)"
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


def drop_all_tables():
    # Orden inverso a las dependencias
    drop_order = [
        "Prestamos",
        "Libros",
        "DataSetsDescargados",
        "MaterialExclusivo",
        "Investigadores",
        "Docentes",
        "Estudiantes",
        "Biblioteca",
        "Usuarios"
    ]
    drops = [f"DROP TABLE {table} CASCADE CONSTRAINTS" for table in drop_order]
    for query in drops:
        create_schema(query)

def create_Usuarios(
        id_usuario: int,
        nombre: str,
        apellido: str,
        correo: str
):
    sql = (
        "INSERT INTO Usuarios (id_usuario, nombre, apellido, correo) "
        "VALUES (:id_usuario, :nombre, :apellido, :correo)"
    )
    parametros = {
        "id_usuario": id_usuario,
        "nombre": nombre,
        "apellido": apellido,
        "correo": correo
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla Usuarios")
    except oracledb.DatabaseError as e:
        print(f"Error al insertar datos: {e}")


def create_Estudiantes(
        id_estudiante: int,
        id_usuario: int,
        PrestamosActivos: int,
        Estado: str
):
    sql = (
        "INSERT INTO Estudiantes (id_estudiante, id_usuario, PrestamosActivos, Estado) "
        "VALUES (:id_estudiante, :id_usuario, :PrestamosActivos, :Estado)"
    )
    parametros = {
        "id_estudiante": id_estudiante,
        "id_usuario": id_usuario,
        "PrestamosActivos": PrestamosActivos,
        "Estado": Estado
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla Estudiantes")
    except oracledb.DatabaseError as e:
        print(f"Error al insertar datos: {e}")


def create_Docentes(
        id_docente: int,
        id_usuario: int
):
    sql = (
        "INSERT INTO Docentes (id_docente, id_usuario) "
        "VALUES (:id_docente, :id_usuario)"
    )
    parametros = {
        "id_docente": id_docente,
        "id_usuario": id_usuario
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla Docentes")
    except oracledb.DatabaseError as e:
        print(f"Error al insertar datos: {e}")


def create_Investigadores(
        id_investigador: int,
        id_usuario: int,
        NivelAcceso: str
):
    sql = (
        "INSERT INTO Investigadores (id_investigador, id_usuario, NivelAcceso) "
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
        print(f"Error al insertar datos: {e}")


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
        print(f"Error al insertar datos: {e}")


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
        print(f"Error al insertar datos: {e}")


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
        print(f"Error al insertar datos: {e}")


def create_MaterialExclusivo(
        id_material_exclusivo: int,
        id_docente: int,
        nombre: str,
        Descripcion: str
):
    sql = (
        "INSERT INTO MaterialExclusivo (id_material_exclusivo, id_docente, nombre, Descripcion) "
        "VALUES (:id_material_exclusivo, :id_docente, :nombre, :Descripcion)"
    )
    parametros = {
        "id_material_exclusivo": id_material_exclusivo,
        "id_docente": id_docente,
        "nombre": nombre,
        "Descripcion": Descripcion
    }
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print("Datos insertados en la tabla MaterialExclusivo")
    except oracledb.DatabaseError as e:
        print(f"Error al insertar datos: {e}")


def create_Biblioteca(
        id_biblioteca: int,
        CantidadMaterial: int,
        GestionPrestamo: int
):
    sql = (
        "INSERT INTO Biblioteca (id_biblioteca, CantidadMaterial, GestionPrestamo) "
        "VALUES (:id_biblioteca, :CantidadMaterial, :GestionPrestamo)"
    )
    parametros = {
        "id_biblioteca": id_biblioteca,
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
        print(f"Error al insertar datos: {e}")


def read_Usuarios():
    sql = "SELECT * FROM Usuarios"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()
                print("Consulta a la tabla Usuarios")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Usuarios_by_id(id_usuario):
    sql = "SELECT * FROM Usuarios WHERE id_usuario = :id_usuario"
    parametros = {"id_usuario": id_usuario}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                resultados = cur.fetchall()
                print("Consulta a la tabla Usuarios por ID")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Estudiantes():
    sql = "SELECT * FROM Estudiantes"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()
                print("Consulta a la tabla Estudiantes")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Estudiantes_by_id(id_estudiante):
    sql = "SELECT * FROM Estudiantes WHERE id_estudiante = :id_estudiante"
    parametros = {"id_estudiante": id_estudiante}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                resultados = cur.fetchall()
                print("Consulta a la tabla Estudiantes por ID")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Docentes():
    sql = "SELECT * FROM Docentes"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()
                print("Consulta a la tabla Docentes")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Docentes_by_id(id_docente):
    sql = "SELECT * FROM Docentes WHERE id_docente = :id_docente"
    parametros = {"id_docente": id_docente}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                resultados = cur.fetchall()
                print("Consulta a la tabla Docentes por ID")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Investigadores():
    sql = "SELECT * FROM Investigadores"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()
                print("Consulta a la tabla Investigadores")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Investigadores_by_id(id_investigador):
    sql = "SELECT * FROM Investigadores WHERE id_investigador = :id_investigador"
    parametros = {"id_investigador": id_investigador}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                resultados = cur.fetchall()
                print("Consulta a la tabla Investigadores por ID")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Libros():
    sql = "SELECT * FROM Libros"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()
                print("Consulta a la tabla Libros")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Libros_by_id(id_libro):
    sql = "SELECT * FROM Libros WHERE id_libro = :id_libro"
    parametros = {"id_libro": id_libro}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                resultados = cur.fetchall()
                print("Consulta a la tabla Libros por ID")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Prestamos():
    sql = "SELECT * FROM Prestamos"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()
                print("Consulta a la tabla Prestamos")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Prestamos_by_id(id_prestamo):
    sql = "SELECT * FROM Prestamos WHERE id_prestamo = :id_prestamo"
    parametros = {"id_prestamo": id_prestamo}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                resultados = cur.fetchall()
                print("Consulta a la tabla Prestamos por ID")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_DataSetsDescargados():
    sql = "SELECT * FROM DataSetsDescargados"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()
                print("Consulta a la tabla DataSetsDescargados")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_DataSetsDescargados_by_id(id_Data_Set_Descargado):
    sql = "SELECT * FROM DataSetsDescargados WHERE id_Data_Set_Descargado = :id_Data_Set_Descargado"
    parametros = {"id_Data_Set_Descargado": id_Data_Set_Descargado}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                resultados = cur.fetchall()
                print("Consulta a la tabla DataSetsDescargados por ID")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_MaterialExclusivo():
    sql = "SELECT * FROM MaterialExclusivo"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()
                print("Consulta a la tabla MaterialExclusivo")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_MaterialExclusivo_by_id(id_material_exclusivo):
    sql = "SELECT * FROM MaterialExclusivo WHERE id_material_exclusivo = :id_material_exclusivo"
    parametros = {"id_material_exclusivo": id_material_exclusivo}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                resultados = cur.fetchall()
                print("Consulta a la tabla MaterialExclusivo por ID")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Biblioteca():
    sql = "SELECT * FROM Biblioteca"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()
                print("Consulta a la tabla Biblioteca")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


def read_Biblioteca_by_id(id_biblioteca):
    sql = "SELECT * FROM Biblioteca WHERE id_biblioteca = :id_biblioteca"
    parametros = {"id_biblioteca": id_biblioteca}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                resultados = cur.fetchall()
                print("Consulta a la tabla Biblioteca por ID")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        print(f"Error al consultar datos: {e}")


from typing import Optional
from datetime import datetime

def update_Usuarios(id_usuario: int, nombre: Optional[str] = None, apellido: Optional[str] = None, correo: Optional[str] = None):
    modificaciones = []
    parametros = {"id_usuario": id_usuario}
    if nombre is not None:
        modificaciones.append("nombre = :nombre")
        parametros["nombre"] = nombre
    if apellido is not None:
        modificaciones.append("apellido = :apellido")
        parametros["apellido"] = apellido
    if correo is not None:
        modificaciones.append("correo = :correo")
        parametros["correo"] = correo
    if not modificaciones:
        print("No hay campos para actualizar.")
        return

    sql = "UPDATE Usuarios SET " + ", ".join(modificaciones) + " WHERE id_usuario = :id_usuario"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Usuario con ID={id_usuario} actualizado.")
    except oracledb.DatabaseError as e:
        print(f"Error al actualizar datos: {e}")


def update_Estudiantes(id_estudiante: int, PrestamosActivos: Optional[int] = None, Estado: Optional[str] = None):
    modificaciones = []
    parametros = {"id_estudiante": id_estudiante}
    if PrestamosActivos is not None:
        modificaciones.append("PrestamosActivos = :PrestamosActivos")
        parametros["PrestamosActivos"] = PrestamosActivos
    if Estado is not None:
        modificaciones.append("Estado = :Estado")
        parametros["Estado"] = Estado
    if not modificaciones:
        print("No hay campos para actualizar.")
        return

    sql = "UPDATE Estudiantes SET " + ", ".join(modificaciones) + " WHERE id_estudiante = :id_estudiante"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Estudiante con ID={id_estudiante} actualizado.")
    except oracledb.DatabaseError as e:
        print(f"Error al actualizar datos: {e}")



def update_Docentes(id_docente: int, id_usuario: Optional[int] = None):
    modificaciones = []
    parametros = {"id_docente": id_docente}

    if id_usuario is not None:
        modificaciones.append("id_usuario = :id_usuario")
        parametros["id_usuario"] = id_usuario

    if not modificaciones:
        print("No hay campos para actualizar.")
        return

    sql = "UPDATE Docentes SET " + ", ".join(modificaciones) + " WHERE id_docente = :id_docente"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Docente con ID={id_docente} actualizado.")
    except oracledb.DatabaseError as e:
        print(f"Error al actualizar datos: {e}")


def update_Investigadores(id_investigador: int, NivelAcceso: Optional[str] = None):
    modificaciones = []
    parametros = {"id_investigador": id_investigador}
    if NivelAcceso is not None:
        modificaciones.append("NivelAcceso = :NivelAcceso")
        parametros["NivelAcceso"] = NivelAcceso
    if not modificaciones:
        print("No hay campos para actualizar.")
        return

    sql = "UPDATE Investigadores SET " + ", ".join(modificaciones) + " WHERE id_investigador = :id_investigador"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Investigador con ID={id_investigador} actualizado.")
    except oracledb.DatabaseError as e:
        print(f"Error al actualizar datos: {e}")


def update_Libros(id_libro: int, nombre: Optional[str] = None, autor: Optional[str] = None,
                  anio_publicacion: Optional[int] = None, CantidadPaginas: Optional[int] = None,
                  Cantidad: Optional[int] = None, Descripcion: Optional[str] = None):
    modificaciones = []
    parametros = {"id_libro": id_libro}
    if nombre is not None:
        modificaciones.append("nombre = :nombre")
        parametros["nombre"] = nombre
    if autor is not None:
        modificaciones.append("autor = :autor")
        parametros["autor"] = autor
    if anio_publicacion is not None:
        modificaciones.append("anio_publicacion = :anio_publicacion")
        parametros["anio_publicacion"] = anio_publicacion
    if CantidadPaginas is not None:
        modificaciones.append("CantidadPaginas = :CantidadPaginas")
        parametros["CantidadPaginas"] = CantidadPaginas
    if Cantidad is not None:
        modificaciones.append("Cantidad = :Cantidad")
        parametros["Cantidad"] = Cantidad
    if Descripcion is not None:
        modificaciones.append("Descripcion = :Descripcion")
        parametros["Descripcion"] = Descripcion
    if not modificaciones:
        print("No hay campos para actualizar.")
        return

    sql = "UPDATE Libros SET " + ", ".join(modificaciones) + " WHERE id_libro = :id_libro"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Libro con ID={id_libro} actualizado.")
    except oracledb.DatabaseError as e:
        print(f"Error al actualizar datos: {e}")


def update_Prestamos(id_prestamo: int, cantidad: Optional[int] = None,
                     fecha_prestamo: Optional[str] = None, fecha_devolucion: Optional[str] = None):
    modificaciones = []
    parametros = {"id_prestamo": id_prestamo}
    if cantidad is not None:
        modificaciones.append("cantidad = :cantidad")
        parametros["cantidad"] = cantidad
    if fecha_prestamo is not None:
        modificaciones.append("fecha_prestamo = :fecha_prestamo")
        parametros["fecha_prestamo"] = datetime.strptime(fecha_prestamo, "%Y-%m-%d")
    if fecha_devolucion is not None:
        modificaciones.append("fecha_devolucion = :fecha_devolucion")
        parametros["fecha_devolucion"] = datetime.strptime(fecha_devolucion, "%Y-%m-%d")
    if not modificaciones:
        print("No hay campos para actualizar.")
        return

    sql = "UPDATE Prestamos SET " + ", ".join(modificaciones) + " WHERE id_prestamo = :id_prestamo"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Préstamo con ID={id_prestamo} actualizado.")
    except oracledb.DatabaseError as e:
        print(f"Error al actualizar datos: {e}")


def update_DataSetsDescargados(id_Data_Set_Descargado: int, Nombre: Optional[str] = None, Cantidad: Optional[int] = None):
    modificaciones = []
    parametros = {"id_Data_Set_Descargado": id_Data_Set_Descargado}
    if Nombre is not None:
        modificaciones.append("Nombre = :Nombre")
        parametros["Nombre"] = Nombre
    if Cantidad is not None:
        modificaciones.append("Cantidad = :Cantidad")
        parametros["Cantidad"] = Cantidad
    if not modificaciones:
        print("No hay campos para actualizar.")
        return

    sql = "UPDATE DataSetsDescargados SET " + ", ".join(modificaciones) + " WHERE id_Data_Set_Descargado = :id_Data_Set_Descargado"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"DataSetDescargado con ID={id_Data_Set_Descargado} actualizado.")
    except oracledb.DatabaseError as e:
        print(f"Error al actualizar datos: {e}")


def update_MaterialExclusivo(id_material_exclusivo: int, nombre: Optional[str] = None, Descripcion: Optional[str] = None):
    modificaciones = []
    parametros = {"id_material_exclusivo": id_material_exclusivo}
    if nombre is not None:
        modificaciones.append("nombre = :nombre")
        parametros["nombre"] = nombre
    if Descripcion is not None:
        modificaciones.append("Descripcion = :Descripcion")
        parametros["Descripcion"] = Descripcion
    if not modificaciones:
        print("No hay campos para actualizar.")
        return

    sql = "UPDATE MaterialExclusivo SET " + ", ".join(modificaciones) + " WHERE id_material_exclusivo = :id_material_exclusivo"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"MaterialExclusivo con ID={id_material_exclusivo} actualizado.")
    except oracledb.DatabaseError as e:
        print(f"Error al actualizar datos: {e}")
              
def update_Biblioteca(id_biblioteca: int, CantidadMaterial: Optional[int] = None, GestionPrestamo: Optional[int] = None):
    modificaciones = []
    parametros = {"id_biblioteca": id_biblioteca}
    if CantidadMaterial is not None:
        modificaciones.append("CantidadMaterial = :CantidadMaterial")
        parametros["CantidadMaterial"] = CantidadMaterial
    if GestionPrestamo is not None:
        modificaciones.append("GestionPrestamo = :GestionPrestamo")
        parametros["GestionPrestamo"] = GestionPrestamo
    if not modificaciones:
        print("No hay campos para actualizar.")
        return

    sql = "UPDATE Biblioteca SET " + ", ".join(modificaciones) + " WHERE id_biblioteca = :id_biblioteca"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Biblioteca con ID={id_biblioteca} actualizada.")
    except oracledb.DatabaseError as e:
        print(f"Error al actualizar datos: {e}")



def delete_Usuario(id_usuario: int):
    sql = "DELETE FROM Usuarios WHERE id_usuario = :id_usuario"
    parametros = {"id_usuario": id_usuario}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Usuario eliminado: {parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar Usuario: {e}")


def delete_Estudiante(id_estudiante: int):
    sql = "DELETE FROM Estudiantes WHERE id_estudiante = :id_estudiante"
    parametros = {"id_estudiante": id_estudiante}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Estudiante eliminado: {parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar Estudiante: {e}")


def delete_Docente(id_docente: int):
    sql = "DELETE FROM Docentes WHERE id_docente = :id_docente"
    parametros = {"id_docente": id_docente}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Docente eliminado: {parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar Docente: {e}")


def delete_Investigador(id_investigador: int):
    sql = "DELETE FROM Investigadores WHERE id_investigador = :id_investigador"
    parametros = {"id_investigador": id_investigador}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Investigador eliminado: {parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar Investigador: {e}")


def delete_Libro(id_libro: int):
    sql = "DELETE FROM Libros WHERE id_libro = :id_libro"
    parametros = {"id_libro": id_libro}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Libro eliminado: {parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar Libro: {e}")


def delete_Prestamo(id_prestamo: int):
    sql = "DELETE FROM Prestamos WHERE id_prestamo = :id_prestamo"
    parametros = {"id_prestamo": id_prestamo}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Préstamo eliminado: {parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar Préstamo: {e}")


def delete_Data_Set_Descargado(id_Data_Set_Descargado: int):
    sql = "DELETE FROM DataSetsDescargados WHERE id_Data_Set_Descargado = :id_Data_Set_Descargado"
    parametros = {"id_Data_Set_Descargado": id_Data_Set_Descargado}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"DataSetDescargado eliminado: {parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar DataSetDescargado: {e}")


def delete_Material_Exclusivo(id_material_exclusivo: int):
    sql = "DELETE FROM MaterialExclusivo WHERE id_material_exclusivo = :id_material_exclusivo"
    parametros = {"id_material_exclusivo": id_material_exclusivo}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"MaterialExclusivo eliminado: {parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar MaterialExclusivo: {e}")


def delete_Biblioteca(id_biblioteca: int):
    sql = "DELETE FROM Biblioteca WHERE id_biblioteca = :id_biblioteca"
    parametros = {"id_biblioteca": id_biblioteca}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Biblioteca eliminada: {parametros}")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar Biblioteca: {e}")

import os

def menu_Usuarios():
    while True:
        os.system("cls")  # En Linux/Mac usar "clear"
        print("""
            ==========================================
            |          Menu Usuarios                 |
            ==========================================
            | 1. Insertar Usuario                    |
            |----------------------------------------|
            | 2. Leer Usuario por Id                 |
            |----------------------------------------|
            | 3. Modificar Usuario                   |
            |----------------------------------------|
            | 4. Eliminar Usuario                    |
            |----------------------------------------|
            | 0. Volver al Menu Principal            |
            ==========================================
        """)
        opcion = input("Selecciona una opción [1-4, 0 para volver]: ").strip()

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break

        elif opcion == "1":
            try:
                id_usuario = int(input("Ingrese el id numérico del Usuario: "))
                nombre = input("Ingrese el nombre del Usuario: ").strip()
                apellido = input("Ingrese el apellido del Usuario: ").strip()
                if nombre and apellido:
                    correo = f"{nombre.lower()}.{apellido.lower()}@correo.cl"
                    print(f"📧 Nuevo correo generado: {correo}")
                else:
                    correo = None
                create_Usuarios(id_usuario, nombre, apellido, correo)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "2":
            try:
                id_usuario = int(input("Ingrese el id numérico del Usuario: "))
                read_Usuarios_by_id(id_usuario)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "3":
            try:
                id_usuario = int(input("Ingrese el id numérico del Usuario: "))
                read_Usuarios_by_id(id_usuario)
                print("⚠️ Si no deseas cambiar un campo, déjalo vacío.")
                nombre = input("Nuevo nombre: ").strip()
                apellido = input("Nuevo apellido: ").strip()
                if nombre and apellido:
                    correo = f"{nombre.lower()}.{apellido.lower()}@correo.cl"
                    print(f"📧 Nuevo correo generado: {correo}")
                else:
                    correo = None
                update_Usuarios(
                    id_usuario,
                    nombre if nombre else None,
                    apellido if apellido else None,
                    correo
                )
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "4":
            try:
                id_usuario = int(input("Ingrese el id numérico del Usuario: "))
                delete_Usuario(id_usuario)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")
            input("Presiona ENTER para continuar...")
            break


import os

def menu_Estudiantes():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu Estudiantes              |
            ==========================================
            | 1. Insertar Estudiante                 |
            |----------------------------------------|
            | 2. Leer Estudiante por Id              |
            |----------------------------------------|
            | 3. Modificar Estudiante                |
            |----------------------------------------|
            | 4. Eliminar Estudiante                 |
            |----------------------------------------|
            | 0. Volver al Menu Principal            |
            ==========================================
        """)
        opcion = input("Selecciona una opción [1-4, 0 para volver]: ").strip()

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break

        elif opcion == "1":
            try:
                id_estudiante = int(input("Ingrese el id numérico del Estudiante: "))
                id_usuario = int(input("Ingrese el id numérico del Usuario: "))
                prestamos_activos = int(input("Ingrese la cantidad de préstamos activos: "))
                opciones_validas = ["pendiente", "devuelto", "retrasado"]
                Estado = input("Ingrese el Estado de deuda (pendiente-devuelto-retrasado): ").strip().lower()
                while Estado not in opciones_validas:
                    print("❌ Opción no válida. Debe ingresar: pendiente, devuelto o retrasado.")
                    Estado = input("Ingrese nuevamente el Estado de deuda: ").strip().lower()
                print("✔️ Estado de deuda registrado correctamente:", Estado)
                create_Estudiantes(id_estudiante, id_usuario, prestamos_activos, Estado)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "2":
            try:
                id_estudiante = int(input("Ingrese el id numérico del Estudiante: "))
                read_Estudiantes_by_id(id_estudiante)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "3":
            try:
                id_estudiante = int(input("Ingrese el id numérico del Estudiante: "))
                read_Estudiantes_by_id(id_estudiante)
                print("⚠️ Si no deseas cambiar un campo, déjalo vacío.")
                prestamos_activos = input("Nueva cantidad de préstamos activos: ").strip()
                Estado = input("Nuevo Estado de deuda (pendiente-devuelto-retrasado): ").strip().lower()
                update_Estudiantes(
                    id_estudiante,
                    int(prestamos_activos) if prestamos_activos else None,
                    Estado if Estado else None
                )
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "4":
            try:
                id_estudiante = int(input("Ingrese el id numérico del Estudiante: "))
                delete_Estudiante(id_estudiante)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")
            input("Presiona ENTER para continuar...")


def menu_Docentes():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu Docentes                 |
            ==========================================
            | 1. Insertar Docente                    |
            |----------------------------------------|
            | 2. Leer Docente por Id                 |
            |----------------------------------------|
            | 3. Modificar Docente                   |
            |----------------------------------------|
            | 4. Eliminar Docente                    |
            |----------------------------------------|
            | 0. Volver al Menu Principal            |
            ==========================================
        """)
        opcion = input("Selecciona una opción [1-4, 0 para volver]: ").strip()

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break

        elif opcion == "1":
            try:
                id_docente = int(input("Ingrese el id numérico del Docente: "))
                id_usuario = int(input("Ingrese el id numérico del Usuario: "))
                create_Docentes(id_docente, id_usuario)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "2":
            try:
                id_docente = int(input("Ingrese el id numérico del Docente: "))
                read_Docentes_by_id(id_docente)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "3":
            try:
                id_docente = int(input("Ingrese el id numérico del Docente: "))
                print("⚠️ Si no deseas cambiar un campo, déjalo vacío.")
                id_usuario = input("Nuevo id de Usuario: ").strip()
                if id_usuario:
                    id_usuario = int(id_usuario)
                else:
                    id_usuario = None
                update_Docentes(id_docente, id_usuario)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "4":
            try:
                id_docente = int(input("Ingrese el id numérico del Docente: "))
                delete_Docente(id_docente)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")
            input("Presiona ENTER para continuar...")



import os

def menu_Investigadores():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu Investigadores           |
            ==========================================
            | 1. Insertar Investigador               |
            |----------------------------------------|
            | 2. Leer Investigador por Id            |
            |----------------------------------------|
            | 3. Modificar Investigador              |
            |----------------------------------------|
            | 4. Eliminar Investigador               |
            |----------------------------------------|
            | 0. Volver al Menu Principal            |
            ==========================================
        """)
        opcion = input("Selecciona una opción [1-4, 0 para volver]: ").strip()

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break

        elif opcion == "1":
            try:
                id_investigador = int(input("Ingrese el id numérico del Investigador: "))
                id_usuario = int(input("Ingrese el id numérico del Usuario: "))
                NivelAcceso = input("Ingrese el nivel de acceso del Investigador: ").strip()
                create_Investigadores(id_investigador, id_usuario, NivelAcceso)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "2":
            try:
                id_investigador = int(input("Ingrese el id numérico del Investigador: "))
                read_Investigadores_by_id(id_investigador)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "3":
            try:
                id_investigador = int(input("Ingrese el id numérico del Investigador: "))
                read_Investigadores_by_id(id_investigador)
                print("⚠️ Si no deseas cambiar un campo, déjalo vacío.")
                NivelAcceso = input("Nuevo nivel de acceso: ").strip()
                update_Investigadores(id_investigador, NivelAcceso if NivelAcceso else None)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "4":
            try:
                id_investigador = int(input("Ingrese el id numérico del Investigador: "))
                delete_Investigador(id_investigador)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")
            input("Presiona ENTER para continuar...")


def menu_Libros():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu Libros                   |
            ==========================================
            | 1. Insertar Libro                      |
            |----------------------------------------|
            | 2. Leer Libro por Id                   |
            |----------------------------------------|
            | 3. Modificar Libro                     |
            |----------------------------------------|
            | 4. Eliminar Libro                      |
            |----------------------------------------|
            | 0. Volver al Menu Principal            |
            ==========================================
        """)
        opcion = input("Selecciona una opción [1-4, 0 para volver]: ").strip()

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break

        elif opcion == "1":
            try:
                id_libro = int(input("Ingrese el id numérico del Libro: "))
                id_estudiante = int(input("Ingrese el id numérico del Estudiante: "))
                nombre = input("Ingrese el nombre del Libro: ").strip()
                autor = input("Ingrese el autor del Libro: ").strip()
                anio_publicacion = int(input("Ingrese el año de publicación del Libro: "))
                CantidadPaginas = int(input("Ingrese la cantidad de páginas del Libro: "))
                cantidad = int(input("Ingrese la cantidad del Libro: "))
                Descripcion = input("Ingrese la descripción del Libro: ").strip()
                create_Libros(id_libro, id_estudiante, nombre, autor, anio_publicacion, CantidadPaginas, cantidad, Descripcion)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "2":
            try:
                id_libro = int(input("Ingrese el id numérico del Libro: "))
                read_Libros_by_id(id_libro)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "3":
            try:
                id_libro = int(input("Ingrese el id numérico del Libro: "))
                read_Libros_by_id(id_libro)
                print("⚠️ Si no deseas cambiar un campo, déjalo vacío.")
                nombre = input("Nuevo nombre: ").strip()
                autor = input("Nuevo autor: ").strip()
                anio_publicacion = input("Nuevo año de publicación: ").strip()
                CantidadPaginas = input("Nueva cantidad de páginas: ").strip()
                cantidad = input("Nueva cantidad: ").strip()
                Descripcion = input("Nueva descripción: ").strip()

                update_Libros(
                    id_libro,
                    nombre if nombre else None,
                    autor if autor else None,
                    int(anio_publicacion) if anio_publicacion else None,
                    int(CantidadPaginas) if CantidadPaginas else None,
                    int(cantidad) if cantidad else None,
                    Descripcion if Descripcion else None
                )
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "4":
            try:
                id_libro = int(input("Ingrese el id numérico del Libro: "))
                delete_Libro(id_libro)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")
            input("Presiona ENTER para continuar...")



import os

def menu_Prestamos():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu Prestamos                |
            ==========================================
            | 1. Insertar Prestamo                   |
            |----------------------------------------|
            | 2. Leer Prestamo por Id                |
            |----------------------------------------|
            | 3. Modificar Prestamo                  |
            |----------------------------------------|
            | 4. Eliminar Prestamo                   |
            |----------------------------------------|
            | 0. Volver al Menu Principal            |
            ==========================================
        """)
        opcion = input("Selecciona una opción [1-4, 0 para volver]: ").strip()

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break

        elif opcion == "1":
            try:
                id_prestamo = int(input("Ingrese el id numérico del Prestamo: "))
                id_estudiante = int(input("Ingrese el id numérico del Estudiante: "))
                id_libro = int(input("Ingrese el id numérico del Libro: "))
                cantidad = int(input("Ingrese la cantidad del Prestamo: "))
                fecha_prestamo = input("Ingrese la fecha de préstamo (YYYY-MM-DD): ").strip()
                fecha_devolucion = input("Ingrese la fecha de devolución (YYYY-MM-DD): ").strip()
                create_Prestamos(id_prestamo, id_estudiante, id_libro, cantidad, fecha_prestamo, fecha_devolucion)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "2":
            try:
                id_prestamo = int(input("Ingrese el id numérico del Prestamo: "))
                read_Prestamos_by_id(id_prestamo)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "3":
            try:
                id_prestamo = int(input("Ingrese el id numérico del Prestamo: "))
                print("⚠️ Si no deseas cambiar un campo, déjalo vacío.")
                cantidad = input("Nueva cantidad: ").strip()
                fecha_prestamo = input("Nueva fecha de préstamo (YYYY-MM-DD): ").strip()
                fecha_devolucion = input("Nueva fecha de devolución (YYYY-MM-DD): ").strip()

                update_Prestamos(
                    id_prestamo,
                    int(cantidad) if cantidad else None,
                    fecha_prestamo if fecha_prestamo else None,
                    fecha_devolucion if fecha_devolucion else None
                )
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "4":
            try:
                id_prestamo = int(input("Ingrese el id numérico del Prestamo: "))
                delete_Prestamo(id_prestamo)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")
            input("Presiona ENTER para continuar...")


def menu_DataSetsDescargados():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu DataSetsDescargados      |
            ==========================================
            | 1. Insertar DataSetDescargado          |
            |----------------------------------------|
            | 2. Leer DataSetDescargado por Id       |
            |----------------------------------------|
            | 3. Modificar DataSetDescargado         |
            |----------------------------------------|
            | 4. Eliminar DataSetDescargado          |
            |----------------------------------------|
            | 0. Volver al Menu Principal            |
            ==========================================
        """)
        opcion = input("Selecciona una opción [1-4, 0 para volver]: ").strip()

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break

        elif opcion == "1":
            try:
                id_Data_Set_Descargado = int(input("Ingrese el id numérico del DataSetDescargado: "))
                id_investigador = int(input("Ingrese el id numérico del Investigador: "))
                Nombre = input("Ingrese el nombre del DataSetDescargado: ").strip()
                Cantidad = int(input("Ingrese la cantidad del DataSetDescargado: "))
                create_DataSetsDescargados(id_Data_Set_Descargado, id_investigador, Nombre, Cantidad)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "2":
            try:
                id_Data_Set_Descargado = int(input("Ingrese el id numérico del DataSetDescargado: "))
                read_DataSetsDescargados_by_id(id_Data_Set_Descargado)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "3":
            try:
                id_Data_Set_Descargado = int(input("Ingrese el id numérico del DataSetDescargado: "))
                print("⚠️ Si no deseas cambiar un campo, déjalo vacío.")
                Nombre = input("Nuevo nombre: ").strip()
                Cantidad = input("Nueva cantidad: ").strip()

                update_DataSetsDescargados(
                    id_Data_Set_Descargado,
                    Nombre if Nombre else None,
                    int(Cantidad) if Cantidad else None
                )
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "4":
            try:
                id_Data_Set_Descargado = int(input("Ingrese el id numérico del DataSetDescargado: "))
                delete_Data_Set_Descargado(id_Data_Set_Descargado)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")
            input("Presiona ENTER para continuar...")


import os

def menu_MaterialExclusivo():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu MaterialExclusivo        |
            ==========================================
            | 1. Insertar MaterialExclusivo          |
            |----------------------------------------|
            | 2. Leer MaterialExclusivo por Id       |
            |----------------------------------------|
            | 3. Modificar MaterialExclusivo         |
            |----------------------------------------|
            | 4. Eliminar MaterialExclusivo          |
            |----------------------------------------|
            | 0. Volver al Menu Principal            |
            ==========================================
        """)
        opcion = input("Selecciona una opción [1-4, 0 para volver]: ").strip()

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break

        elif opcion == "1":
            try:
                id_material_exclusivo = int(input("Ingrese el id numérico del MaterialExclusivo: "))
                id_docente = int(input("Ingrese el id numérico del Docente asociado: "))
                nombre = input("Ingrese el nombre del MaterialExclusivo: ").strip()
                descripcion = input("Ingrese la descripción del MaterialExclusivo: ").strip()
                create_MaterialExclusivo(id_material_exclusivo, id_docente, nombre, descripcion)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "2":
            try:
                id_material_exclusivo = int(input("Ingrese el id numérico del MaterialExclusivo: "))
                read_MaterialExclusivo_by_id(id_material_exclusivo)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "3":
            try:
                id_material_exclusivo = int(input("Ingrese el id numérico del MaterialExclusivo: "))
                print("⚠️ Si no deseas cambiar un campo, déjalo vacío.")
                nombre = input("Nuevo nombre: ").strip()
                descripcion = input("Nueva descripción: ").strip()
                update_MaterialExclusivo(
                    id_material_exclusivo,
                    nombre if nombre else None,
                    descripcion if descripcion else None
                )
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "4":
            try:
                id_material_exclusivo = int(input("Ingrese el id numérico del MaterialExclusivo: "))
                delete_Material_Exclusivo(id_material_exclusivo)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")
            input("Presiona ENTER para continuar...")


def menu_Biblioteca():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu Biblioteca               |
            ==========================================
            | 1. Insertar Biblioteca                 |
            |----------------------------------------|
            | 2. Leer Biblioteca por Id              |
            |----------------------------------------|
            | 3. Modificar Biblioteca                |
            |----------------------------------------|
            | 4. Eliminar Biblioteca                 |
            |----------------------------------------|
            | 0. Volver al Menu Principal            |
            ==========================================
        """)
        opcion = input("Selecciona una opción [1-4, 0 para volver]: ").strip()

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break

        elif opcion == "1":
            try:
                id_biblioteca = int(input("Ingrese el id numérico de la Biblioteca: "))
                CantidadMaterial = int(input("Ingrese la cantidad de material: "))
                GestionPrestamo = int(input("Ingrese la cantidad de préstamos: "))
                create_Biblioteca(id_biblioteca, CantidadMaterial, GestionPrestamo)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "2":
            try:
                id_biblioteca = int(input("Ingrese el id numérico de la Biblioteca: "))
                read_Biblioteca_by_id(id_biblioteca)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "3":
            try:
                id_biblioteca = int(input("Ingrese el id numérico de la Biblioteca: "))
                print("⚠️ Si no deseas cambiar un campo, déjalo vacío.")
                CantidadMaterial = input("Nueva cantidad de material: ").strip()
                GestionPrestamo = input("Nueva cantidad de préstamos: ").strip()

                update_Biblioteca(
                    id_biblioteca,
                    int(CantidadMaterial) if CantidadMaterial else None,
                    int(GestionPrestamo) if GestionPrestamo else None
                )
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        elif opcion == "4":
            try:
                id_biblioteca = int(input("Ingrese el id numérico de la Biblioteca: "))
                delete_Biblioteca(id_biblioteca)
            except ValueError:
                print("⚠️ Ingresaste un valor no numérico.")
            input("Presiona ENTER para continuar...")

        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")
            input("Presiona ENTER para continuar...")


import os

def main():
    while True:
        os.system("cls")  # En Linux/Mac usar "clear"
        print(
            """
            ==========================================
            |          CRUD CON ORACLE SQL           |
            ==========================================
            | 1. Aplicar esquema en la base de datos |
            |----------------------------------------|
            | 2. Tabla Usuarios                      |
            |----------------------------------------|
            | 3. Tabla Estudiantes                   |
            |----------------------------------------|
            | 4. Tabla Docentes                      |
            |----------------------------------------|
            | 5. Tabla Investigadores                |
            |----------------------------------------|
            | 6. Tabla Libros                        |
            |----------------------------------------|
            | 7. Tabla Prestamos                     |
            |----------------------------------------|
            | 8. Tabla DataSetsDescargados           |
            |----------------------------------------|
            | 9. Tabla Biblioteca                    |
            |----------------------------------------|
            | 10. Tabla MaterialExclusivo            |
            |----------------------------------------|
            | 0. Salir                               |
            ==========================================
            """
        )
        opcion = input("Selecciona una opción [1-10, 0 para salir]: ").strip()

        if opcion == "0":
            print( "Adiós : ")
            input("Presiona ENTER para continuar...")
            break

        elif opcion == "1":
            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        # Primero eliminamos las tablas
                        for sql in drop_all_tables():
                            cur.execute(sql)
                        # Luego creamos las tablas
                        for sql in create_all_tables():
                            cur.execute(sql)
                    conn.commit()
                print("✔️ Esquema aplicado correctamente en la base de datos.")
            except Exception as e:
                print(f"❌ Error al aplicar esquema: {e}")
            input("Presiona ENTER para continuar...")

        elif opcion == "2":
            menu_Usuarios()
        elif opcion == "3":
            menu_Estudiantes()
        elif opcion == "4":
            menu_Docentes()
        elif opcion == "5":
            menu_Investigadores()
        elif opcion == "6":
            menu_Libros()
        elif opcion == "7":
            menu_Prestamos()
        elif opcion == "8":
            menu_DataSetsDescargados()
        elif opcion == "9":
            menu_Biblioteca()
        elif opcion == "10":
            menu_MaterialExclusivo()
        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")
            input("Presiona ENTER para continuar...")


if __name__ == "__main__":
    main()