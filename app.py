"""
Intro to Flask - Simple Todo API

This application demonstrates how to build a basic REST API
using Flask without a database (in-memory storage only).
"""

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# -------------------------------
# In-memory storage for todos
# -------------------------------
# Each todo will be a dictionary:
# {
#   "id": int,
#   "title": str,
#   "completed": bool
# }

todos = []
next_id = 1  # Used to assign unique IDs


# -------------------------------
# GET /todos
# Get all todos
# -------------------------------
@app.route("/todos", methods=["GET"])
def get_todos():
    """
    Returns a list of all todos.
    """
    return jsonify(todos), 200


# -------------------------------
# GET /todos/<id>
# Get a single todo by ID
# -------------------------------
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    """
    Returns one todo by its ID.
    """
    for todo in todos:
        if todo["id"] == todo_id:
            return jsonify(todo), 200

    # If todo not found
    abort(404, description="Todo not found")


# -------------------------------
# POST /todos
# Create a new todo
# -------------------------------
@app.route("/todos", methods=["POST"])
def create_todo():
    """
    Creates a new todo.
    Expects JSON with at least a 'title'.
    Example:
    {
        "title": "Buy groceries"
    }
    """
    global next_id

    data = request.get_json()

    # Validate input
    if not data or "title" not in data:
        abort(400, description="Title is required")

    new_todo = {
        "id": next_id,
        "title": data["title"],
        "completed": False
    }

    todos.append(new_todo)
    next_id += 1

    return jsonify(new_todo), 201


# -------------------------------
# PUT /todos/<id>
# Update an existing todo
# -------------------------------
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """
    Updates an existing todo.
    Example:
    {
        "title": "Buy groceries",
        "completed": true
    }
    """
    data = request.get_json()

    for todo in todos:
        if todo["id"] == todo_id:
            # Update fields if they exist in request
            if "title" in data:
                todo["title"] = data["title"]
            if "completed" in data:
                todo["completed"] = data["completed"]

            return jsonify(todo), 200

    abort(404, description="Todo not found")


# -------------------------------
# DELETE /todos/<id>
# Delete a todo
# -------------------------------
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """
    Deletes a todo by ID.
    """
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return jsonify({"message": "Todo deleted"}), 200

    abort(404, description="Todo not found")


# -------------------------------
# Run the application
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
