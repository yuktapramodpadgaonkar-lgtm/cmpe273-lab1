# CMPE-273 Lab 1 - REST API

A simple RESTful API application built with Flask for CMPE-273 Enterprise Distributed Systems course.

## Features

- Simple REST API with CRUD operations
- In-memory data storage
- JSON request/response format
- Health check endpoint

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yuktapramodpadgaonkar-lgtm/cmpe273-lab1.git
cd cmpe273-lab1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Home
```
GET /
```
Returns a welcome message.

### Health Check
```
GET /health
```
Returns the health status of the API.

### Get All Items
```
GET /api/items
```
Returns all items in the data store.

### Get Single Item
```
GET /api/items/<id>
```
Returns a specific item by ID.

### Create Item
```
POST /api/items
Content-Type: application/json

{
  "name": "example",
  "value": "data"
}
```
Creates a new item and returns it with an assigned ID.

### Update Item
```
PUT /api/items/<id>
Content-Type: application/json

{
  "name": "updated",
  "value": "new data"
}
```
Updates an existing item.

### Delete Item
```
DELETE /api/items/<id>
```
Deletes an item by ID.

## Example Usage

### Using curl:

```bash
# Get home message
curl http://localhost:5000/

# Create an item
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": "123"}'

# Get all items
curl http://localhost:5000/api/items

# Get a specific item
curl http://localhost:5000/api/items/1

# Update an item
curl -X PUT http://localhost:5000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "updated", "value": "456"}'

# Delete an item
curl -X DELETE http://localhost:5000/api/items/1
```

## License

This project is created for educational purposes as part of CMPE-273 coursework.