from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = 'data.db'

# Initialize database
with sqlite3.connect(DB) as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)")

# Create
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO items (name) VALUES (?)", (data['name'],))
    return jsonify({'message': 'Item created'}), 201

# Read
@app.route('/items', methods=['GET'])
def read_items():
    with sqlite3.connect(DB) as conn:
        items = conn.execute("SELECT * FROM items").fetchall()
    return jsonify([{'id': i[0], 'name': i[1]} for i in items])

# Update
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    with sqlite3.connect(DB) as conn:
        conn.execute("UPDATE items SET name = ? WHERE id = ?", (data['name'], item_id))
    return jsonify({'message': 'Item updated'})

# Delete
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    return jsonify({'message': 'Item deleted'})

if __name__ == '__main__':
    app.run(debug=True)
