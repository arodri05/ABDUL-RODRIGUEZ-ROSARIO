import sqlite3

def init_db():
    conn = sqlite3.connect('presupuestor2024.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def add_item(name, category, amount):
    conn = sqlite3.connect('presupuestor2024.db')
    c = conn.cursor()
    c.execute('INSERT INTO items (name, category, amount) VALUES (?, ?, ?)', (name, category, amount))
    conn.commit()
    conn.close()

def search_items(keyword):
    conn = sqlite3.connect('presupuestor2024.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items WHERE name LIKE ? OR category LIKE ?', (f'%{keyword}%', f'%{keyword}%'))
    results = c.fetchall()
    conn.close()
    return results

def edit_item(item_id, name=None, category=None, amount=None):
    conn = sqlite3.connect('presupuestor2024.db')
    c = conn.cursor()
    if name:
        c.execute('UPDATE items SET name = ? WHERE id = ?', (name, item_id))
    if category:
        c.execute('UPDATE items SET category = ? WHERE id = ?', (category, item_id))
    if amount:
        c.execute('UPDATE items SET amount = ? WHERE id = ?', (amount, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect('presupuestor2024.db')
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
import argparse

def main():
    parser = argparse.ArgumentParser(description='Sistema de Registro de Presupuesto')
    subparsers = parser.add_subparsers(dest='command')

    # Subcomando para añadir un artículo
    parser_add = subparsers.add_parser('add', help='Añadir un nuevo artículo')
    parser_add.add_argument('name', type=str, help='Nombre del artículo')
    parser_add.add_argument('category', type=str, help='Categoría del artículo')
    parser_add.add_argument('amount', type=float, help='Monto del artículo')

    # Subcomando para buscar artículos
    parser_search = subparsers.add_parser('search', help='Buscar artículos')
    parser_search.add_argument('keyword', type=str, help='Palabra clave para buscar')

    # Subcomando para editar un artículo
    parser_edit = subparsers.add_parser('edit', help='Editar un artículo existente')
    parser_edit.add_argument('id', type=int, help='ID del artículo a editar')
    parser_edit.add_argument('--name', type=str, help='Nuevo nombre del artículo')
    parser_edit.add_argument('--category', type=str, help='Nueva categoría del artículo')
    parser_edit.add_argument('--amount', type=float, help='Nuevo monto del artículo')

    # Subcomando para eliminar un artículo
    parser_delete = subparsers.add_parser('delete', help='Eliminar un artículo')
    parser_delete.add_argument('id', type=int, help='ID del artículo a eliminar')

    args = parser.parse_args()

    if args.command == 'add':
        add_item(args.name, args.category, args.amount)
        print(f'Artículo "{args.name}" añadido.')
    elif args.command == 'search':
        results = search_items(args.keyword)
        for row in results:
            print(f'ID: {row[0]}, Nombre: {row[1]}, Categoría: {row[2]}, Monto: {row[3]}')
    elif args.command == 'edit':
        edit_item(args.id, args.name, args.category, args.amount)
        print(f'Artículo ID {args.id} editado.')
    elif args.command == 'delete':
        delete_item(args.id)
        print(f'Artículo ID {args.id} eliminado.')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
##Para usar la aplicación, ejecuta los siguientes comandos en la terminal:

##Añadir un artículo:
## python presupuesto2024_parcial_1.py add "TERMO" "ENVASES" 123.45

##Buscar artículos:
## python presupuesto2024_parcial_1.py search "palabra clave"

##Editar un artículo:
## python presupuesto2024_parcial_1.py edit 1 --name "Nuevo Nombre" --category "Nueva Categoría" --amount 543.21

##Eliminar un artículo:
## python presupuesto2024_parcial_1.py delete 1
    
