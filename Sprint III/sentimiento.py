import mysql.connector
from textblob import TextBlob

# Función para calcular la polaridad del sentimiento
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

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

    # Lista para almacenar los textos con polaridad positiva alta
    textos_sentimentales = [
        (texto[0], get_sentiment(texto[0]))
        for texto in cursor.fetchall()
        if get_sentiment(texto[0]) > 0.9
    ]

    # Mostrar los textos con polaridad alta (opcional)
    for texto, sentimiento in textos_sentimentales:
        print(f"Texto: {texto}, Sentimiento: {sentimiento}")

    # Encontrar el texto con la intensidad de sentimiento más alta
    if textos_sentimentales:
        texto_mas_intenso, intensidad_mas_alta = max(textos_sentimentales, key=lambda x: abs(x[1]))
        print(f"\nEl sentimiento más intenso es '{texto_mas_intenso}' con una intensidad de {intensidad_mas_alta:.2f}")
    else:
        print("No se encontraron textos con sentimiento superior a 0.9")

finally:
    # Cerrar la conexión a la base de datos
    if connection.is_connected():
        cursor.close()
        connection.close()
