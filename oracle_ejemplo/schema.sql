CREATE TABLE Usuarios(
    id_usuario INTEGER PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL,
    apellido VARCHAR2(50) NOT NULL,
    Rut VARCHAR2(12) UNIQUE NOT NULL,
    correo VARCHAR2(50) UNIQUE NOT NULL
);


CREATE TABLE Estudiantes(
    id_estudiante INTEGER PRIMARY KEY,
    id_usuario INTEGER,
    PrestamosActivos INTEGER NOT NULL,
    EstadoDeuda VARCHAR2(50) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);


CREATE TABLE Docentes(
    id_docente INTEGER PRIMARY KEY,
    id_usuario INTEGER,
    MaterialExclusivoAccedido VARCHAR2(50) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);


CREATE TABLE Investigadores(
    id_investigador INTEGER PRIMARY KEY,
    NivelAcceso VARCHAR2(50) NOT NULL
);


CREATE TABLE Libro(
    id_libro INTEGER PRIMARY KEY,
    id_estudiante INTEGER,
    nombre VARCHAR2(50),
    autor VARCHAR2(50),
    anio_publicacion NUMBER(4),
    CantidadPaginas INTEGER,
    Cantidad INTEGER,
    Descripcion VARCHAR2(100),
    FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante)
);


CREATE TABLE Prestamos(
    Id_prestamo INTEGER PRIMARY KEY,
    id_estudiante INTEGER NOT NULL,
    Id_libro INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha_prestamo DATE,
    fecha_devolucion DATE,
    FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante),
    FOREIGN KEY (Id_libro) REFERENCES Libro(id_libro)
);


CREATE TABLE DataSetsDescargados(
    id_Data_Set_Descargado INTEGER PRIMARY KEY,
    id_investigador INTEGER NOT NULL,
    Nombre VARCHAR2(50) NOT NULL,
    Cantidad INTEGER NOT NULL,
    FOREIGN KEY (id_investigador) REFERENCES Investigadores(id_investigador)
);


CREATE TABLE Biblioteca(
    id_Biblioteca INTEGER PRIMARY KEY,
    CantidadMaterial INTEGER NOT NULL,
    GestionPrestamo INTEGER NOT NULL
);

