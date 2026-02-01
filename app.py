from flask import Flask, jsonify, request
from threading import Lock
import os

app = Flask(__name__)

# In-memory data store with thread safety
data_store = {}
counter = 0
data_lock = Lock()


@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Welcome to CMPE-273 Lab 1',
        'status': 'success'
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy'
    })


@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all items"""
    return jsonify({
        'items': list(data_store.values()),
        'count': len(data_store)
    })


@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item by ID"""
    if item_id not in data_store:
        return jsonify({
            'error': 'Item not found'
        }), 404
    
    return jsonify(data_store[item_id])


@app.route('/api/items', methods=['POST'])
def create_item():
    """Create a new item"""
    global counter
    
    if not request.json:
        return jsonify({
            'error': 'Invalid request. JSON body required'
        }), 400
    
    with data_lock:
        counter += 1
        item = {
            'id': counter,
            'data': request.json
        }
        data_store[counter] = item
    
    return jsonify(item), 201


@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item"""
    if item_id not in data_store:
        return jsonify({
            'error': 'Item not found'
        }), 404
    
    if not request.json:
        return jsonify({
            'error': 'Invalid request. JSON body required'
        }), 400
    
    with data_lock:
        data_store[item_id]['data'] = request.json
        updated_item = data_store[item_id]
    
    return jsonify(updated_item)


@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item"""
    if item_id not in data_store:
        return jsonify({
            'error': 'Item not found'
        }), 404
    
    with data_lock:
        deleted_item = data_store.pop(item_id)
    
    return jsonify({
        'message': 'Item deleted successfully',
        'deleted_item': deleted_item
    })


if __name__ == '__main__':
    # Get configuration from environment variables
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', '5000'))
    
    app.run(host=host, port=port, debug=debug_mode)
