import redis
import json
import sys

# Configuración de la base de datos
DATABASE_URL = "redis://localhost:6379"
r = redis.from_url(DATABASE_URL)

# Función para agregar una nueva receta
def add_receta():
    receta_id = r.incr("receta_id")  # Genera un nuevo ID
    nombre = input("Ingrese el nombre de la receta: ")
    ingredientes = input("Ingrese los ingredientes (separados por comas): ")
    procedimientos = input("Ingrese los pasos (separados por comas): ")

    nueva_receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "procedimientos": procedimientos
    }
    r.set(f"receta:{receta_id}", json.dumps(nueva_receta))
    print("Receta agregada exitosamente.\n")

# Función para actualizar una receta existente
def update_receta():
    receta_id = input("Ingrese el ID de la receta que desea actualizar: ")
    if not receta_id.isdigit():
        print("El ID debe ser un número. Intente de nuevo.")
        return

    nombre = input("Ingrese el nuevo nombre de la receta: ")
    ingredientes = input("Ingrese los nuevos ingredientes (separados por comas): ")
    procedimientos = input("Ingrese los nuevos pasos (separados por comas): ")

    receta_key = f"receta:{receta_id}"
    if r.exists(receta_key):
        receta = {
            "nombre": nombre,
            "ingredientes": ingredientes,
            "procedimientos": procedimientos
        }
        r.set(receta_key, json.dumps(receta))
        print("Receta actualizada exitosamente.\n")
    else:
        print("Receta no encontrada.\n")

# Función para eliminar una receta existente
def delete_receta():
    receta_id = input("Ingrese el ID de la receta que desea eliminar: ")
    if not receta_id.isdigit():
        print("El ID debe ser un número. Intente de nuevo.")
        return

    receta_key = f"receta:{receta_id}"
    if r.exists(receta_key):
        r.delete(receta_key)
        print("Receta eliminada exitosamente.\n")
    else:
        print("Receta no encontrada.\n")

# Función para ver el listado de recetas
def list_recetas():
    receta_keys = r.keys("receta:*")
    if receta_keys:
        print("Listado de recetas:")
        for key in receta_keys:
            receta_id = key.decode().split(":")[1]
            receta = json.loads(r.get(key))
            print(f"ID: {receta_id}, Nombre: {receta['nombre']}")
    else:
        print("No hay recetas disponibles.\n")

# Función para buscar ingredientes y pasos de una receta
def search_receta():
    receta_id = input("Ingrese el ID de la receta que desea buscar: ")
    if not receta_id.isdigit():
        print("El ID debe ser un número. Intente de nuevo.")
        return

    receta_key = f"receta:{receta_id}"
    if r.exists(receta_key):
        receta = json.loads(r.get(receta_key))
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
