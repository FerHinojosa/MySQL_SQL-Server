import mysql.connector
from textblob import TextBlob

# Definir función para calcular la objetividad
def get_objectivity(text):
    return TextBlob(text).sentiment.subjectivity

# Conectar a la base de datos
try:
    connection = mysql.connector.connect(
        host='localhost',
        port='33060',
        database='nao',
        user='root',
        password='secret',
        charset='utf8mb4'
    )
    cursor = connection.cursor()

    # Consultar la base de datos solo para tweets que cumplan condiciones
    cursor.execute("SELECT texto FROM nao.tweet")
    
    # Almacenar textos con alta objetividad y calcular objetividad en una sola pasada
    tweets_objetivos = [
        (tweet[0], get_objectivity(tweet[0]))
        for tweet in cursor.fetchall()
        if get_objectivity(tweet[0]) > 0.9
    ]
    
    # Mostrar resultados y construir lista para análisis adicional si es necesario
    for tweet, objetividad in tweets_objetivos:
        print(f"Tweet: {tweet}, Sentiment: {objetividad}")
    
    # Encontrar el tweet con la objetividad más intensa
    if tweets_objetivos:
        texto_mas_objetivo, intensidad_mas_alta = max(tweets_objetivos, key=lambda x: abs(x[1]))
        print(f"El objetividad más intenso es '{texto_mas_objetivo}' con una objetividad de {intensidad_mas_alta:.2f}")
    else:
        print("No se encontraron tweets con objetividad superior a 0.9")

finally:
    # Cerrar la conexión a la base de datos
    if connection.is_connected():
        cursor.close()
        connection.close()
