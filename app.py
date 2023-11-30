# Importa las librerías necesarias para el manejo de la base de datos y variables de entorno
import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd

# Define la clase DatabaseManager
class DatabaseManager:
    # Método constructor de la clase
    def __init__(self):
        # Carga las variables de entorno desde el archivo .env
        load_dotenv()
        # Inicializa las variables de instancia con las credenciales de la base de datos
        self.db_server_name = os.getenv('db_server_name')
        self.db_name = os.getenv('db_name')
        self.db_user = os.getenv('db_user')
        self.db_password = os.getenv('db_password')
        self.db_port = os.getenv('db_port')
        # Inicializa la conexión y el cursor de la base de datos como None
        self.connection = None
        self.cursor = None

    # Método para conectar a la base de datos
    def connect(self):
        try:
            # Intenta establecer una conexión con la base de datos usando SSL
            self.connection = psycopg2.connect(
                host=self.db_server_name,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port,
                sslmode='require'
            )
            # Crea un cursor para la conexión
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            # Maneja cualquier error de conexión e imprime un mensaje de error
            print(f"Error al conectar a la base de datos: {e}")
            # Establece la conexión y el cursor a None en caso de error
            self.connection = None
            self.cursor = None

    # Método para cerrar la conexión a la base de datos
    def close(self):
        # Si hay una conexión activa, cierra el cursor y la conexión
        if self.connection:
            self.cursor.close()
            self.connection.close()

    # Método para recuperar datos mediante una consulta SELECT
    def fetch_data(self, query):
        # Verifica si la conexión y el cursor son válidos
        if self.connection is None or self.cursor is None:
            print("No hay conexión a la base de datos.")
            return []
        try:
            # Ejecuta la consulta SELECT
            self.cursor.execute(query)
            # Retorna los resultados de la consulta
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            # Maneja cualquier error durante la recuperación de datos
            print(f"Error al recuperar datos: {e}")
            return []
    
    # Método para mostrar un menú interactivo y manejar las operaciones de la base de datos
    def main_menu(self):
        # Establece la conexión a la base de datos
        self.connect()
        # Ciclo infinito para mantener el menú en ejecución hasta que el usuario decida salir
        while True:
            # Imprime las opciones del menú
            print("\nMenú de Base de Datos")
            print("1. Realizar consulta SELECT * FROM PADRON")
            print("2. Salir")
            # Solicita al usuario elegir una opción
            choice = input("Elige una opción: ")
            if choice == '1':
                # Solicita al usuario ingresar una consulta SELECT
                query = "SELECT * FROM PADRON"
                # Llama al método fetch_data para ejecutar la consulta y obtener los resultados
                results = self.fetch_data(query)
                # Imprime cada fila de los resultados
                for row in results:
                    print(row)
            # Opción 5: Salir
            elif choice == '2':
                # Imprime un mensaje y rompe el ciclo para salir del programa
                print("Saliendo del programa.")
                break
            else:
                # Maneja el caso de una opción no válida
                print("Opción no válida. Por favor, intenta de nuevo.")
        # Cierra la conexión a la base de datos al salir del menú
        self.close()

# Punto de entrada del script
if __name__ == "__main__":
    # Crea una instancia de DatabaseManager y llama al menú principal
    db_manager = DatabaseManager()
    db_manager.main_menu()

