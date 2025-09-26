class usuario:
    def __init__(self, nombre:str,rut: int, correo: str):
        self._nombre: str = nombre
        self._rut:  int = rut
        self._correo: str = correo


class Estudiantes:
    def __init__(self, PrestamosActivos: int, EstadoDeuda: str, HistorialPrestamo: str):
        self.__PrestamosActivos: int = PrestamosActivos
        self._EstadoDeuda: str = EstadoDeuda
        self._HistorialPrestamo: str = HistorialPrestamo



class Docentes:
    def __init__(self, MaterialExclusivoAccedido: str):
        self.__MaterialExclusivoAccedido: str = MaterialExclusivoAccedido

class Investigadores:
    def __init__(self, NivelDeAcceso: str, DataSetsDescargados: int ):
        self.__NivelDeAcceso: str= NivelDeAcceso
        self.__DataSetsDescargados: int = DataSetsDescargados


class usuario:
    def __init__(self, CantidadMaterial: int, GestionUsuario: int, GestionPrestamo: int ):
        self.CantidadMaterial: int = CantidadMaterial
        self._GestionUsuario: int = GestionUsuario
        self._GestionPrestamo: int = GestionPrestamo