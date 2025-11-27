from typing import Optional
import oracledb
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

username= os.getenv("prueba_poo")
dsn = os.getenv("localhost:1521/XEPDB1")
password = os.getenv("prueba_poo")

def get_connection():
    return oracledb.connect(user = username, password = password, dsn = dsn)

def create_schema(query):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                print(f"Tabla creada \n {query}")
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
            "correo varchar2(50)"
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
            "id_material_exclusivo  INTEGER,"
            "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),"
            "FOREIGN KEY (id_material_exclusivo) REFERENCES Usuarios(id_material_exclusivo)"
            ")"
        ),
        (
            "CREATE TABLE Investigadores ("
            "id_investigador INTEGER PRIMARY KEY,"
            "id_usuario INTEGER,"
            "id_Data_Set_Descargado  INTEGER,"
            "NivelAcceso VARCHAR2(100) NOT NULL,"
            "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),"
            "FOREIGN KEY (id_Data_Set_Descargado) REFERENCES Usuarios(id_Data_Set_Descargado),"
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
            "FOREIGN KEY (id_libro) REFERENCES Libro(id_libro)"
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
            "id_material_exclusivo  INTEGER PRIMARY KEY,"
            "id_docente             INTEGER NOT NULL,"
            "nombre                 VARCHAR2(150) NOT NULL,"
            "Descripcion            VARCHAR2(300) NOT NULL,"
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

def create_Usuarios(
        id_usuario: int,
        nombre: str,
        apellido: str,
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
        id_material_exclusivo: int,
        PrestamosActivos: int,
        Estado: str
):
    sql = (
        "INSERT INTO Estudiantes (id_estudiante, id_usuario,id_material_exclusivo, PrestamosActivos, Estado) "
        "VALUES (:id_estudiante, :id_usuario,:id_material_exclusivo, :PrestamosActivos, :Estado)"
    )
    parametros = {
        "id_estudiante": id_estudiante,
        "id_usuario": id_usuario,
        "id_material_exclusivo": id_material_exclusivo,
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
        id_Data_Set_Descargado: int,
        NivelAcceso: str
):
    sql = (
        "INSERT INTO Investigadores (id_investigador,id_usuario, id_Data_Set_Descargado, NivelAcceso) "
        "VALUES (:id_investigador, :id_usuario,:id_Data_Set_Descargado, :NivelAcceso)"
    )
    parametros = {
        "id_investigador": id_investigador,
        "id_usuario": id_usuario,
        "id_Data_Set_Descargado": id_Data_Set_Descargado,
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


def read_MaterialExclusivo():
    sql = (
        "Select * from MaterialExclusivo"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print("Consulta a la tabla MaterialExclusivo")
                for row in resultados:
                    print(row)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err}")


def read_MaterialExclusivo_by_id(id_material_exclusivo):
    sql = (
        "Select * from MaterialExclusivo where id_material_exclusivo = :id"
    )

    parametros = {"id_material_exclusivo": id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print("Consulta a la tabla MaterialExclusivo")
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


def update_Estudiantes(id_estudiante,PrestamosActivos: Optional[int] = None,Estado: Optional[str] = None):
    modificaciones = []     
    parametros = {"id": id_estudiante}
    if PrestamosActivos is not None:         
        modificaciones.append("PrestamosActivos =: PrestamosActivos")         
        parametros["PrestamosActivos"] = PrestamosActivos
    if Estado is not None:         
        modificaciones.append("Estado =: Estado")         
        parametros["Estado"] = Estado
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

def update_MaterialExclusivo(id_material_exclusivo: int,nombre: Optional[str] = None,Descripcion: Optional[str] = None):
    modificaciones = []     
    parametros = {"id": id_material_exclusivo}
    if nombre is not None:         
        modificaciones.append("nombre =: nombre")         
        parametros["nombre"] = nombre
    if Descripcion is not None:         
        modificaciones.append("Descripcion =: Descripcion")         
        parametros["Descripcion"] = Descripcion
    if not modificaciones:         
        print("No hay campos para actualizar.")         
        return

    sql = "UPDATE MaterialExclusivo SET " + ", ".join(modificaciones) + " WHERE id_material_exclusivo =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"MaterialExclusivo con ID={id_material_exclusivo} actualizado.")
    

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




def delete_Prestamo(id_prestamo:int):
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

def delete_Material_Exclusivo(id_material_exclusivo:int):
    sql ={
        "DELETE FROM Usuarios WHERE id_material_exclusivo = :id"
    }

    parametros = {"id": id_material_exclusivo}
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
                if nombre and apellido:
                    correo = f"{nombre.lower()}.{apellido.lower()}@correo.cl"
                    print(f"📧 Nuevo correo generado: {correo}")
                else:
                    correo = None
                create_Usuarios(id_usuario,nombre,apellido,correo)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            id_usuario = int(input("Ingrese el id numerico del Usuario: "))
            read_Usuarios_by_id(id_usuario)
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_usuario = int(input("Ingrese el id numerico del Usuario: "))
                read_Usuarios_by_id(id_usuario)
                print("⚠️ Si no deseas cambiar un campo, déjalo vacío.")
                nombre = input("Nuevo nombre: ").strip()
                apellido = input("Nuevo apellido: ").strip()
                if nombre and apellido:
                    correo = f"{nombre.lower()}.{apellido.lower()}@correo.cl"
                    print(f"📧 Nuevo correo generado: {correo}")
                else:
                    correo = None
                update_Usuarios(id_usuario,nombre if nombre else None,apellido if apellido else None,correo)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_usuario = int(input("Ingrese el id numerico del usuario: "))
                delete_Usuario(id_usuario)
            except ValueError:
                print("Ingresaste un valor no númerico")
               

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
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
                id_usuario = int(input("Ingrese el id numerico del usuario: "))
                id_material_exclusivo = int(input("Ingrese el id numerico del Material Exclusivo: "))
                prestamos_activos = int(input("Ingrese la cantidad de prestamos activos del Estudiante: "))
                opciones_validas = ["pendiente", "devuelto", "retrasado"]
                Estado = input("Ingrese el Estado de deuda del Estudiante (pendiente-devuelto-retrasado): ")
                while Estado not in opciones_validas:
                    print("❌ Opción no válida. Debe ingresar: pendiente, devuelto o retrasado.")
                    Estado = input("Ingrese nuevamente el Estado de deuda: ").strip().lower()
                print("✔️ Estado de deuda registrado correctamente:", Estado)
                create_Estudiantes(id_estudiante,id_usuario,id_material_exclusivo,  prestamos_activos,Estado)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            id_estudiante = int(input("Ingrese el id numerico del Estudiante: "))
            read_Estudiantes_by_id(id_estudiante)
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_estudiante = int(input("Ingrese el id numerico del Estudiante: "))
                read_Estudiantes_by_id(id_estudiante)
                print("⚠️ Si no deseas cambiar un campo, déjalo vacío.")
                prestamos_activos = input("Nueva cantidad de prestamos activos: ").strip()
                Estado = input("Nuevo Estado de deuda (pendiente-devuelto-retrasado): ").strip().lower()
                update_Estudiantes(id_estudiante,prestamos_activos,Estado)               
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_estudiante = int(input("Ingrese el id numerico del estudiante: "))
                delete_Estudiante(id_estudiante)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":            
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
                id_usuario = int(input("Ingrese el id numerico del usuario: "))
                id_material_exclusivo = int(input("Ingrese el id numerico del material exclusivo: "))
                create_Docentes(id_docente, id_usuario,id_material_exclusivo )
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            id_docente = int(input("Ingrese el id numerico del Docente: "))
            id_usuario = int(input("Ingrese el id numerico del usuario: "))
            id_material_exclusivo = int(input("Ingrese el id numerico del material exclusivo: "))
            read_Docentes_by_id(id_docente,id_usuario,id_material_exclusivo  )
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_docente = int(input("Ingrese el id numerico del Docente: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                id_usuario = int(input("Ingrese el id numerico del usuario: "))
                id_material_exclusivo = int(input("Ingrese el id numerico del material exclusivo: "))
                update_Docentes(id_docente, id_usuario,id_material_exclusivo)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_docente = int(input("Ingrese el id numerico del docente: "))
                delete_Docente(id_docente)
            except ValueError:
                print("Ingresaste un valor no númerico")
        elif opcion == "5":
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
                id_usuario = int(input("Ingrese el id numerico del usuario: "))
                id_Data_Set_Descargado = int(input("Ingrese el id numerico del Data Set Descargado: "))
                NivelAcceso = input("Ingrese el nivel de acceso del Investigador: ")
                create_Investigadores(id_investigador, id_usuario,id_Data_Set_Descargado, NivelAcceso)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            id_investigador = int(input("Ingrese el id numerico del Investigador: "))
            read_Investigadores_by_id(id_investigador)
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_investigador = int(input("Ingrese el id numerico del Investigador: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                id_usuario = int(input("Ingrese el id numerico del usuario: "))
                id_Data_Set_Descargado = int(input("Ingrese el id numerico del Data Set Descargado: "))
                NivelAcceso = input("Ingrese el nivel de acceso del Investigador: ")
                if len(NivelAcceso.strip()) == 0:
                    NivelAcceso = None
                update_Investigadores(id_investigador,id_usuario,id_Data_Set_Descargado, NivelAcceso)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_investigador = int(input("Ingrese el id numerico del investigador: "))
                delete_investigador(id_investigador)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "5":
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
                id_prestamo = int(input("Ingrese el id numerico del prestamo: "))
                nombre = input("Ingrese el nombre del Libro: ")
                autor = input("Ingrese el autor del Libro: ")
                anio_publicacion = int(input("Ingrese el año de publicación del Libro: "))
                CantidadPaginas = int(input("Ingrese la cantidad de páginas del Libro: "))
                cantidad = int(input("Ingrese la cantidad del Libro: "))
                Descripcion = input("Ingrese la descripción del Libro: ")
                create_Libros(id_libro,id_prestamo,nombre,autor,anio_publicacion,CantidadPaginas,cantidad,Descripcion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            id_libro = int(input("Ingrese el id numerico del Libro: "))
            read_Libros_by_id(id_libro)
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_libro = int(input("Ingrese el id numerico del Libro: "))
                id_prestamo = int(input("Ingrese el id numerico del prestamo: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                nombre = input("Ingrese el nombre del Libro: ")
                autor = input("Ingrese el autor del Libro: ")
                anio_publicacion = input("Ingrese el año de publicación del Libro: ")
                CantidadPaginas = input("Ingrese la cantidad de páginas del Libro: ")
                cantidad = input("Ingrese la cantidad del Libro: ")
                Descripcion = input("Ingrese la descripción del Libro: ")
                if len(nombre.strip()) == 0:
                    nombre = None
                if len(autor.strip()) == 0:
                    autor = None
                if len(anio_publicacion.strip()) == 0:
                    anio_publicacion = None
                if len(CantidadPaginas.strip()) == 0:
                    CantidadPaginas = None
                if len(cantidad.strip()) == 0:
                    cantidad = None
                if len(Descripcion.strip()) == 0:
                    Descripcion = None
                update_Libros(id_libro,nombre,autor,anio_publicacion,CantidadPaginas,cantidad,Descripcion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_libro = int(input("Ingrese el id numerico del libro: "))
                delete_Libro(id_libro)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "5":
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
                id_estudiante = int(input("Ingrese el id numerico del estudiante: "))
                id_libro = int(input("Ingrese el id numerico del libro: "))
                cantidad = int(input("Ingrese la cantidad del Prestamo: "))
                fecha_prestamo = input("Ingrese la fecha de prestamo del Prestamo (YYYY-MM-DD): ")
                fecha_devolucion = input("Ingrese la fecha de devolucion del Prestamo (YYYY-MM-DD): ")
                create_Prestamos(id_prestamo,id_estudiante,id_libro,cantidad,fecha_prestamo,fecha_devolucion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            try:
                id_prestamo = int(input("Ingrese el id numerico del Prestamo: "))
                read_Prestamos_by_id(id_prestamo)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
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
                update_Prestamos(id_prestamo,cantidad,fecha_prestamo,fecha_devolucion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_prestamo = int(input("Ingrese el id numerico del prestamo: "))
                delete_Prestamo(id_prestamo)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
        elif opcion == "5":
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
                id_investigador = int(input("Ingrese el id numerico del usuario: "))
                Nombre = input("Ingrese el nombre del DataSetDescargado: ")
                Cantidad = int(input("Ingrese la cantidad del DataSetDescargado: "))
                create_DataSetsDescargados(id_Data_Set_Descargado,id_investigador,Nombre,Cantidad)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            try:
                id_Data_Set_Descargado = int(input("Ingrese el id numerico del DataSetDescargado: "))
                read_DataSetsDescargados_by_id(id_Data_Set_Descargado)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
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
        elif opcion == "4":
            try:
                id_Data_Set_Descargado = int(input("Ingrese el id numerico del DataSetDescargado: "))
                delete_Data_Set_Descargado(id_Data_Set_Descargado)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break


def menu_MaterialExclusivo():
    while True:
        os.system("cls")
        print("""
            ==========================================
            |          Menu MaterialExclusivo        |
            ==========================================
            |----------------------------------------|
            ==========================================
            |1.Insertar MaterialExclusivo            | 
            |----------------------------------------|
            |2. Leer MaterialExclusivo por Id        |
            |----------------------------------------|
            |3. Modificar MaterialExclusivo          |
            |----------------------------------------|
            |4. Eliminar MaterialExclusivo           |
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
                id_material_exclusivo = int(input("Ingrese el id numerico del MaterialExclusivo: "))
                id_docente = int(input("Ingrese el id numerico del Docente asociado: "))
                nombre = input("Ingrese el nombre del MaterialExclusivo: ")
                descripcion = input("Ingrese la descripcion del MaterialExclusivo: ")
                create_MaterialExclusivo(id_material_exclusivo,id_docente,nombre,descripcion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            try:
                id_material_exclusivo = int(input("Ingrese el id numerico del MaterialExclusivo: "))
                read_MaterialExclusivo_by_id(id_material_exclusivo)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id_material_exclusivo = int(input("Ingrese el id numerico del MaterialExclusivo: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                id_docente = input("Ingrese el id numerico del Docente asociado: ")
                nombre = input("Ingrese el nombre del MaterialExclusivo: ")
                Descripcion = input("Ingrese la descripcion del MaterialExclusivo: ")
                if len(id_docente.strip()) == 0:
                    id_docente = None
                if len(nombre.strip()) == 0:
                    nombre = None
                if len(Descripcion.strip()) == 0:
                    Descripcion = None
                update_MaterialExclusivo(id_material_exclusivo,id_docente,nombre,Descripcion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id_material_exclusivo = int(input("Ingrese el id numerico del MaterialExclusivo: "))
                delete_Material_Exclusivo(id_material_exclusivo)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "5":
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
            |0. Volver al Menu Principal             |  
            |----------------------------------------|                                                        
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-3, 0 para volver al menu principal]: ")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal ヾ(•ω•`)o")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id_biblioteca = int(input("Ingrese el id numerico del Biblioteca: "))
                CantidadMaterial = int(input("Ingrese la cantidad de material: "))
                GestionPrestamo = (input("Ingrese la cantidad de prestamos: "))
                create_Biblioteca(id_biblioteca,CantidadMaterial,GestionPrestamo)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            try:
                id_biblioteca = int(input("Ingrese el id numerico del Biblioteca: "))
                read_Biblioteca_by_id(id_biblioteca)
            except ValueError:
                print("Ingresaste un valor no númerico")
        elif opcion == "3":
            try:
                id_biblioteca = int(input("Ingrese el id numerico del Biblioteca: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                CantidadMaterial = int(input("Ingrese el nombre del Biblioteca: "))
                GestionPrestamo = (input("Ingrese la ubicacion del Biblioteca: "))
                if len(nombre.strip()) == 0:
                    nombre = None
                if len(ubicacion.strip()) == 0:
                    ubicacion = None
                update_Biblioteca(id_biblioteca,CantidadMaterial,GestionPrestamo)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "4":
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
            |10. TABLA MATERIALEXCLUSIVO             |
            |----------------------------------------|
            |0. SALIR                                |  
            |----------------------------------------|                                                        
            ==========================================
            """
        )
        opcion = input("Selecciona una opcion [1-10, 0 para salir] : ")

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
        elif opcion == "10":
            menu_MaterialExclusivo()
        else:
            print("Opcion invalida")
            print("Presiona ENTER para continuar...")
            break


if __name__ == "__main__":
    main()