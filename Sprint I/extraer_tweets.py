import json
import jsonschema


def verificar_campos_vacios(datos_json):
    """
    Encuentra y devuelve una lista de campos vacíos en el JSON.

    Parámetros:
    datos_json (dict o list): Estructura de datos JSON.

    Retorna:
    list: Lista de claves con campos vacíos.
    """
    campos_vacios = []
    if isinstance(datos_json, dict):
        for clave, valor in datos_json.items():
            if valor in [None, '', []]:
                campos_vacios.append(clave)
            elif isinstance(valor, (dict, list)):
                campos_vacios.extend(verificar_campos_vacios(valor))
    elif isinstance(datos_json, list):
        for elemento in datos_json:
            campos_vacios.extend(verificar_campos_vacios(elemento))
    return campos_vacios


def validar_json(datos, esquema):
    """
    Valida un JSON usando un esquema dado.

    Parámetros:
    datos (dict): Datos JSON cargados.
    esquema (dict): Esquema de JSON Schema para la validación.

    Retorna:
    None
    """
    try:
        jsonschema.validate(instance=datos, schema=esquema)
        print("\nEl archivo JSON cumple con el esquema especificado.")
    except jsonschema.exceptions.ValidationError as error:
        print(f"\nError de validación del esquema: {error.message}")


def mostrar_informacion(datos):
    """
    Muestra la información de cada tweet en formato legible.

    Parámetros:
    datos (list): Lista de tweets con detalles como texto, usuario, etc.

    Retorna:
    None
    """
    for tweet in datos:
        print("\n" + "=" * 50)
        print(f"ID del Tweet: {tweet.get('id')}")
        print(f"Texto: {tweet.get('texto')}")
        print(f"Usuario: {tweet.get('usuario')}")
        hashtags = tweet.get('hashtags', [])
        print(f"Hashtags: {', '.join(hashtags) if hashtags else 'Ninguno'}")
        print(f"Fecha: {tweet.get('fecha')}")
        print(f"Retweets: {tweet.get('retweets', 0)}")
        print(f"Favoritos: {tweet.get('favoritos', 0)}")
    print("\n" + "=" * 50)


# Cargar el archivo JSON
with open('../../tweets_extraction.json', 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)

# Definición del esquema de JSON para la validación
esquema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "texto": {"type": "string"},
            "usuario": {"type": "string"},
            "hashtags": {"type": "array", "items": {"type": "string"}},
            "fecha": {"type": "string", "format": "date-time"},
            "retweets": {"type": "number"},
            "favoritos": {"type": "number"}
        },
        "required": ["id", "texto", "usuario", "hashtags", "fecha",
                     "retweets", "favoritos"]
    }
}

# Validar el JSON con el esquema
validar_json(datos, esquema)

# Verificar si existen campos vacíos
campos_vacios = verificar_campos_vacios(datos)
if campos_vacios:
    print("\nSe encontraron campos vacíos:", ", ".join(campos_vacios))
else:
    print("\nTodos los campos se encuentra llenos.")

# Mostrar la información de los tweets
mostrar_informacion(datos)
