from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Cambia esto por una clave secreta más segura

# Configuración de la base de datos
DATABASE_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "recetas_db"
COLLECTION_NAME = "recetas"

client = MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Ruta para la página principal (listado de recetas)
@app.route('/')
def index():
    recetas = collection.find()
    return render_template('index.html', recetas=recetas)

# Ruta para agregar una nueva receta
@app.route('/add', methods=['GET', 'POST'])
def add_receta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ingredientes = request.form['ingredientes']
        procedimientos = request.form['procedimientos']

        nueva_receta = {
            "nombre": nombre,
            "ingredientes": ingredientes,
            "procedimientos": procedimientos
        }
        collection.insert_one(nueva_receta)
        flash("Receta agregada exitosamente.", "success")
        return redirect(url_for('index'))

    return render_template('add_receta.html')

# Ruta para actualizar una receta existente
@app.route('/update/<receta_id>', methods=['GET', 'POST'])
def update_receta(receta_id):
    receta = collection.find_one({"_id": ObjectId(receta_id)})
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        ingredientes = request.form['ingredientes']
        procedimientos = request.form['procedimientos']

        new_values = {"$set": {
            "nombre": nombre,
            "ingredientes": ingredientes,
            "procedimientos": procedimientos
        }}
        collection.update_one({"_id": ObjectId(receta_id)}, new_values)
        flash("Receta actualizada exitosamente.", "success")
        return redirect(url_for('index'))

    return render_template('update_receta.html', receta=receta)

# Ruta para eliminar una receta existente
@app.route('/delete/<receta_id>')
def delete_receta(receta_id):
    collection.delete_one({"_id": ObjectId(receta_id)})
    flash("Receta eliminada exitosamente.", "success")
    return redirect(url_for('index'))

# Ruta para ver los detalles de una receta
@app.route('/receta/<receta_id>')
def search_receta(receta_id):
    receta = collection.find_one({"_id": ObjectId(receta_id)})
    if receta:
        return render_template('receta_detalle.html', receta=receta)
    else:
        flash("No se encontró la receta.", "danger")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
