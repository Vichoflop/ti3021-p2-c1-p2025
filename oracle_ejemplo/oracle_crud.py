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

def create_all_tables():
    tables = [
        (
            "CREATE TABLE Usuarios ("
            "id_usuario INTEGER PRIMARY KEY,"
            "nombre VARCHAR2(64),"
            "apellido VARCHAR2(64),"
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
            "id_usuario INTEGER,"
            "NivelAcceso VARCHAR2(50) NOT NULL"
            "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)"
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
            "Cantidad INTEGER NOT NULL,"
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
        "INSERT INTO Usuarios (id_usuario, nombre, apellido,correo) "
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
        err = e
        print(f"Error al insertar datos: {err}")


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


def update_Usuarios(id_usuario, nombre: Optional[str] = None, apellido: Optional[str] = None, correo: Optional[str] = None ):
    Modificaciones = []     
    parametros = {"id": id_usuario}     
    if nombre is not None:         
        Modificaciones.append("nombre =: nombre")         
        parametros["nombre"] = nombre   
    if apellido is not None:         
        Modificaciones.append("apellido =: apellido")         
        parametros["apellido"] = apellido                 
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
        os.system("cls")
        print("""
            ==========================================
            |          Menu Usuarios                 |
            ==========================================
            |----------------------------------------|
            ==========================================
            |1.Insertar Usuarios                     | 
            |----------------------------------------|
            |2. Leer Usuario por Id                  |
            |----------------------------------------|
            |3. Modificar Usuario                    |
            |----------------------------------------|
            |4. Eliminar Usuario                     |
            |----------------------------------------|
            |0. Volver al Menu Principal             |  
            |----------------------------------------|                                                        
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-4, 0 para volver al menu principal]: ")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id_usuario = int(input("Ingrese el id numerico del Usuario: "))
                nombre = input("Ingrese el nombre del Usuario: ")
                apellido = input("Ingrese el apellido del Usuario: ")
                correo = input("Ingrese el correo del Usuario: ")
                create_Usuario(id_usuario,nombre,apellido,correo)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_Usuarios()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_usuario = int(input("Ingrese el id numerico del Usuario: "))
                read_Usuario_by_id(id_usuario)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_usuario = int(input("Ingrese el id numerico del Usuario: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                nombre = input("Ingrese el nombre del Usuario: ")
                apellido = input("Ingrese el apellido del Usuario: ")
                correo = input("Ingrese el correo del Usuario: ")
                if len(nombre.strip()) == 0:
                    nombres = None
                if len(apellido.strip()) == 0:
                    apellidos = None
                if len(correo.strip()) == 0:
                    correo = None
                update_Usuario(id_usuario,nombre,apellido,correo)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id_usuario = int(input("Ingrese el id numerico del usuario: "))
                delete_Usuario(id_usuario)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break


def menu_Estudiantes():
    while True:
        os.system("cls")       
        print("""
            ==========================================
            |          Menu Estudiantes              |
            ==========================================
            |----------------------------------------|
            ==========================================
            |1.Insertar Estudiantes                  | 
            |----------------------------------------|
            |2. Leer Estudiante por Id               |
            |----------------------------------------|
            |3. Modificar Estudiante                 |
            |----------------------------------------|
            |4. Eliminar Estudiante                  |
            |----------------------------------------|
            |0. Volver al Menu Principal             |  
            |----------------------------------------|                                                        
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-4, 0 para volver al menu principal]: ")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id_estudiante = int(input("Ingrese el id numerico del Estudiante: "))
                prestamos_activos = int(input("Ingrese la cantidad de prestamos activos del Estudiante: "))
                opciones_validas = ["pendiente", "devuelto", "retrasado"]
                estado_deuda = input("Ingrese el estado de deuda del Estudiante (pendiente-devuelto-retrasado): ")
                while estado_deuda not in opciones_validas:
                    print("❌ Opción no válida. Debe ingresar: pendiente, devuelto o retrasado.")
                    estado_deuda = input("Ingrese nuevamente el estado de deuda: ").strip().lower()
                print("✔️ Estado de deuda registrado correctamente:", estado_deuda)
                create_Estudiante(id_estudiante,prestamos_activos,estado_deuda)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_Estudiantes()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_estudiante = int(input("Ingrese el id numerico del Estudiante: "))
                read_Estudiante_by_id(id_estudiante)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_estudiante = int(input("Ingrese el id numerico del Estudiante: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                prestamos_activos = input("Ingrese la cantidad de prestamos activos del Estudiante: ")
                estado_deuda = input("Ingrese el estado de deuda del Estudiante: ")
                if len(prestamos_activos.strip()) == 0:
                    prestamos_activos = None
                if len(estado_deuda.strip()) == 0:
                    estado_deuda = None
                update_Estudiante(id_estudiante,prestamos_activos,estado_deuda)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id_estudiante = int(input("Ingrese el id numerico del estudiante: "))
                delete_Estudiante(id_estudiante)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break

        
def menu_Docentes():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu Docentes                 |
            ==========================================
            |----------------------------------------|
            ==========================================
            |1.Insertar Docentes                     | 
            |----------------------------------------|
            |2. Leer Docente por Id                  |
            |----------------------------------------|
            |3. Modificar Docente                    |
            |----------------------------------------|
            |4. Eliminar Docente                     |
            |----------------------------------------|
            |0. Volver al Menu Principal             |  
            |----------------------------------------|                                                        
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-4, 0 para volver al menu principal]: ")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id_docente = int(input("Ingrese el id numerico del Docente: "))
                material_exclusivo_accedido = input("Ingrese el material exclusivo accedido del Docente: ")
                create_Docente(id_docente,material_exclusivo_accedido)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_Docentes()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_docente = int(input("Ingrese el id numerico del Docente: "))
                read_Docente_by_id(id_docente)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_docente = int(input("Ingrese el id numerico del Docente: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                material_exclusivo_accedido = input("Ingrese el material exclusivo accedido del Docente: ")
                if len(material_exclusivo_accedido.strip()) == 0:
                    material_exclusivo_accedido = None
                update_Docente(id_docente,material_exclusivo_accedido)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id_docente = int(input("Ingrese el id numerico del docente: "))
                delete_Docente(id_docente)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break



def menu_Investigadores():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu Investigadores           |
            ==========================================
            |----------------------------------------|
            ==========================================
            |1.Insertar Investigadores               | 
            |----------------------------------------|
            |2. Leer Investigador por Id             |
            |----------------------------------------|
            |3. Modificar Investigador               |
            |----------------------------------------|
            |4. Eliminar Investigador                |
            |----------------------------------------|
            |0. Volver al Menu Principal             |  
            |----------------------------------------|                                                        
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-4, 0 para volver al menu principal]: ")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id_investigador = int(input("Ingrese el id numerico del Investigador: "))
                nivel_acceso = input("Ingrese el nivel de acceso del Investigador: ")
                create_Investigador(id_investigador,nivel_acceso)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_Investigadores()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_investigador = int(input("Ingrese el id numerico del Investigador: "))
                read_Investigador_by_id(id_investigador)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_investigador = int(input("Ingrese el id numerico del Investigador: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                nivel_acceso = input("Ingrese el nivel de acceso del Investigador: ")
                if len(nivel_acceso.strip()) == 0:
                    nivel_acceso = None
                update_Investigador(id_investigador,nivel_acceso)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id_investigador = int(input("Ingrese el id numerico del investigador: "))
                delete_investigador(id_investigador)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break



def menu_Libros():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu Libros                   |
            ==========================================
            |----------------------------------------|
            ==========================================
            |1.Insertar Libros                       | 
            |----------------------------------------|
            |2. Leer Libro por Id                    |
            |----------------------------------------|
            |3. Modificar Libro                      |
            |----------------------------------------|
            |4. Eliminar Libro                       |
            |----------------------------------------|
            |0. Volver al Menu Principal             |  
            |----------------------------------------|                                                        
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-4, 0 para volver al menu principal]: ")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id_libro = int(input("Ingrese el id numerico del Libro: "))
                nombre = input("Ingrese el nombre del Libro: ")
                autor = input("Ingrese el autor del Libro: ")
                anio_publicacion = int(input("Ingrese el año de publicación del Libro: "))
                cantidad_paginas = int(input("Ingrese la cantidad de páginas del Libro: "))
                cantidad = int(input("Ingrese la cantidad del Libro: "))
                descripcion = input("Ingrese la descripción del Libro: ")
                create_Libro(id_libro,nombre,autor,anio_publicacion,cantidad_paginas,cantidad,descripcion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_Libros()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_libro = int(input("Ingrese el id numerico del Libro: "))
                read_Libro_by_id(id_libro)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_libro = int(input("Ingrese el id numerico del Libro: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                nombre = input("Ingrese el nombre del Libro: ")
                autor = input("Ingrese el autor del Libro: ")
                anio_publicacion = input("Ingrese el año de publicación del Libro: ")
                cantidad_paginas = input("Ingrese la cantidad de páginas del Libro: ")
                cantidad = input("Ingrese la cantidad del Libro: ")
                descripcion = input("Ingrese la descripción del Libro: ")
                if len(nombre.strip()) == 0:
                    nombre = None
                if len(autor.strip()) == 0:
                    autor = None
                if len(anio_publicacion.strip()) == 0:
                    anio_publicacion = None
                if len(cantidad_paginas.strip()) == 0:
                    cantidad_paginas = None
                if len(cantidad.strip()) == 0:
                    cantidad = None
                if len(descripcion.strip()) == 0:
                    descripcion = None
                update_Libro(id_libro,nombre,autor,anio_publicacion,cantidad_paginas,cantidad,descripcion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id_libro = int(input("Ingrese el id numerico del libro: "))
                delete_Libro(id_libro)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break



def menu_Prestamos():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu Prestamos                |
            ==========================================
            |----------------------------------------|
            ==========================================
            |1.Insertar Prestamos                    | 
            |----------------------------------------|
            |2. Leer Prestamo por Id                 |
            |----------------------------------------|
            |3. Modificar Prestamo                   |
            |----------------------------------------|
            |4. Eliminar Prestamo                    |
            |----------------------------------------|
            |0. Volver al Menu Principal             |  
            |----------------------------------------|                                                        
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-4, 0 para volver al menu principal]: ")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id_prestamo = int(input("Ingrese el id numerico del Prestamo: "))
                cantidad = int(input("Ingrese la cantidad del Prestamo: "))
                fecha_prestamo = input("Ingrese la fecha de prestamo del Prestamo (YYYY-MM-DD): ")
                fecha_devolucion = input("Ingrese la fecha de devolucion del Prestamo (YYYY-MM-DD): ")
                create_Prestamo(id_prestamo,cantidad,fecha_prestamo,fecha_devolucion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_Prestamos()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_prestamo = int(input("Ingrese el id numerico del Prestamo: "))
                read_Prestamo_by_id(id_prestamo)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_prestamo = int(input("Ingrese el id numerico del Prestamo: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                cantidad = input("Ingrese la cantidad del Prestamo: ")
                fecha_prestamo = input("Ingrese la fecha de prestamo del Prestamo (YYYY-MM-DD): ")
                fecha_devolucion = input("Ingrese la fecha de devolucion del Prestamo (YYYY-MM-DD): ")
                if len(cantidad.strip()) == 0:
                    cantidad = None
                if len(fecha_prestamo.strip()) == 0:
                    fecha_prestamo = None
                if len(fecha_devolucion.strip()) == 0:
                    fecha_devolucion = None
                update_Prestamo(id_prestamo,cantidad,fecha_prestamo,fecha_devolucion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id_prestamo = int(input("Ingrese el id numerico del prestamo: "))
                delete_prestamo(id_prestamo)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break



def menu_DataSetsDescargados():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu DataSetsDescargados      |
            ==========================================
            |----------------------------------------|
            ==========================================
            |1.Insertar DataSetsDescargados          | 
            |----------------------------------------|
            |2. Leer DataSetDescargado por Id        |
            |----------------------------------------|
            |3. Modificar DataSetDescargado          |
            |----------------------------------------|
            |4. Eliminar DataSetDescargado           |
            |----------------------------------------|
            |0. Volver al Menu Principal             |  
            |----------------------------------------|                                                        
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-4, 0 para volver al menu principal]: ")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id_Data_Set_Descargado = int(input("Ingrese el id numerico del DataSetDescargado: "))
                Nombre = input("Ingrese el nombre del DataSetDescargado: ")
                Cantidad = int(input("Ingrese la cantidad del DataSetDescargado: "))
                create_DataSetDescargado(id_Data_Set_Descargado,Nombre,Cantidad)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_DataSetsDescargados()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_Data_Set_Descargado = int(input("Ingrese el id numerico del DataSetDescargado: "))
                read_DataSetDescargado_by_id(id_Data_Set_Descargado)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_Data_Set_Descargado = int(input("Ingrese el id numerico del DataSetDescargado: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                Nombre = input("Ingrese el nombre del DataSetDescargado: ")
                Cantidad = input("Ingrese la cantidad del DataSetDescargado: ")
                if len(Nombre.strip()) == 0:
                    Nombre = None
                if len(Cantidad.strip()) == 0:
                    Cantidad = None
                update_DataSetsDescargados(id_Data_Set_Descargado,Nombre,Cantidad)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id_Data_Set_Descargado = int(input("Ingrese el id numerico del DataSetDescargado: "))
                delete_Data_Set_Descargado(id_Data_Set_Descargado)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break



def menu_Biblioteca():    
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu Biblioteca               |
            ==========================================
            |----------------------------------------|
            ==========================================
            |1.Insertar Biblioteca                   | 
            |----------------------------------------|
            |2. Leer Biblioteca por Id               |
            |----------------------------------------|
            |3. Modificar Biblioteca                 |
            |----------------------------------------|
            |4. Eliminar Biblioteca                  |
            |----------------------------------------|
            |0. Volver al Menu Principal             |  
            |----------------------------------------|                                                        
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-4, 0 para volver al menu principal]: ")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id_biblioteca = int(input("Ingrese el id numerico del Biblioteca: "))
                nombre = input("Ingrese el nombre del Biblioteca: ")
                ubicacion = input("Ingrese la ubicacion del Biblioteca: ")
                create_Biblioteca(id_biblioteca,nombre,ubicacion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_Bibliotecas()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_biblioteca = int(input("Ingrese el id numerico del Biblioteca: "))
                read_Biblioteca_by_id(id_biblioteca)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4": 
            try:
                id_biblioteca = int(input("Ingrese el id numerico del Biblioteca: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                nombre = input("Ingrese el nombre del Biblioteca: ")
                ubicacion = input("Ingrese la ubicacion del Biblioteca: ")
                if len(nombre.strip()) == 0:
                    nombre = None
                if len(ubicacion.strip()) == 0:
                    ubicacion = None
                update_Biblioteca(id_biblioteca,nombre,ubicacion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id_biblioteca = int(input("Ingrese el id numerico del biblioteca: "))
                delete_Biblioteca(id_biblioteca)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break

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
            create_all_tables()
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
        else:
            print("Opcion invalida")
            print("Presiona ENTER para continuar...")
            break


if __name__ == "__main__":
    main()