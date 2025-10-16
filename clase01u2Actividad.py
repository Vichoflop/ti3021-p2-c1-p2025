class Usuario:
    def __init__(self, nombre: str, rut: int, correo: str):
        self._nombre = nombre
        self._rut = rut
        self._correo = correo

    # --- Propiedades de solo lectura ---
    @property
    def nombre(self):
        return self._nombre

    @property
    def rut(self):
        return self._rut

    @property
    def correo(self):
        return self._correo


class Estudiantes:
    def __init__(self, prestamos_activos: int, estado_deuda: str, historial_prestamo: str):
        self._prestamos_activos = prestamos_activos
        self._estado_deuda = estado_deuda
        self._historial_prestamo = historial_prestamo

    # --- Propiedades de solo lectura ---
    @property
    def prestamos_activos(self):
        return self._prestamos_activos

    @property
    def estado_deuda(self):
        return self._estado_deuda

    @property
    def historial_prestamo(self):
        return self._historial_prestamo


class Docentes:
    def __init__(self, material_exclusivo_accedido: str):
        self._material_exclusivo_accedido = material_exclusivo_accedido

    @property
    def material_exclusivo_accedido(self):
        return self._material_exclusivo_accedido


class Investigadores:
    def __init__(self, nivel_de_acceso: str, datasets_descargados: int):
        self._nivel_de_acceso = nivel_de_acceso
        self._datasets_descargados = datasets_descargados

    # --- Propiedades de solo lectura ---
    @property
    def nivel_de_acceso(self):
        return self._nivel_de_acceso

    @property
    def datasets_descargados(self):
        return self._datasets_descargados


