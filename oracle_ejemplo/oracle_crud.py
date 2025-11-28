from typing import Optional
from dotenv import load_dotenv
from datetime import datetime
import oracledb
import os

load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)

def create_schema(query):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        # Ignorar error si la tabla no existe (ORA-00942)
        if "ORA-00942" not in str(e):
            print(f"Error en base de datos: {e}")

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
            "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)"
            ")"
        ),
        (
            "CREATE TABLE Investigadores ("
            "id_investigador INTEGER PRIMARY KEY,"
            "id_usuario INTEGER,"
            "NivelAcceso VARCHAR2(100) NOT NULL,"
            "FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)"
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
    for table in drop_order:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
            connection.commit()
            cursor.close()
            connection.close()
        except oracledb.DatabaseError as e:
            # Ignorar si la tabla no existe
            if "ORA-00942" not in str(e):
                print(f"Error al eliminar {table}: {e}")

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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def read_Usuarios():
    sql = "SELECT * FROM Usuarios"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultados
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return []

def read_Usuarios_by_id(id_usuario):
    sql = "SELECT * FROM Usuarios WHERE id_usuario = :id_usuario"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_usuario": id_usuario})
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return None

def read_Estudiantes():
    sql = "SELECT * FROM Estudiantes"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultados
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return []

def read_Estudiantes_by_id(id_estudiante):
    sql = "SELECT * FROM Estudiantes WHERE id_estudiante = :id_estudiante"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_estudiante": id_estudiante})
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return None

def read_Docentes():
    sql = "SELECT * FROM Docentes"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultados
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return []

def read_Docentes_by_id(id_docente):
    sql = "SELECT * FROM Docentes WHERE id_docente = :id_docente"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_docente": id_docente})
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return None

def read_Investigadores():
    sql = "SELECT * FROM Investigadores"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultados
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return []

def read_Investigadores_by_id(id_investigador):
    sql = "SELECT * FROM Investigadores WHERE id_investigador = :id_investigador"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_investigador": id_investigador})
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return None

def read_Libros():
    sql = "SELECT * FROM Libros"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultados
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return []

def read_Libros_by_id(id_libro):
    sql = "SELECT * FROM Libros WHERE id_libro = :id_libro"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_libro": id_libro})
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return None

def read_Prestamos():
    sql = "SELECT * FROM Prestamos"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultados
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return []

def read_Prestamos_by_id(id_prestamo):
    sql = "SELECT * FROM Prestamos WHERE Id_prestamo = :id_prestamo"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_prestamo": id_prestamo})
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return None

def read_DataSetsDescargados():
    sql = "SELECT * FROM DataSetsDescargados"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultados
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return []

def read_DataSetsDescargados_by_id(id_Data_Set_Descargado):
    sql = "SELECT * FROM DataSetsDescargados WHERE id_Data_Set_Descargado = :id_Data_Set_Descargado"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_Data_Set_Descargado": id_Data_Set_Descargado})
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return None

def read_MaterialExclusivo():
    sql = "SELECT * FROM MaterialExclusivo"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultados
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return []

def read_MaterialExclusivo_by_id(id_material_exclusivo):
    sql = "SELECT * FROM MaterialExclusivo WHERE id_material_exclusivo = :id_material_exclusivo"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_material_exclusivo": id_material_exclusivo})
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return None

def read_Biblioteca():
    sql = "SELECT * FROM Biblioteca"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultados
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return []

def read_Biblioteca_by_id(id_biblioteca):
    sql = "SELECT * FROM Biblioteca WHERE id_biblioteca = :id_biblioteca"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_biblioteca": id_biblioteca})
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")
        return None

def update_Usuarios(id_usuario: int, nombre: Optional[str] = None, apellido: Optional[str] = None, correo: Optional[str] = None):
    updates = []
    parametros = {"id_usuario": id_usuario}
    
    if nombre is not None:
        updates.append("nombre = :nombre")
        parametros["nombre"] = nombre
    if apellido is not None:
        updates.append("apellido = :apellido")
        parametros["apellido"] = apellido
    if correo is not None:
        updates.append("correo = :correo")
        parametros["correo"] = correo
    
    if not updates:
        print("❌ No hay campos para actualizar")
        return
    
    sql = f"UPDATE Usuarios SET {', '.join(updates)} WHERE id_usuario = :id_usuario"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Usuario actualizado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def update_Estudiantes(id_estudiante: int, PrestamosActivos: Optional[int] = None, Estado: Optional[str] = None):
    updates = []
    parametros = {"id_estudiante": id_estudiante}
    
    if PrestamosActivos is not None:
        updates.append("PrestamosActivos = :PrestamosActivos")
        parametros["PrestamosActivos"] = PrestamosActivos
    if Estado is not None:
        updates.append("Estado = :Estado")
        parametros["Estado"] = Estado
    
    if not updates:
        print("❌ No hay campos para actualizar")
        return
    
    sql = f"UPDATE Estudiantes SET {', '.join(updates)} WHERE id_estudiante = :id_estudiante"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Estudiante actualizado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def update_Docentes(id_docente: int, id_usuario: Optional[int] = None):
    updates = []
    parametros = {"id_docente": id_docente}
    
    if id_usuario is not None:
        updates.append("id_usuario = :id_usuario")
        parametros["id_usuario"] = id_usuario
    
    if not updates:
        print("❌ No hay campos para actualizar")
        return
    
    sql = f"UPDATE Docentes SET {', '.join(updates)} WHERE id_docente = :id_docente"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Docente actualizado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def update_Investigadores(id_investigador: int, NivelAcceso: Optional[str] = None):
    updates = []
    parametros = {"id_investigador": id_investigador}
    
    if NivelAcceso is not None:
        updates.append("NivelAcceso = :NivelAcceso")
        parametros["NivelAcceso"] = NivelAcceso
    
    if not updates:
        print("❌ No hay campos para actualizar")
        return
    
    sql = f"UPDATE Investigadores SET {', '.join(updates)} WHERE id_investigador = :id_investigador"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Investigador actualizado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def update_Libros(id_libro: int, nombre: Optional[str] = None, autor: Optional[str] = None,
                  anio_publicacion: Optional[int] = None, CantidadPaginas: Optional[int] = None,
                  Cantidad: Optional[int] = None, Descripcion: Optional[str] = None):
    updates = []
    parametros = {"id_libro": id_libro}
    
    if nombre is not None:
        updates.append("nombre = :nombre")
        parametros["nombre"] = nombre
    if autor is not None:
        updates.append("autor = :autor")
        parametros["autor"] = autor
    if anio_publicacion is not None:
        updates.append("anio_publicacion = :anio_publicacion")
        parametros["anio_publicacion"] = anio_publicacion
    if CantidadPaginas is not None:
        updates.append("CantidadPaginas = :CantidadPaginas")
        parametros["CantidadPaginas"] = CantidadPaginas
    if Cantidad is not None:
        updates.append("Cantidad = :Cantidad")
        parametros["Cantidad"] = Cantidad
    if Descripcion is not None:
        updates.append("Descripcion = :Descripcion")
        parametros["Descripcion"] = Descripcion
    
    if not updates:
        print("❌ No hay campos para actualizar")
        return
    
    sql = f"UPDATE Libros SET {', '.join(updates)} WHERE id_libro = :id_libro"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Libro actualizado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def update_Prestamos(id_prestamo: int, cantidad: Optional[int] = None,
                     fecha_prestamo: Optional[str] = None, fecha_devolucion: Optional[str] = None):
    updates = []
    parametros = {"id_prestamo": id_prestamo}
    
    if cantidad is not None:
        updates.append("cantidad = :cantidad")
        parametros["cantidad"] = cantidad
    if fecha_prestamo is not None:
        updates.append("fecha_prestamo = :fecha_prestamo")
        parametros["fecha_prestamo"] = fecha_prestamo
    if fecha_devolucion is not None:
        updates.append("fecha_devolucion = :fecha_devolucion")
        parametros["fecha_devolucion"] = fecha_devolucion
    
    if not updates:
        print("❌ No hay campos para actualizar")
        return
    
    sql = f"UPDATE Prestamos SET {', '.join(updates)} WHERE Id_prestamo = :id_prestamo"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Préstamo actualizado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def update_DataSetsDescargados(id_Data_Set_Descargado: int, Nombre: Optional[str] = None, Cantidad: Optional[int] = None):
    updates = []
    parametros = {"id_Data_Set_Descargado": id_Data_Set_Descargado}
    
    if Nombre is not None:
        updates.append("Nombre = :Nombre")
        parametros["Nombre"] = Nombre
    if Cantidad is not None:
        updates.append("Cantidad = :Cantidad")
        parametros["Cantidad"] = Cantidad
    
    if not updates:
        print("❌ No hay campos para actualizar")
        return
    
    sql = f"UPDATE DataSetsDescargados SET {', '.join(updates)} WHERE id_Data_Set_Descargado = :id_Data_Set_Descargado"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Dataset actualizado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def update_MaterialExclusivo(id_material_exclusivo: int, nombre: Optional[str] = None, Descripcion: Optional[str] = None):
    updates = []
    parametros = {"id_material_exclusivo": id_material_exclusivo}
    
    if nombre is not None:
        updates.append("nombre = :nombre")
        parametros["nombre"] = nombre
    if Descripcion is not None:
        updates.append("Descripcion = :Descripcion")
        parametros["Descripcion"] = Descripcion
    
    if not updates:
        print("❌ No hay campos para actualizar")
        return
    
    sql = f"UPDATE MaterialExclusivo SET {', '.join(updates)} WHERE id_material_exclusivo = :id_material_exclusivo"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Material Exclusivo actualizado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def update_Biblioteca(id_biblioteca: int, CantidadMaterial: Optional[int] = None, GestionPrestamo: Optional[int] = None):
    updates = []
    parametros = {"id_biblioteca": id_biblioteca}
    
    if CantidadMaterial is not None:
        updates.append("CantidadMaterial = :CantidadMaterial")
        parametros["CantidadMaterial"] = CantidadMaterial
    if GestionPrestamo is not None:
        updates.append("GestionPrestamo = :GestionPrestamo")
        parametros["GestionPrestamo"] = GestionPrestamo
    
    if not updates:
        print("❌ No hay campos para actualizar")
        return
    
    sql = f"UPDATE Biblioteca SET {', '.join(updates)} WHERE id_biblioteca = :id_biblioteca"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, parametros)
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Biblioteca actualizada correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def delete_Usuario(id_usuario: int):
    sql = "DELETE FROM Usuarios WHERE id_usuario = :id_usuario"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_usuario": id_usuario})
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Usuario eliminado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def delete_Estudiante(id_estudiante: int):
    sql = "DELETE FROM Estudiantes WHERE id_estudiante = :id_estudiante"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_estudiante": id_estudiante})
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Estudiante eliminado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def delete_Docente(id_docente: int):
    sql = "DELETE FROM Docentes WHERE id_docente = :id_docente"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_docente": id_docente})
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Docente eliminado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def delete_Investigador(id_investigador: int):
    sql = "DELETE FROM Investigadores WHERE id_investigador = :id_investigador"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_investigador": id_investigador})
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Investigador eliminado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def delete_Libro(id_libro: int):
    sql = "DELETE FROM Libros WHERE id_libro = :id_libro"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_libro": id_libro})
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Libro eliminado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def delete_Prestamo(id_prestamo: int):
    sql = "DELETE FROM Prestamos WHERE Id_prestamo = :id_prestamo"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_prestamo": id_prestamo})
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Préstamo eliminado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def delete_Data_Set_Descargado(id_Data_Set_Descargado: int):
    sql = "DELETE FROM DataSetsDescargados WHERE id_Data_Set_Descargado = :id_Data_Set_Descargado"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_Data_Set_Descargado": id_Data_Set_Descargado})
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Dataset eliminado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def delete_Material_Exclusivo(id_material_exclusivo: int):
    sql = "DELETE FROM MaterialExclusivo WHERE id_material_exclusivo = :id_material_exclusivo"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, {"id_material_exclusivo": id_material_exclusivo})
        connection.commit()
        cursor.close()
        connection.close()
        print("✔️ Material Exclusivo eliminado correctamente")
    except oracledb.DatabaseError as e:
        print(f"Error en base de datos: {e}")

def menu_Usuarios():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE USUARIOS")
        print("="*50)
        print("1. Crear Usuario")
        print("2. Ver todos los Usuarios")
        print("3. Ver Usuario por ID")
        print("4. Actualizar Usuario")
        print("5. Eliminar Usuario")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_usuario = int(input("ID Usuario: "))
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                correo = input("Correo: ")
                create_Usuarios(id_usuario, nombre, apellido, correo)
                print("✔️ Usuario creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "2":
            usuarios = read_Usuarios()
            if usuarios:
                print("\n" + "-"*50)
                print(f"{'ID':<10} {'Nombre':<15} {'Apellido':<15} {'Correo':<15}")
                print("-"*50)
                for usuario in usuarios:
                    print(f"{usuario[0]:<10} {usuario[1]:<15} {usuario[2]:<15} {usuario[3]:<15}")
                print("-"*50)
            else:
                print("❌ No hay usuarios registrados")
        
        elif opcion == "3":
            try:
                id_usuario = int(input("ID Usuario a buscar: "))
                usuario = read_Usuarios_by_id(id_usuario)
                if usuario:
                    print(f"\nID: {usuario[0]}, Nombre: {usuario[1]}, Apellido: {usuario[2]}, Correo: {usuario[3]}")
                else:
                    print("❌ Usuario no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_usuario = int(input("ID Usuario a actualizar: "))
                print("Deja en blanco para no modificar un campo")
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                apellido = input("Nuevo Apellido (opcional): ").strip() or None
                correo = input("Nuevo Correo (opcional): ").strip() or None
                update_Usuarios(id_usuario, nombre, apellido, correo)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_usuario = int(input("ID Usuario a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Usuario(id_usuario)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Estudiantes():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE ESTUDIANTES")
        print("="*50)
        print("1. Crear Estudiante")
        print("2. Ver todos los Estudiantes")
        print("3. Ver Estudiante por ID")
        print("4. Actualizar Estudiante")
        print("5. Eliminar Estudiante")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_estudiante = int(input("ID Estudiante: "))
                id_usuario = int(input("ID Usuario: "))
                prestamos = int(input("Préstamos Activos: "))
                estado = input("Estado: ")
                create_Estudiantes(id_estudiante, id_usuario, prestamos, estado)
                print("✔️ Estudiante creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            estudiantes = read_Estudiantes()
            if estudiantes:
                print("\n" + "-"*70)
                print(f"{'ID':<10} {'ID Usuario':<12} {'Préstamos':<12} {'Estado':<20}")
                print("-"*70)
                for est in estudiantes:
                    print(f"{est[0]:<10} {est[1]:<12} {est[2]:<12} {est[3]:<20}")
                print("-"*70)
            else:
                print("❌ No hay estudiantes registrados")
        
        elif opcion == "3":
            try:
                id_estudiante = int(input("ID Estudiante a buscar: "))
                est = read_Estudiantes_by_id(id_estudiante)
                if est:
                    print(f"\nID: {est[0]}, ID Usuario: {est[1]}, Préstamos: {est[2]}, Estado: {est[3]}")
                else:
                    print("❌ Estudiante no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_estudiante = int(input("ID Estudiante a actualizar: "))
                prestamos = input("Nuevos Préstamos (opcional): ").strip()
                estado = input("Nuevo Estado (opcional): ").strip() or None
                update_Estudiantes(id_estudiante, int(prestamos) if prestamos else None, estado)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_estudiante = int(input("ID Estudiante a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Estudiante(id_estudiante)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Docentes():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE DOCENTES")
        print("="*50)
        print("1. Crear Docente")
        print("2. Ver todos los Docentes")
        print("3. Ver Docente por ID")
        print("4. Actualizar Docente")
        print("5. Eliminar Docente")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_docente = int(input("ID Docente: "))
                id_usuario = int(input("ID Usuario: "))
                create_Docentes(id_docente, id_usuario)
                print("✔️ Docente creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            docentes = read_Docentes()
            if docentes:
                print("\n" + "-"*40)
                print(f"{'ID Docente':<15} {'ID Usuario':<15}")
                print("-"*40)
                for doc in docentes:
                    print(f"{doc[0]:<15} {doc[1]:<15}")
                print("-"*40)
            else:
                print("❌ No hay docentes registrados")
        
        elif opcion == "3":
            try:
                id_docente = int(input("ID Docente a buscar: "))
                doc = read_Docentes_by_id(id_docente)
                if doc:
                    print(f"\nID Docente: {doc[0]}, ID Usuario: {doc[1]}")
                else:
                    print("❌ Docente no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_docente = int(input("ID Docente a actualizar: "))
                id_usuario = input("Nuevo ID Usuario (opcional): ").strip()
                update_Docentes(id_docente, int(id_usuario) if id_usuario else None)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_docente = int(input("ID Docente a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Docente(id_docente)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Investigadores():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE INVESTIGADORES")
        print("="*50)
        print("1. Crear Investigador")
        print("2. Ver todos los Investigadores")
        print("3. Ver Investigador por ID")
        print("4. Actualizar Investigador")
        print("5. Eliminar Investigador")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_investigador = int(input("ID Investigador: "))
                id_usuario = int(input("ID Usuario: "))
                nivel = input("Nivel de Acceso: ")
                create_Investigadores(id_investigador, id_usuario, nivel)
                print("✔️ Investigador creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            investigadores = read_Investigadores()
            if investigadores:
                print("\n" + "-"*60)
                print(f"{'ID Inv':<12} {'ID Usuario':<12} {'Nivel Acceso':<20}")
                print("-"*60)
                for inv in investigadores:
                    print(f"{inv[0]:<12} {inv[1]:<12} {inv[2]:<20}")
                print("-"*60)
            else:
                print("❌ No hay investigadores registrados")
        
        elif opcion == "3":
            try:
                id_investigador = int(input("ID Investigador a buscar: "))
                inv = read_Investigadores_by_id(id_investigador)
                if inv:
                    print(f"\nID: {inv[0]}, ID Usuario: {inv[1]}, Nivel: {inv[2]}")
                else:
                    print("❌ Investigador no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_investigador = int(input("ID Investigador a actualizar: "))
                nivel = input("Nuevo Nivel de Acceso (opcional): ").strip() or None
                update_Investigadores(id_investigador, nivel)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_investigador = int(input("ID Investigador a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Investigador(id_investigador)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Libros():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE LIBROS")
        print("="*50)
        print("1. Crear Libro")
        print("2. Ver todos los Libros")
        print("3. Ver Libro por ID")
        print("4. Actualizar Libro")
        print("5. Eliminar Libro")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_libro = int(input("ID Libro: "))
                id_estudiante = int(input("ID Estudiante: "))
                nombre = input("Nombre: ")
                autor = input("Autor: ")
                anio = int(input("Año Publicación: "))
                paginas = int(input("Cantidad Páginas: "))
                cantidad = int(input("Cantidad: "))
                descripcion = input("Descripción: ")
                create_Libros(id_libro, id_estudiante, nombre, autor, anio, paginas, cantidad, descripcion)
                print("✔️ Libro creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            libros = read_Libros()
            if libros:
                print("\n" + "-"*100)
                print(f"{'ID':<8} {'Nombre':<20} {'Autor':<15} {'Año':<6} {'Páginas':<10} {'Cantidad':<10}")
                print("-"*100)
                for libro in libros:
                    print(f"{libro[0]:<8} {libro[2]:<20} {libro[3]:<15} {libro[4]:<6} {libro[5]:<10} {libro[6]:<10}")
                print("-"*100)
            else:
                print("❌ No hay libros registrados")
        
        elif opcion == "3":
            try:
                id_libro = int(input("ID Libro a buscar: "))
                libro = read_Libros_by_id(id_libro)
                if libro:
                    print(f"\nID: {libro[0]}, Nombre: {libro[2]}, Autor: {libro[3]}, Año: {libro[4]}")
                else:
                    print("❌ Libro no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_libro = int(input("ID Libro a actualizar: "))
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                autor = input("Nuevo Autor (opcional): ").strip() or None
                cantidad = input("Nueva Cantidad (opcional): ").strip()
                update_Libros(id_libro, nombre, autor, Cantidad=int(cantidad) if cantidad else None)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_libro = int(input("ID Libro a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Libro(id_libro)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Prestamos():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE PRÉSTAMOS")
        print("="*50)
        print("1. Crear Préstamo")
        print("2. Ver todos los Préstamos")
        print("3. Ver Préstamo por ID")
        print("4. Actualizar Préstamo")
        print("5. Eliminar Préstamo")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_prestamo = int(input("ID Préstamo: "))
                id_estudiante = int(input("ID Estudiante: "))
                id_libro = int(input("ID Libro: "))
                cantidad = int(input("Cantidad: "))
                fecha_prestamo = input("Fecha Préstamo (YYYY-MM-DD): ")
                fecha_devolucion = input("Fecha Devolución (YYYY-MM-DD): ")
                create_Prestamos(id_prestamo, id_estudiante, id_libro, cantidad, fecha_prestamo, fecha_devolucion)
                print("✔️ Préstamo creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            prestamos = read_Prestamos()
            if prestamos:
                print("\n" + "-"*80)
                print(f"{'ID':<8} {'Estudiante':<12} {'Libro':<10} {'Cantidad':<10} {'Préstamo':<15}")
                print("-"*80)
                for prest in prestamos:
                    print(f"{prest[0]:<8} {prest[1]:<12} {prest[2]:<10} {prest[3]:<10} {prest[4]:<15}")
                print("-"*80)
            else:
                print("❌ No hay préstamos registrados")
        
        elif opcion == "3":
            try:
                id_prestamo = int(input("ID Préstamo a buscar: "))
                prest = read_Prestamos_by_id(id_prestamo)
                if prest:
                    print(f"\nID: {prest[0]}, Estudiante: {prest[1]}, Libro: {prest[2]}, Cantidad: {prest[3]}")
                else:
                    print("❌ Préstamo no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_prestamo = int(input("ID Préstamo a actualizar: "))
                cantidad = input("Nueva Cantidad (opcional): ").strip()
                fecha_prestamo = input("Nueva fecha de préstamo (YYYY-MM-DD): ").strip()
                fecha_devolucion = input("Nueva fecha de devolución (YYYY-MM-DD): ").strip()

                update_Prestamos(
                    id_prestamo,
                    int(cantidad) if cantidad else None,
                    fecha_prestamo if fecha_prestamo else None,
                    fecha_devolucion if fecha_devolucion else None
                )
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_prestamo = int(input("ID Préstamo a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Prestamo(id_prestamo)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_DataSetsDescargados():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE DATASETS DESCARGADOS")
        print("="*50)
        print("1. Crear Dataset")
        print("2. Ver todos los Datasets")
        print("3. Ver Dataset por ID")
        print("4. Actualizar Dataset")
        print("5. Eliminar Dataset")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_dataset = int(input("ID Dataset: "))
                id_investigador = int(input("ID Investigador: "))
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                create_DataSetsDescargados(id_dataset, id_investigador, nombre, cantidad)
                print("✔️ Dataset creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            datasets = read_DataSetsDescargados()
            if datasets:
                print("\n" + "-"*70)
                print(f"{'ID':<10} {'Investigador':<15} {'Nombre':<25} {'Cantidad':<10}")
                print("-"*70)
                for ds in datasets:
                    print(f"{ds[0]:<10} {ds[1]:<15} {ds[2]:<25} {ds[3]:<10}")
                print("-"*70)
            else:
                print("❌ No hay datasets registrados")
        
        elif opcion == "3":
            try:
                id_dataset = int(input("ID Dataset a buscar: "))
                ds = read_DataSetsDescargados_by_id(id_dataset)
                if ds:
                    print(f"\nID: {ds[0]}, Investigador: {ds[1]}, Nombre: {ds[2]}, Cantidad: {ds[3]}")
                else:
                    print("❌ Dataset no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_dataset = int(input("ID Dataset a actualizar: "))
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                cantidad = input("Nueva Cantidad (opcional): ").strip()
                update_DataSetsDescargados(id_dataset, nombre, int(cantidad) if cantidad else None)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_dataset = int(input("ID Dataset a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Data_Set_Descargado(id_dataset)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_MaterialExclusivo():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE MATERIAL EXCLUSIVO")
        print("="*50)
        print("1. Crear Material Exclusivo")
        print("2. Ver todos los Materiales")
        print("3. Ver Material por ID")
        print("4. Actualizar Material")
        print("5. Eliminar Material")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_material = int(input("ID Material: "))
                id_docente = int(input("ID Docente: "))
                nombre = input("Nombre: ")
                descripcion = input("Descripción: ")
                create_MaterialExclusivo(id_material, id_docente, nombre, descripcion)
                print("✔️ Material Exclusivo creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            materiales = read_MaterialExclusivo()
            if materiales:
                print("\n" + "-"*80)
                print(f"{'ID':<10} {'Docente':<10} {'Nombre':<25} {'Descripción':<25}")
                print("-"*80)
                for mat in materiales:
                    print(f"{mat[0]:<10} {mat[1]:<10} {mat[2]:<25} {mat[3]:<25}")
                print("-"*80)
            else:
                print("❌ No hay materiales registrados")
        
        elif opcion == "3":
            try:
                id_material = int(input("ID Material a buscar: "))
                mat = read_MaterialExclusivo_by_id(id_material)
                if mat:
                    print(f"\nID: {mat[0]}, Docente: {mat[1]}, Nombre: {mat[2]}, Descripción: {mat[3]}")
                else:
                    print("❌ Material no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_material = int(input("ID Material a actualizar: "))
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                descripcion = input("Nueva Descripción (opcional): ").strip() or None
                update_MaterialExclusivo(id_material, nombre, descripcion)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_material = int(input("ID Material a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Material_Exclusivo(id_material)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Biblioteca():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE BIBLIOTECA")
        print("="*50)
        print("1. Crear Biblioteca")
        print("2. Ver todos")
        print("3. Ver Biblioteca por ID")
        print("4. Actualizar Biblioteca")
        print("5. Eliminar Biblioteca")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_biblioteca = int(input("ID Biblioteca: "))
                cantidad = int(input("Cantidad Material: "))
                gestion = int(input("Gestión Préstamo: "))
                create_Biblioteca(id_biblioteca, cantidad, gestion)
                print("✔️ Biblioteca creada correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            bibliotecas = read_Biblioteca()
            if bibliotecas:
                print("\n" + "-"*60)
                print(f"{'ID':<10} {'Cantidad Material':<20} {'Gestión Préstamo':<20}")
                print("-"*60)
                for bib in bibliotecas:
                    print(f"{bib[0]:<10} {bib[1]:<20} {bib[2]:<20}")
                print("-"*60)
            else:
                print("❌ No hay bibliotecas registradas")
        
        elif opcion == "3":
            try:
                id_biblioteca = int(input("ID Biblioteca a buscar: "))
                bib = read_Biblioteca_by_id(id_biblioteca)
                if bib:
                    print(f"\nID: {bib[0]}, Cantidad: {bib[1]}, Gestión: {bib[2]}")
                else:
                    print("❌ Biblioteca no encontrada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_biblioteca = int(input("ID Biblioteca a actualizar: "))
                cantidad = input("Nueva Cantidad (opcional): ").strip()
                gestion = input("Nueva Gestión (opcional): ").strip()
                update_Biblioteca(id_biblioteca, int(cantidad) if cantidad else None, int(gestion) if gestion else None)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_biblioteca = int(input("ID Biblioteca a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    print("❌ No se pueden eliminar bibliotecas por restricciones")
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")


import os

def main():
    while True:
        print("\n" + "="*50)
        print("MENÚ PRINCIPAL - BIBLIOTECA")
        print("="*50)
        print("1. Crear/Reiniciar Base de Datos")
        print("2. Gestionar Usuarios")
        print("3. Gestionar Estudiantes")
        print("4. Gestionar Docentes")
        print("5. Gestionar Investigadores")
        print("6. Gestionar Libros")
        print("7. Gestionar Préstamos")
        print("8. Gestionar Datasets Descargados")
        print("9. Gestionar Material Exclusivo")
        print("10. Gestionar Biblioteca")
        print("0. Salir")
        print("="*50)
        
        opcion = input("Selecciona una opción [1-10, 0 para salir]: ").strip()
        
        if opcion == "1":
            try:
                print("⏳ Eliminando tablas antiguas...")
                drop_all_tables()
                print("⏳ Creando nuevas tablas...")
                create_all_tables()
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
            menu_MaterialExclusivo()
        elif opcion == "10":
            menu_Biblioteca()
        elif opcion == "0":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
            input("Presiona ENTER para continuar...")

def menu_Usuarios():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE USUARIOS")
        print("="*50)
        print("1. Crear Usuario")
        print("2. Ver todos los Usuarios")
        print("3. Ver Usuario por ID")
        print("4. Actualizar Usuario")
        print("5. Eliminar Usuario")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_usuario = int(input("ID Usuario: "))
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                correo = input("Correo: ")
                create_Usuarios(id_usuario, nombre, apellido, correo)
                print("✔️ Usuario creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "2":
            usuarios = read_Usuarios()
            if usuarios:
                print("\n" + "-"*50)
                print(f"{'ID':<10} {'Nombre':<15} {'Apellido':<15} {'Correo':<15}")
                print("-"*50)
                for usuario in usuarios:
                    print(f"{usuario[0]:<10} {usuario[1]:<15} {usuario[2]:<15} {usuario[3]:<15}")
                print("-"*50)
            else:
                print("❌ No hay usuarios registrados")
        
        elif opcion == "3":
            try:
                id_usuario = int(input("ID Usuario a buscar: "))
                usuario = read_Usuarios_by_id(id_usuario)
                if usuario:
                    print(f"\nID: {usuario[0]}, Nombre: {usuario[1]}, Apellido: {usuario[2]}, Correo: {usuario[3]}")
                else:
                    print("❌ Usuario no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_usuario = int(input("ID Usuario a actualizar: "))
                print("Deja en blanco para no modificar un campo")
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                apellido = input("Nuevo Apellido (opcional): ").strip() or None
                correo = input("Nuevo Correo (opcional): ").strip() or None
                update_Usuarios(id_usuario, nombre, apellido, correo)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_usuario = int(input("ID Usuario a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Usuario(id_usuario)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Estudiantes():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE ESTUDIANTES")
        print("="*50)
        print("1. Crear Estudiante")
        print("2. Ver todos los Estudiantes")
        print("3. Ver Estudiante por ID")
        print("4. Actualizar Estudiante")
        print("5. Eliminar Estudiante")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_estudiante = int(input("ID Estudiante: "))
                id_usuario = int(input("ID Usuario: "))
                prestamos = int(input("Préstamos Activos: "))
                estado = input("Estado: ")
                create_Estudiantes(id_estudiante, id_usuario, prestamos, estado)
                print("✔️ Estudiante creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            estudiantes = read_Estudiantes()
            if estudiantes:
                print("\n" + "-"*70)
                print(f"{'ID':<10} {'ID Usuario':<12} {'Préstamos':<12} {'Estado':<20}")
                print("-"*70)
                for est in estudiantes:
                    print(f"{est[0]:<10} {est[1]:<12} {est[2]:<12} {est[3]:<20}")
                print("-"*70)
            else:
                print("❌ No hay estudiantes registrados")
        
        elif opcion == "3":
            try:
                id_estudiante = int(input("ID Estudiante a buscar: "))
                est = read_Estudiantes_by_id(id_estudiante)
                if est:
                    print(f"\nID: {est[0]}, ID Usuario: {est[1]}, Préstamos: {est[2]}, Estado: {est[3]}")
                else:
                    print("❌ Estudiante no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_estudiante = int(input("ID Estudiante a actualizar: "))
                prestamos = input("Nuevos Préstamos (opcional): ").strip()
                estado = input("Nuevo Estado (opcional): ").strip() or None
                update_Estudiantes(id_estudiante, int(prestamos) if prestamos else None, estado)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_estudiante = int(input("ID Estudiante a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Estudiante(id_estudiante)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Docentes():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE DOCENTES")
        print("="*50)
        print("1. Crear Docente")
        print("2. Ver todos los Docentes")
        print("3. Ver Docente por ID")
        print("4. Actualizar Docente")
        print("5. Eliminar Docente")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_docente = int(input("ID Docente: "))
                id_usuario = int(input("ID Usuario: "))
                create_Docentes(id_docente, id_usuario)
                print("✔️ Docente creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            docentes = read_Docentes()
            if docentes:
                print("\n" + "-"*40)
                print(f"{'ID Docente':<15} {'ID Usuario':<15}")
                print("-"*40)
                for doc in docentes:
                    print(f"{doc[0]:<15} {doc[1]:<15}")
                print("-"*40)
            else:
                print("❌ No hay docentes registrados")
        
        elif opcion == "3":
            try:
                id_docente = int(input("ID Docente a buscar: "))
                doc = read_Docentes_by_id(id_docente)
                if doc:
                    print(f"\nID Docente: {doc[0]}, ID Usuario: {doc[1]}")
                else:
                    print("❌ Docente no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_docente = int(input("ID Docente a actualizar: "))
                id_usuario = input("Nuevo ID Usuario (opcional): ").strip()
                update_Docentes(id_docente, int(id_usuario) if id_usuario else None)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_docente = int(input("ID Docente a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Docente(id_docente)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Investigadores():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE INVESTIGADORES")
        print("="*50)
        print("1. Crear Investigador")
        print("2. Ver todos los Investigadores")
        print("3. Ver Investigador por ID")
        print("4. Actualizar Investigador")
        print("5. Eliminar Investigador")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_investigador = int(input("ID Investigador: "))
                id_usuario = int(input("ID Usuario: "))
                nivel = input("Nivel de Acceso: ")
                create_Investigadores(id_investigador, id_usuario, nivel)
                print("✔️ Investigador creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            investigadores = read_Investigadores()
            if investigadores:
                print("\n" + "-"*60)
                print(f"{'ID Inv':<12} {'ID Usuario':<12} {'Nivel Acceso':<20}")
                print("-"*60)
                for inv in investigadores:
                    print(f"{inv[0]:<12} {inv[1]:<12} {inv[2]:<20}")
                print("-"*60)
            else:
                print("❌ No hay investigadores registrados")
        
        elif opcion == "3":
            try:
                id_investigador = int(input("ID Investigador a buscar: "))
                inv = read_Investigadores_by_id(id_investigador)
                if inv:
                    print(f"\nID: {inv[0]}, ID Usuario: {inv[1]}, Nivel: {inv[2]}")
                else:
                    print("❌ Investigador no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_investigador = int(input("ID Investigador a actualizar: "))
                nivel = input("Nuevo Nivel de Acceso (opcional): ").strip() or None
                update_Investigadores(id_investigador, nivel)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_investigador = int(input("ID Investigador a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Investigador(id_investigador)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Libros():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE LIBROS")
        print("="*50)
        print("1. Crear Libro")
        print("2. Ver todos los Libros")
        print("3. Ver Libro por ID")
        print("4. Actualizar Libro")
        print("5. Eliminar Libro")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_libro = int(input("ID Libro: "))
                id_estudiante = int(input("ID Estudiante: "))
                nombre = input("Nombre: ")
                autor = input("Autor: ")
                anio = int(input("Año Publicación: "))
                paginas = int(input("Cantidad Páginas: "))
                cantidad = int(input("Cantidad: "))
                descripcion = input("Descripción: ")
                create_Libros(id_libro, id_estudiante, nombre, autor, anio, paginas, cantidad, descripcion)
                print("✔️ Libro creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            libros = read_Libros()
            if libros:
                print("\n" + "-"*100)
                print(f"{'ID':<8} {'Nombre':<20} {'Autor':<15} {'Año':<6} {'Páginas':<10} {'Cantidad':<10}")
                print("-"*100)
                for libro in libros:
                    print(f"{libro[0]:<8} {libro[2]:<20} {libro[3]:<15} {libro[4]:<6} {libro[5]:<10} {libro[6]:<10}")
                print("-"*100)
            else:
                print("❌ No hay libros registrados")
        
        elif opcion == "3":
            try:
                id_libro = int(input("ID Libro a buscar: "))
                libro = read_Libros_by_id(id_libro)
                if libro:
                    print(f"\nID: {libro[0]}, Nombre: {libro[2]}, Autor: {libro[3]}, Año: {libro[4]}")
                else:
                    print("❌ Libro no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_libro = int(input("ID Libro a actualizar: "))
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                autor = input("Nuevo Autor (opcional): ").strip() or None
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

        elif opcion == "5":
            try:
                id_libro = int(input("ID Libro a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Libro(id_libro)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")



import os

def menu_Prestamos():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE PRÉSTAMOS")
        print("="*50)
        print("1. Crear Préstamo")
        print("2. Ver todos los Préstamos")
        print("3. Ver Préstamo por ID")
        print("4. Actualizar Préstamo")
        print("5. Eliminar Préstamo")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_prestamo = int(input("ID Préstamo: "))
                id_estudiante = int(input("ID Estudiante: "))
                id_libro = int(input("ID Libro: "))
                cantidad = int(input("Cantidad: "))
                fecha_prestamo = input("Fecha Préstamo (YYYY-MM-DD): ")
                fecha_devolucion = input("Fecha Devolución (YYYY-MM-DD): ")
                create_Prestamos(id_prestamo, id_estudiante, id_libro, cantidad, fecha_prestamo, fecha_devolucion)
                print("✔️ Préstamo creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            prestamos = read_Prestamos()
            if prestamos:
                print("\n" + "-"*80)
                print(f"{'ID':<8} {'Estudiante':<12} {'Libro':<10} {'Cantidad':<10} {'Préstamo':<15}")
                print("-"*80)
                for prest in prestamos:
                    print(f"{prest[0]:<8} {prest[1]:<12} {prest[2]:<10} {prest[3]:<10} {prest[4]:<15}")
                print("-"*80)
            else:
                print("❌ No hay préstamos registrados")
        
        elif opcion == "3":
            try:
                id_prestamo = int(input("ID Préstamo a buscar: "))
                prest = read_Prestamos_by_id(id_prestamo)
                if prest:
                    print(f"\nID: {prest[0]}, Estudiante: {prest[1]}, Libro: {prest[2]}, Cantidad: {prest[3]}")
                else:
                    print("❌ Préstamo no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_prestamo = int(input("ID Préstamo a actualizar: "))
                cantidad = input("Nueva Cantidad (opcional): ").strip()
                fecha_prestamo = input("Nueva fecha de préstamo (YYYY-MM-DD): ").strip()
                fecha_devolucion = input("Nueva fecha de devolución (YYYY-MM-DD): ").strip()

                update_Prestamos(
                    id_prestamo,
                    int(cantidad) if cantidad else None,
                    fecha_prestamo if fecha_prestamo else None,
                    fecha_devolucion if fecha_devolucion else None
                )
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_prestamo = int(input("ID Préstamo a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Prestamo(id_prestamo)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_DataSetsDescargados():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE DATASETS DESCARGADOS")
        print("="*50)
        print("1. Crear Dataset")
        print("2. Ver todos los Datasets")
        print("3. Ver Dataset por ID")
        print("4. Actualizar Dataset")
        print("5. Eliminar Dataset")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_dataset = int(input("ID Dataset: "))
                id_investigador = int(input("ID Investigador: "))
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                create_DataSetsDescargados(id_dataset, id_investigador, nombre, cantidad)
                print("✔️ Dataset creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            datasets = read_DataSetsDescargados()
            if datasets:
                print("\n" + "-"*70)
                print(f"{'ID':<10} {'Investigador':<15} {'Nombre':<25} {'Cantidad':<10}")
                print("-"*70)
                for ds in datasets:
                    print(f"{ds[0]:<10} {ds[1]:<15} {ds[2]:<25} {ds[3]:<10}")
                print("-"*70)
            else:
                print("❌ No hay datasets registrados")
        
        elif opcion == "3":
            try:
                id_dataset = int(input("ID Dataset a buscar: "))
                ds = read_DataSetsDescargados_by_id(id_dataset)
                if ds:
                    print(f"\nID: {ds[0]}, Investigador: {ds[1]}, Nombre: {ds[2]}, Cantidad: {ds[3]}")
                else:
                    print("❌ Dataset no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_dataset = int(input("ID Dataset a actualizar: "))
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                cantidad = input("Nueva Cantidad (opcional): ").strip()
                update_DataSetsDescargados(id_dataset, nombre, int(cantidad) if cantidad else None)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_dataset = int(input("ID Dataset a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Data_Set_Descargado(id_dataset)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")


def menu_MaterialExclusivo():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE MATERIAL EXCLUSIVO")
        print("="*50)
        print("1. Crear Material Exclusivo")
        print("2. Ver todos los Materiales")
        print("3. Ver Material por ID")
        print("4. Actualizar Material")
        print("5. Eliminar Material")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_material = int(input("ID Material: "))
                id_docente = int(input("ID Docente: "))
                nombre = input("Nombre: ")
                descripcion = input("Descripción: ")
                create_MaterialExclusivo(id_material, id_docente, nombre, descripcion)
                print("✔️ Material Exclusivo creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            materiales = read_MaterialExclusivo()
            if materiales:
                print("\n" + "-"*80)
                print(f"{'ID':<10} {'Docente':<10} {'Nombre':<25} {'Descripción':<25}")
                print("-"*80)
                for mat in materiales:
                    print(f"{mat[0]:<10} {mat[1]:<10} {mat[2]:<25} {mat[3]:<25}")
                print("-"*80)
            else:
                print("❌ No hay materiales registrados")
        
        elif opcion == "3":
            try:
                id_material = int(input("ID Material a buscar: "))
                mat = read_MaterialExclusivo_by_id(id_material)
                if mat:
                    print(f"\nID: {mat[0]}, Docente: {mat[1]}, Nombre: {mat[2]}, Descripción: {mat[3]}")
                else:
                    print("❌ Material no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_material = int(input("ID Material a actualizar: "))
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                descripcion = input("Nueva Descripción (opcional): ").strip() or None
                update_MaterialExclusivo(id_material, nombre, descripcion)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_material = int(input("ID Material a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Material_Exclusivo(id_material)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")


def menu_Biblioteca():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE BIBLIOTECA")
        print("="*50)
        print("1. Crear Biblioteca")
        print("2. Ver todos")
        print("3. Ver Biblioteca por ID")
        print("4. Actualizar Biblioteca")
        print("5. Eliminar Biblioteca")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_biblioteca = int(input("ID Biblioteca: "))
                cantidad = int(input("Cantidad Material: "))
                gestion = int(input("Gestión Préstamo: "))
                create_Biblioteca(id_biblioteca, cantidad, gestion)
                print("✔️ Biblioteca creada correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            bibliotecas = read_Biblioteca()
            if bibliotecas:
                print("\n" + "-"*60)
                print(f"{'ID':<10} {'Cantidad Material':<20} {'Gestión Préstamo':<20}")
                print("-"*60)
                for bib in bibliotecas:
                    print(f"{bib[0]:<10} {bib[1]:<20} {bib[2]:<20}")
                print("-"*60)
            else:
                print("❌ No hay bibliotecas registradas")
        
        elif opcion == "3":
            try:
                id_biblioteca = int(input("ID Biblioteca a buscar: "))
                bib = read_Biblioteca_by_id(id_biblioteca)
                if bib:
                    print(f"\nID: {bib[0]}, Cantidad: {bib[1]}, Gestión: {bib[2]}")
                else:
                    print("❌ Biblioteca no encontrada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_biblioteca = int(input("ID Biblioteca a actualizar: "))
                cantidad = input("Nueva Cantidad (opcional): ").strip()
                gestion = input("Nueva Gestión (opcional): ").strip()
                update_Biblioteca(id_biblioteca, int(cantidad) if cantidad else None, int(gestion) if gestion else None)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_biblioteca = int(input("ID Biblioteca a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    print("❌ No se pueden eliminar bibliotecas por restricciones")
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")


import os

def main():
    while True:
        print("\n" + "="*50)
        print("MENÚ PRINCIPAL - BIBLIOTECA")
        print("="*50)
        print("1. Crear/Reiniciar Base de Datos")
        print("2. Gestionar Usuarios")
        print("3. Gestionar Estudiantes")
        print("4. Gestionar Docentes")
        print("5. Gestionar Investigadores")
        print("6. Gestionar Libros")
        print("7. Gestionar Préstamos")
        print("8. Gestionar Datasets Descargados")
        print("9. Gestionar Material Exclusivo")
        print("10. Gestionar Biblioteca")
        print("0. Salir")
        print("="*50)
        
        opcion = input("Selecciona una opción [1-10, 0 para salir]: ").strip()
        
        if opcion == "1":
            try:
                print("⏳ Eliminando tablas antiguas...")
                drop_all_tables()
                print("⏳ Creando nuevas tablas...")
                create_all_tables()
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
            menu_MaterialExclusivo()
        elif opcion == "10":
            menu_Biblioteca()
        elif opcion == "0":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
            input("Presiona ENTER para continuar...")

def menu_Usuarios():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE USUARIOS")
        print("="*50)
        print("1. Crear Usuario")
        print("2. Ver todos los Usuarios")
        print("3. Ver Usuario por ID")
        print("4. Actualizar Usuario")
        print("5. Eliminar Usuario")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_usuario = int(input("ID Usuario: "))
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                correo = input("Correo: ")
                create_Usuarios(id_usuario, nombre, apellido, correo)
                print("✔️ Usuario creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "2":
            usuarios = read_Usuarios()
            if usuarios:
                print("\n" + "-"*50)
                print(f"{'ID':<10} {'Nombre':<15} {'Apellido':<15} {'Correo':<15}")
                print("-"*50)
                for usuario in usuarios:
                    print(f"{usuario[0]:<10} {usuario[1]:<15} {usuario[2]:<15} {usuario[3]:<15}")
                print("-"*50)
            else:
                print("❌ No hay usuarios registrados")
        
        elif opcion == "3":
            try:
                id_usuario = int(input("ID Usuario a buscar: "))
                usuario = read_Usuarios_by_id(id_usuario)
                if usuario:
                    print(f"\nID: {usuario[0]}, Nombre: {usuario[1]}, Apellido: {usuario[2]}, Correo: {usuario[3]}")
                else:
                    print("❌ Usuario no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_usuario = int(input("ID Usuario a actualizar: "))
                print("Deja en blanco para no modificar un campo")
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                apellido = input("Nuevo Apellido (opcional): ").strip() or None
                correo = input("Nuevo Correo (opcional): ").strip() or None
                update_Usuarios(id_usuario, nombre, apellido, correo)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_usuario = int(input("ID Usuario a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Usuario(id_usuario)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Estudiantes():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE ESTUDIANTES")
        print("="*50)
        print("1. Crear Estudiante")
        print("2. Ver todos los Estudiantes")
        print("3. Ver Estudiante por ID")
        print("4. Actualizar Estudiante")
        print("5. Eliminar Estudiante")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_estudiante = int(input("ID Estudiante: "))
                id_usuario = int(input("ID Usuario: "))
                prestamos = int(input("Préstamos Activos: "))
                estado = input("Estado: ")
                create_Estudiantes(id_estudiante, id_usuario, prestamos, estado)
                print("✔️ Estudiante creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            estudiantes = read_Estudiantes()
            if estudiantes:
                print("\n" + "-"*70)
                print(f"{'ID':<10} {'ID Usuario':<12} {'Préstamos':<12} {'Estado':<20}")
                print("-"*70)
                for est in estudiantes:
                    print(f"{est[0]:<10} {est[1]:<12} {est[2]:<12} {est[3]:<20}")
                print("-"*70)
            else:
                print("❌ No hay estudiantes registrados")
        
        elif opcion == "3":
            try:
                id_estudiante = int(input("ID Estudiante a buscar: "))
                est = read_Estudiantes_by_id(id_estudiante)
                if est:
                    print(f"\nID: {est[0]}, ID Usuario: {est[1]}, Préstamos: {est[2]}, Estado: {est[3]}")
                else:
                    print("❌ Estudiante no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_estudiante = int(input("ID Estudiante a actualizar: "))
                prestamos = input("Nuevos Préstamos (opcional): ").strip()
                estado = input("Nuevo Estado (opcional): ").strip() or None
                update_Estudiantes(id_estudiante, int(prestamos) if prestamos else None, estado)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_estudiante = int(input("ID Estudiante a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Estudiante(id_estudiante)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Docentes():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE DOCENTES")
        print("="*50)
        print("1. Crear Docente")
        print("2. Ver todos los Docentes")
        print("3. Ver Docente por ID")
        print("4. Actualizar Docente")
        print("5. Eliminar Docente")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_docente = int(input("ID Docente: "))
                id_usuario = int(input("ID Usuario: "))
                create_Docentes(id_docente, id_usuario)
                print("✔️ Docente creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            docentes = read_Docentes()
            if docentes:
                print("\n" + "-"*40)
                print(f"{'ID Docente':<15} {'ID Usuario':<15}")
                print("-"*40)
                for doc in docentes:
                    print(f"{doc[0]:<15} {doc[1]:<15}")
                print("-"*40)
            else:
                print("❌ No hay docentes registrados")
        
        elif opcion == "3":
            try:
                id_docente = int(input("ID Docente a buscar: "))
                doc = read_Docentes_by_id(id_docente)
                if doc:
                    print(f"\nID Docente: {doc[0]}, ID Usuario: {doc[1]}")
                else:
                    print("❌ Docente no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_docente = int(input("ID Docente a actualizar: "))
                id_usuario = input("Nuevo ID Usuario (opcional): ").strip()
                update_Docentes(id_docente, int(id_usuario) if id_usuario else None)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_docente = int(input("ID Docente a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Docente(id_docente)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_Investigadores():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE INVESTIGADORES")
        print("="*50)
        print("1. Crear Investigador")
        print("2. Ver todos los Investigadores")
        print("3. Ver Investigador por ID")
        print("4. Actualizar Investigador")
        print("5. Eliminar Investigador")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_investigador = int(input("ID Investigador: "))
                id_usuario = int(input("ID Usuario: "))
                nivel = input("Nivel de Acceso: ")
                create_Investigadores(id_investigador, id_usuario, nivel)
                print("✔️ Investigador creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            investigadores = read_Investigadores()
            if investigadores:
                print("\n" + "-"*60)
                print(f"{'ID Inv':<12} {'ID Usuario':<12} {'Nivel Acceso':<20}")
                print("-"*60)
                for inv in investigadores:
                    print(f"{inv[0]:<12} {inv[1]:<12} {inv[2]:<20}")
                print("-"*60)
            else:
                print("❌ No hay investigadores registrados")
        
        elif opcion == "3":
            try:
                id_investigador = int(input("ID Investigador a buscar: "))
                inv = read_Investigadores_by_id(id_investigador)
                if inv:
                    print(f"\nID: {inv[0]}, ID Usuario: {inv[1]}, Nivel: {inv[2]}")
                else:
                    print("❌ Investigador no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_investigador = int(input("ID Investigador a actualizar: "))
                nivel = input("Nuevo Nivel de Acceso (opcional): ").strip() or None
                update_Investigadores(id_investigador, nivel)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_investigador = int(input("ID Investigador a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Investigador(id_investigador)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")


def menu_Libros():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE LIBROS")
        print("="*50)
        print("1. Crear Libro")
        print("2. Ver todos los Libros")
        print("3. Ver Libro por ID")
        print("4. Actualizar Libro")
        print("5. Eliminar Libro")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_libro = int(input("ID Libro: "))
                id_estudiante = int(input("ID Estudiante: "))
                nombre = input("Nombre: ")
                autor = input("Autor: ")
                anio = int(input("Año Publicación: "))
                paginas = int(input("Cantidad Páginas: "))
                cantidad = int(input("Cantidad: "))
                descripcion = input("Descripción: ")
                create_Libros(id_libro, id_estudiante, nombre, autor, anio, paginas, cantidad, descripcion)
                print("✔️ Libro creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            libros = read_Libros()
            if libros:
                print("\n" + "-"*100)
                print(f"{'ID':<8} {'Nombre':<20} {'Autor':<15} {'Año':<6} {'Páginas':<10} {'Cantidad':<10}")
                print("-"*100)
                for libro in libros:
                    print(f"{libro[0]:<8} {libro[2]:<20} {libro[3]:<15} {libro[4]:<6} {libro[5]:<10} {libro[6]:<10}")
                print("-"*100)
            else:
                print("❌ No hay libros registrados")
        
        elif opcion == "3":
            try:
                id_libro = int(input("ID Libro a buscar: "))
                libro = read_Libros_by_id(id_libro)
                if libro:
                    print(f"\nID: {libro[0]}, Nombre: {libro[2]}, Autor: {libro[3]}, Año: {libro[4]}")
                else:
                    print("❌ Libro no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_libro = int(input("ID Libro a actualizar: "))
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                autor = input("Nuevo Autor (opcional): ").strip() or None
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

        elif opcion == "5":
            try:
                id_libro = int(input("ID Libro a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Libro(id_libro)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")



import os

def menu_Prestamos():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE PRÉSTAMOS")
        print("="*50)
        print("1. Crear Préstamo")
        print("2. Ver todos los Préstamos")
        print("3. Ver Préstamo por ID")
        print("4. Actualizar Préstamo")
        print("5. Eliminar Préstamo")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_prestamo = int(input("ID Préstamo: "))
                id_estudiante = int(input("ID Estudiante: "))
                id_libro = int(input("ID Libro: "))
                cantidad = int(input("Cantidad: "))
                fecha_prestamo = input("Fecha Préstamo (YYYY-MM-DD): ")
                fecha_devolucion = input("Fecha Devolución (YYYY-MM-DD): ")
                create_Prestamos(id_prestamo, id_estudiante, id_libro, cantidad, fecha_prestamo, fecha_devolucion)
                print("✔️ Préstamo creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            prestamos = read_Prestamos()
            if prestamos:
                print("\n" + "-"*80)
                print(f"{'ID':<8} {'Estudiante':<12} {'Libro':<10} {'Cantidad':<10} {'Préstamo':<15}")
                print("-"*80)
                for prest in prestamos:
                    print(f"{prest[0]:<8} {prest[1]:<12} {prest[2]:<10} {prest[3]:<10} {prest[4]:<15}")
                print("-"*80)
            else:
                print("❌ No hay préstamos registrados")
        
        elif opcion == "3":
            try:
                id_prestamo = int(input("ID Préstamo a buscar: "))
                prest = read_Prestamos_by_id(id_prestamo)
                if prest:
                    print(f"\nID: {prest[0]}, Estudiante: {prest[1]}, Libro: {prest[2]}, Cantidad: {prest[3]}")
                else:
                    print("❌ Préstamo no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_prestamo = int(input("ID Préstamo a actualizar: "))
                cantidad = input("Nueva Cantidad (opcional): ").strip()
                fecha_prestamo = input("Nueva fecha de préstamo (YYYY-MM-DD): ").strip()
                fecha_devolucion = input("Nueva fecha de devolución (YYYY-MM-DD): ").strip()

                update_Prestamos(
                    id_prestamo,
                    int(cantidad) if cantidad else None,
                    fecha_prestamo if fecha_prestamo else None,
                    fecha_devolucion if fecha_devolucion else None
                )
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_prestamo = int(input("ID Préstamo a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Prestamo(id_prestamo)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")

def menu_DataSetsDescargados():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE DATASETS DESCARGADOS")
        print("="*50)
        print("1. Crear Dataset")
        print("2. Ver todos los Datasets")
        print("3. Ver Dataset por ID")
        print("4. Actualizar Dataset")
        print("5. Eliminar Dataset")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_dataset = int(input("ID Dataset: "))
                id_investigador = int(input("ID Investigador: "))
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                create_DataSetsDescargados(id_dataset, id_investigador, nombre, cantidad)
                print("✔️ Dataset creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            datasets = read_DataSetsDescargados()
            if datasets:
                print("\n" + "-"*70)
                print(f"{'ID':<10} {'Investigador':<15} {'Nombre':<25} {'Cantidad':<10}")
                print("-"*70)
                for ds in datasets:
                    print(f"{ds[0]:<10} {ds[1]:<15} {ds[2]:<25} {ds[3]:<10}")
                print("-"*70)
            else:
                print("❌ No hay datasets registrados")
        
        elif opcion == "3":
            try:
                id_dataset = int(input("ID Dataset a buscar: "))
                ds = read_DataSetsDescargados_by_id(id_dataset)
                if ds:
                    print(f"\nID: {ds[0]}, Investigador: {ds[1]}, Nombre: {ds[2]}, Cantidad: {ds[3]}")
                else:
                    print("❌ Dataset no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_dataset = int(input("ID Dataset a actualizar: "))
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                cantidad = input("Nueva Cantidad (opcional): ").strip()
                update_DataSetsDescargados(id_dataset, nombre, int(cantidad) if cantidad else None)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_dataset = int(input("ID Dataset a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Data_Set_Descargado(id_dataset)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")


import os

def menu_MaterialExclusivo():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE MATERIAL EXCLUSIVO")
        print("="*50)
        print("1. Crear Material Exclusivo")
        print("2. Ver todos los Materiales")
        print("3. Ver Material por ID")
        print("4. Actualizar Material")
        print("5. Eliminar Material")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_material = int(input("ID Material: "))
                id_docente = int(input("ID Docente: "))
                nombre = input("Nombre: ")
                descripcion = input("Descripción: ")
                create_MaterialExclusivo(id_material, id_docente, nombre, descripcion)
                print("✔️ Material Exclusivo creado correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            materiales = read_MaterialExclusivo()
            if materiales:
                print("\n" + "-"*80)
                print(f"{'ID':<10} {'Docente':<10} {'Nombre':<25} {'Descripción':<25}")
                print("-"*80)
                for mat in materiales:
                    print(f"{mat[0]:<10} {mat[1]:<10} {mat[2]:<25} {mat[3]:<25}")
                print("-"*80)
            else:
                print("❌ No hay materiales registrados")
        
        elif opcion == "3":
            try:
                id_material = int(input("ID Material a buscar: "))
                mat = read_MaterialExclusivo_by_id(id_material)
                if mat:
                    print(f"\nID: {mat[0]}, Docente: {mat[1]}, Nombre: {mat[2]}, Descripción: {mat[3]}")
                else:
                    print("❌ Material no encontrado")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_material = int(input("ID Material a actualizar: "))
                nombre = input("Nuevo Nombre (opcional): ").strip() or None
                descripcion = input("Nueva Descripción (opcional): ").strip() or None
                update_MaterialExclusivo(id_material, nombre, descripcion)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_material = int(input("ID Material a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    delete_Material_Exclusivo(id_material)
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")


def menu_Biblioteca():
    while True:
        print("\n" + "="*50)
        print("GESTIÓN DE BIBLIOTECA")
        print("="*50)
        print("1. Crear Biblioteca")
        print("2. Ver todos")
        print("3. Ver Biblioteca por ID")
        print("4. Actualizar Biblioteca")
        print("5. Eliminar Biblioteca")
        print("0. Volver al menú principal")
        print("="*50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_biblioteca = int(input("ID Biblioteca: "))
                cantidad = int(input("Cantidad Material: "))
                gestion = int(input("Gestión Préstamo: "))
                create_Biblioteca(id_biblioteca, cantidad, gestion)
                print("✔️ Biblioteca creada correctamente")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "2":
            bibliotecas = read_Biblioteca()
            if bibliotecas:
                print("\n" + "-"*60)
                print(f"{'ID':<10} {'Cantidad Material':<20} {'Gestión Préstamo':<20}")
                print("-"*60)
                for bib in bibliotecas:
                    print(f"{bib[0]:<10} {bib[1]:<20} {bib[2]:<20}")
                print("-"*60)
            else:
                print("❌ No hay bibliotecas registradas")
        
        elif opcion == "3":
            try:
                id_biblioteca = int(input("ID Biblioteca a buscar: "))
                bib = read_Biblioteca_by_id(id_biblioteca)
                if bib:
                    print(f"\nID: {bib[0]}, Cantidad: {bib[1]}, Gestión: {bib[2]}")
                else:
                    print("❌ Biblioteca no encontrada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "4":
            try:
                id_biblioteca = int(input("ID Biblioteca a actualizar: "))
                cantidad = input("Nueva Cantidad (opcional): ").strip()
                gestion = input("Nueva Gestión (opcional): ").strip()
                update_Biblioteca(id_biblioteca, int(cantidad) if cantidad else None, int(gestion) if gestion else None)
            except ValueError:
                print("❌ Entrada inválida")
        
        elif opcion == "5":
            try:
                id_biblioteca = int(input("ID Biblioteca a eliminar: "))
                confirmacion = input("¿Estás seguro? (s/n): ").lower()
                if confirmacion == "s":
                    print("❌ No se pueden eliminar bibliotecas por restricciones")
                else:
                    print("❌ Operación cancelada")
            except ValueError:
                print("❌ ID inválido")
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida")
        
        input("Presiona ENTER para continuar...")


import os

def main():
    while True:
        print("\n" + "="*50)
        print("MENÚ PRINCIPAL - BIBLIOTECA")
        print("="*50)
        print("1. Crear/Reiniciar Base de Datos")
        print("2. Gestionar Usuarios")
        print("3. Gestionar Estudiantes")
        print("4. Gestionar Docentes")
        print("5. Gestionar Investigadores")
        print("6. Gestionar Libros")
        print("7. Gestionar Préstamos")
        print("8. Gestionar Datasets Descargados")
        print("9. Gestionar Material Exclusivo")
        print("10. Gestionar Biblioteca")
        print("0. Salir")
        print("="*50)
        
        opcion = input("Selecciona una opción [1-10, 0 para salir]: ").strip()
        
        if opcion == "1":
            try:
                print("⏳ Eliminando tablas antiguas...")
                drop_all_tables()
                print("⏳ Creando nuevas tablas...")
                create_all_tables()
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
            menu_MaterialExclusivo()
        elif opcion == "10":
            menu_Biblioteca()
        elif opcion == "0":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
            input("Presiona ENTER para continuar...")

if __name__ == "__main__":
    main()