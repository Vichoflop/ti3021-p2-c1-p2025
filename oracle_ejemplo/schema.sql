CREATE TABLE Usuarios (
    id_usuario        INTEGER PRIMARY KEY,
    nombre            VARCHAR2(100) NOT NULL,
    apellido          VARCHAR2(100) NOT NULL,
    correo            VARCHAR2(120) UNIQUE NOT NULL
    );


CREATE TABLE Estudiantes (
    id_estudiante     INTEGER PRIMARY KEY,
    id_usuario        INTEGER NOT NULL,
    PrestamosActivos INTEGER NOT NULL,
    Estado VARCHAR2(100) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);


CREATE TABLE Docentes (
    id_docente       INTEGER PRIMARY KEY,
    id_usuario        INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);


CREATE TABLE Investigadores (
    id_investigador   INTEGER PRIMARY KEY,
    id_usuario        INTEGER NOT NULL,
    NivelAcceso VARCHAR2(100) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);


CREATE TABLE Libros (
    id_libro          INTEGER PRIMARY KEY,
    id_estudiante       integer not null,
    Nombre            VARCHAR2(150) NOT NULL,
    autor             VARCHAR2(150),
    anio_publicacion NUMBER(4),
    CantidadPaginas INTEGER,
    Cantidad INTEGER,
    Descripcion VARCHAR2(100),
    FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante)
);


CREATE TABLE Prestamos (
    id_prestamo       INTEGER PRIMARY KEY,
    id_estudiante        INTEGER NOT NULL,
    id_libro          INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha_prestamo    DATE DEFAULT SYSDATE,
    fecha_devolucion  DATE,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_libro) REFERENCES Libros(id_libro)
);


CREATE TABLE DataSetsDescargados(
    id_Data_Set_Descargado  INTEGER PRIMARY KEY,
    id_investigador         INTEGER NOT NULL,
    Nombre                  VARCHAR2(300) NOT NULL,
    Cantidad                INTEGER NOT NULL,
    FOREIGN KEY (id_investigador) REFERENCES Investigadores(id_investigador)
);

CREATE TABLE MaterialExclusivo (
    id_material_exclusivo  INTEGER PRIMARY KEY,
    id_docente             INTEGER NOT NULL,
    nombre                 VARCHAR2(150) NOT NULL,
    descripcion            VARCHAR2(300) NOT NULL,
    FOREIGN KEY (id_docente) REFERENCES Docentes(id_docente)
);


CREATE TABLE Biblioteca(
    id_biblioteca       INTEGER PRIMARY KEY,
    CantidadMaterial    INTEGER NOT NULL,
    GestionPrestamo     INTEGER NOT NULL
);

