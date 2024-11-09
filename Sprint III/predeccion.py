import mysql.connector
from collections import Counter
import re
from textblob import TextBlob

# Función para calcular la objetividad
def get_objectivity(text):
    return TextBlob(text).sentiment.subjectivity

# Función para calcular la polaridad (sentimiento)
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Conjunto de palabras comunes a excluir
common_words = {"del", "para", "como", "donde", "pero", "porque", "entonces", "sobre", "tiene", "todos", "muchos", "algunas", "siempre", "ahora", "estaba", "están", "aunque"}

try:
    # Conectar a la base de datos
    connection = mysql.connector.connect(
        host='localhost',
        port='33060',
        database='nao',
        user='root',
        password='secret',
        charset='utf8mb4'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT texto FROM nao.tweet")

    # Lista para todas las palabras filtradas
    all_words = []

    # Procesar cada tweet de la base de datos
    for (texto,) in cursor.fetchall():
        # Extraer palabras que tengan más de 5 caracteres y no estén en `common_words`
        words = [word.lower() for word in re.findall(r'\b\w+\b', texto) if len(word) > 5 and word.lower() not in common_words]
        all_words.extend(words)

    # Contar las palabras más comunes
    word_counts = Counter(all_words)
    print("Top 10 palabras más comunes:", word_counts.most_common(10))

finally:
    # Cerrar la conexión a la base de datos
    if connection.is_connected():
        cursor.close()
        connection.close()
