from pymongo import MongoClient
import sys

# Configuración de la base de datos
DATABASE_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "recetas_db"
COLLECTION_NAME = "recetas"

# Conectar a la base de datos
client = MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Función para agregar una nueva receta
def add_receta():
    nombre = input("Ingrese el nombre de la receta: ")
    ingredientes = input("Ingrese los ingredientes (separados por comas): ")
    procedimientos = input("Ingrese los pasos (separados por comas): ")

    nueva_receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "procedimientos": procedimientos
    }
    collection.insert_one(nueva_receta)
    print("Receta agregada exitosamente.\n")

# Función para actualizar una receta existente
def update_receta():
    receta_id = input("Ingrese el ID de la receta que desea actualizar: ")
    
    nombre = input("Ingrese el nuevo nombre de la receta: ")
    ingredientes = input("Ingrese los nuevos ingredientes (separados por comas): ")
    procedimientos = input("Ingrese los nuevos pasos (separados por comas): ")

    query = {"_id": ObjectId(receta_id)}
    new_values = {"$set": {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "procedimientos": procedimientos
    }}
    
    result = collection.update_one(query, new_values)
    if result.modified_count > 0:
        print("Receta actualizada exitosamente.\n")
    else:
        print("Receta no encontrada.\n")

# Función para eliminar una receta existente
def delete_receta():
    receta_id = input("Ingrese el ID de la receta que desea eliminar: ")

    query = {"_id": ObjectId(receta_id)}
    result = collection.delete_one(query)
    if result.deleted_count > 0:
        print("Receta eliminada exitosamente.\n")
    else:
        print("Receta no encontrada.\n")

# Función para ver el listado de recetas
def list_recetas():
    recetas = collection.find()
    if recetas:
        print("Listado de recetas:")
        for receta in recetas:
            print(f"ID: {receta['_id']}, Nombre: {receta['nombre']}")
    else:
        print("No hay recetas disponibles.\n")

# Función para buscar ingredientes y pasos de una receta
def search_receta():
    receta_id = input("Ingrese el ID de la receta que desea buscar: ")

    query = {"_id": ObjectId(receta_id)}
    receta = collection.find_one(query)
    if receta:
        print(f"Nombre: {receta['nombre']}\nIngredientes: {receta['ingredientes']}\nPasos: {receta['procedimientos']}")
    else:
        print("No se encontró la receta.\n")

# Función principal para mostrar el menú y manejar las opciones del usuario
def main():
    while True:
        print("\nLibro de Recetas")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            add_receta()
        elif choice == '2':
            update_receta()
        elif choice == '3':
            delete_receta()
        elif choice == '4':
            list_recetas()
        elif choice == '5':
            search_receta()
        elif choice == '6':
            print("GRACIAS POR VISITAR NUESTRO LIBRO DE RECETAS")
            sys.exit()
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
