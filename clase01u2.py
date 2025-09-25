class Cliente:
    def __init__(self,nombre: str,rut: str, edad: int):
        self.__nombre = nombre
        self.__rut = rut
        self.__edad = edad

    @property
    def nombre(self):
        return self.__nombre 
        

Cliente1: Cliente = Cliente(
    nombre="Felipe Villaroel",
    rut="21789567-k",
    edad=21
)

print(Cliente1.nombre)