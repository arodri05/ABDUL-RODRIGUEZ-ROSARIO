import sqlite3
import sys

# Función para conectar a la base de datos y crear la tabla si no existe
def init_db():
    conn = sqlite3.connect('recetas.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS recetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        ingredientes TEXT NOT NULL,
        procedimientos TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Función para agregar una nueva receta
def add_receta():
    nombre = input("Ingrese el nombre de la receta: ")
    ingredientes = input("Ingrese los ingredientes (separados por comas): ")
    procedimientos = input("Ingrese los pasos (separados por comas): ")
    
    conn = sqlite3.connect('recetas.db')
    c = conn.cursor()
    c.execute('INSERT INTO recetas (nombre, ingredientes, procedimientos) VALUES (?, ?, ?)', (nombre, ingredientes, procedimientos))
    conn.commit()
    conn.close()
    print("Receta agregada exitosamente.\n")

# Función para actualizar una receta existente
def update_receta():
    receta_id = input("Ingrese el ID de la receta que desea actualizar: ")
    nombre = input("Ingrese el nuevo nombre de la receta: ")
    ingredientes = input("Ingrese los nuevos ingredientes (separados por comas): ")
    procedimientos = input("Ingrese los nuevos pasos (separados por comas): ")
    
    conn = sqlite3.connect('recetas.db')
    c = conn.cursor()
    c.execute('''
    UPDATE recetas 
    SET nombre = ?, ingredientes = ?, procedimientos = ? 
    WHERE id = ?
    ''', (nombre, ingredientes, procedimientos, receta_id))
    conn.commit()
    conn.close()
    print("Receta actualizada exitosamente.\n")

# Función para eliminar una receta existente
def delete_receta():
    receta_id = input("Ingrese el ID de la receta que desea eliminar: ")
    
    conn = sqlite3.connect('recetas.db')
    c = conn.cursor()
    c.execute('DELETE FROM recetas WHERE id = ?', (receta_id,))
    conn.commit()
    conn.close()
    print("Receta eliminada exitosamente.\n")

# Función para ver el listado de recetas
def list_recetas():
    conn = sqlite3.connect('recetas.db')
    c = conn.cursor()
    c.execute('SELECT id, nombre FROM recetas')
    recetas = c.fetchall()
    conn.close()
    
    if recetas:
        print("Listado de recetas:")
        for receta in recetas:
            print(f"ID: {receta[0]}, Nombre: {receta[1]}")
    else:
        print("No hay recetas disponibles.\n")

# Función para buscar ingredientes y pasos de una receta
def search_receta():
    receta_id = input("Ingrese el ID de la receta que desea buscar: ")
    
    conn = sqlite3.connect('recetas.db')
    c = conn.cursor()
    c.execute('SELECT nombre, ingredientes, procedimientos FROM recetas WHERE id = ?', (receta_id,))
    receta = c.fetchone()
    conn.close()
    
    if receta:
        print(f"Nombre: {receta[0]}\nIngredientes: {receta[1]}\nPasos: {receta[2]}")
    else:
        print("No se encontró la receta.\n")

# Función principal para mostrar el menú y manejar las opciones del usuario
def main():
    init_db()
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
            print("GRACIAS POR VISITAR NUESTRO LIBRO DE RESETAS")
            sys.exit()
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
