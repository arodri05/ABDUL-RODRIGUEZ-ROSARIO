from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys

# Configuración de la base de datos
DATABASE_URL = "mariadb+mariadbconnector://user:password@localhost/recetas.db"

# Crear la base
Base = declarative_base()

# Definir el modelo de la tabla recetas
class Receta(Base):
    __tablename__ = 'recetas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    ingredientes = Column(String(255), nullable=False)
    procedimientos = Column(String(255), nullable=False)

# Configurar el motor y la sesión
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Crear la tabla
Base.metadata.create_all(engine)

# Función para agregar una nueva receta
def add_receta():
    nombre = input("Ingrese el nombre de la receta: ")
    ingredientes = input("Ingrese los ingredientes (separados por comas): ")
    procedimientos = input("Ingrese los pasos (separados por comas): ")

    nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, procedimientos=procedimientos)
    session.add(nueva_receta)
    session.commit()
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

    receta = session.query(Receta).filter_by(id=receta_id).first()
    if receta:
        receta.nombre = nombre
        receta.ingredientes = ingredientes
        receta.procedimientos = procedimientos
        session.commit()
        print("Receta actualizada exitosamente.\n")
    else:
        print("Receta no encontrada.\n")

# Función para eliminar una receta existente
def delete_receta():
    receta_id = input("Ingrese el ID de la receta que desea eliminar: ")
    if not receta_id.isdigit():
        print("El ID debe ser un número. Intente de nuevo.")
        return

    receta = session.query(Receta).filter_by(id=receta_id).first()
    if receta:
        session.delete(receta)
        session.commit()
        print("Receta eliminada exitosamente.\n")
    else:
        print("Receta no encontrada.\n")

# Función para ver el listado de recetas
def list_recetas():
    recetas = session.query(Receta).all()
    if recetas:
        print("Listado de recetas:")
        for receta in recetas:
            print(f"ID: {receta.id}, Nombre: {receta.nombre}")
    else:
        print("No hay recetas disponibles.\n")

# Función para buscar ingredientes y pasos de una receta
def search_receta():
    receta_id = input("Ingrese el ID de la receta que desea buscar: ")
    if not receta_id.isdigit():
        print("El ID debe ser un número. Intente de nuevo.")
        return

    receta = session.query(Receta).filter_by(id=receta_id).first()
    if receta:
        print(f"Nombre: {receta.nombre}\nIngredientes: {receta.ingredientes}\nPasos: {receta.procedimientos}")
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
