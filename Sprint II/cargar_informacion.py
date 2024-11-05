import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json

def convert_iso_to_mysql_format(iso_datetime):
    """
    Convierte una fecha en formato ISO 8601 a un formato compatible con MySQL.

    Parámetros:
        iso_datetime (str): Fecha y hora en formato ISO 8601.

    Retorna:
        str: Fecha y hora en formato compatible con MySQL.
    """
    parsed_date = datetime.strptime(iso_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
    return parsed_date.strftime('%Y-%m-%d %H:%M:%S')

# Configuración de la conexión
def create_connection():
    """
    Crea y devuelve una conexión a la base de datos MySQL.

    Retorna:
        connection: Objeto de conexión a la base de datos.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port='33060',
            database='nao',
            user='root',
            password='secret',
            charset='utf8mb4'
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def execute_sql_script(cursor, script_path):
    """
    Ejecuta un script SQL desde un archivo.

    Parámetros:
        cursor (mysql.connector.cursor): Cursor de la conexión a MySQL.
        script_path (str): Ruta del archivo SQL que contiene el script.
    """
    with open(script_path, 'r') as sql_file:
        sql_script = sql_file.read()
    sql_statements = sql_script.split(';')
    
    for statement in sql_statements:
        if statement.strip():  # Ignorar líneas vacías
            cursor.execute(statement)
            print(f"Ejecutando: {statement.strip()}")

def insert_tweet_data(cursor, record):
    """
    Inserta un tweet y sus hashtags en las tablas correspondientes.

    Parámetros:
        cursor (mysql.connector.cursor): Cursor de la conexión a MySQL.
        record (dict): Diccionario que contiene los datos del tweet.
    """
    insert_query_tweet = '''
        INSERT INTO nao.tweet (id_tweet, texto, usuario, fecha, retweets, favoritos)
        VALUES (%s, %s, %s, %s, %s, %s);
    '''
    tweet_values = (
        record['id'],
        record['texto'],
        record['usuario'],
        convert_iso_to_mysql_format(record['fecha']),
        record['retweets'],
        record['favoritos'],
    )
    
    cursor.execute(insert_query_tweet, tweet_values)
    id_tweet = cursor.lastrowid

    if record['hashtags']:
        insert_query_hash = '''
            INSERT INTO nao.hashtag (hashtags, id_tweets)
            VALUES (%s, %s);
        '''
        for hashtag in record['hashtags']:
            cursor.execute(insert_query_hash, (hashtag, id_tweet))

def main():
    """
    Ejecuta el proceso principal: conecta a la base de datos, ejecuta el script de creación de tablas
    e inserta datos desde un archivo JSON.
    """
    connection = create_connection()
    if connection:
        cursor = connection.cursor()

        # Ejecutar el script SQL de creación de tablas
        execute_sql_script(cursor, 'crearTabla.sql')
        connection.commit()

        # Cargar e insertar datos desde el archivo JSON
        with open('../tweets_extraction.json', 'r') as json_file:
            data = json.load(json_file)
            for record in data:
                insert_tweet_data(cursor, record)
                
        connection.commit()
        cursor.close()
        connection.close()
        print("Operación completada exitosamente.")

if __name__ == "__main__":
    main()
