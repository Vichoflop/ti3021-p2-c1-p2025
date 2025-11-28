"""

HEAD: informacion adicional importante
-> Con que tipo de informacion voy a trabajar
    content-Type: application/json
-> Si tengo que autentcarm, como lo voy a hacer
    Authorization: secreto


BODY: Informacion principal de comunicacion

URAL: La ubicacion a donde voy a ir a buscar la informacion
STATUS: Estado de respuesta de la solicitud

FLUJO DE SOLICITUD
1.(Nosotros)Python -[Solicitud] ->  API 
2.API -[Respuesta] -> [Nosotros]Python

ESTRUCTURA DE ubicacion

[Declarar el protocolo]

https://universalis.app/api/v2/data-centers

[Donde esta la API]     [El recurso o endpoint]

SERIALIZACION DE LA INFORMACION
Utilizar  un estandar de ordenar la informacion que quiero
comunicaR, para ello,utilizo serializadores como:
-JSON(Javascript Object Notation)
    ["persona" : {"id" . 1092, "nombre" : "sebastian"}]

-XML(Extensible Markup Language)

    <persona>
        <id>1092</id>
        <nombre>Sebastian</npmbre>
    </persona>

"""

import requests

respuesta = requests.get("url = https://universalis.app/api/v2/data-centers")
codigo_respuesta = respuesta.status_code
data = respuesta.json()



print(f"Codigo de respuesta : {codigo_respuesta} ")
print(f"data : {data} ")


