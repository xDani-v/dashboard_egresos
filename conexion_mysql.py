import mysql.connector


def conectar_mysql():
    # Configurar conexión con MySQL (reemplaza los valores con los de tu conexión)
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'datosbd',
        'port': 3306
    }

    # Conectarse a MySQL
    conn = mysql.connector.connect(**config)
    return conn
