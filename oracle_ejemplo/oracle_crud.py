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
        "Libros ("
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
        "Prestamos("
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
        "Biblioteca ("
        "id_Biblioteca INTEGER PRIMARY KEY,"
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
        "INSERT INTO Usuarios (id_usuario, nombres, apellidos, rut, correo) "
        "VALUES (:id_usuario, :nombres, :apellidos, :rut, :correo)"
    )
    parametros = {
        "id_usuario": id_usuario,
        "nombres": nombres,
        "apellidos": apellidos,
        "rut": rut,
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
        print(f"Error al insertar datos: {e}")

 
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
        print(f"Error al insertar datos: {e}")


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
        print(f"Error al insertar datos: {e}")
    

def create_Investigadores(
        id_investigador: int,
        NivelAcceso: str
):
    sql = (
        "INSERT INTO Investigadores (id_investigador, NivelAcceso) "
        "VALUES (:id_investigador, :NivelAcceso)"
    )
    parametros = {
        "id_investigador": id_investigador,
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
        err = e
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
        err = e
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
        err = e
        print(f"Error al insertar datos: {e}")
    

def create_Biblioteca(
        id_Biblioteca: int,
        CantidadMaterial: int,
        GestionPrestamo: int
):
    sql = (
        "INSERT INTO Biblioteca (id_Biblioteca, CantidadMaterial, GestionPrestamo) "
        "VALUES (:id_Biblioteca, :CantidadMaterial, :GestionPrestamo)"
    )
    parametros = {
        "id_Biblioteca": id_Biblioteca,
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
        print(f"Error al insertar datos: {e}")
    


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
        parametros["anio_publicacion"] = datetime.strptime(anio_publicacion, "%Y-%m-%d") 
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
    

def update_Biblioteca(id_Biblioteca: int,CantidadMaterial: Optional[int] = None,GestionPrestamo: Optional[int] = None):
    modificaciones = []     
    parametros = {"id": id_Biblioteca}
    if CantidadMaterial is not None:         
        modificaciones.append("CantidadMaterial =: CantidadMaterial")         
        parametros["CantidadMaterial"] = CantidadMaterial
    if GestionPrestamo is not None:         
        modificaciones.append("GestionPrestamo =: GestionPrestamo")         
        parametros["GestionPrestamo"] = GestionPrestamo
    if not modificaciones:         
        print("No hay campos para actualizar.")         
        return

    sql = "UPDATE Biblioteca SET " + ", ".join(modificaciones) + " WHERE id_Biblioteca =: id"


