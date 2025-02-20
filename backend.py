from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with backend

tasks = []  # Temporary storage (replace with database later)

categories = ["General"] 

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Retrieve all tasks."""
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    """Add a new task."""
    data = request.json
    new_task = {"task": data["task"], "category": data.get("category", "General"), "completed": False}
    tasks.append(new_task)
    return jsonify({"message": "Task added!", "task": new_task})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by index."""
    if 0 <= task_id < len(tasks):
        deleted_task = tasks.pop(task_id)
        return jsonify({"message": "Task deleted!", "task": deleted_task})
    return jsonify({"error": "Task not found!"}), 404

@app.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    """Mark a task as completed."""
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True
        return jsonify({"message": "Task marked as completed!", "task": tasks[task_id]})
    return jsonify({"error": "Task not found!"}), 404    

@app.route('/categories', methods=['GET'])
def get_categories():
    """Retrieve all categories."""
    return jsonify(categories)

@app.route('/categories', methods=['POST'])
def create_category():
    """Create a new category."""
    data = request.json
    new_category = data.get("category", "").strip()

    if not new_category:
        return jsonify({"error": "Category name cannot be empty!"}), 400

    if new_category in categories:
        return jsonify({"error": "Category already exists!"}), 400

    categories.append(new_category)
    return jsonify({"message": "Category created!", "category": new_category})


@app.route('/start_timer', methods=['POST'])
def start_timer():
    """Starts a Pomodoro timer (dummy endpoint for now)."""
    data = request.json
    work_time = int(data.get("work_time", 25))
    return jsonify({"message": f"Pomodoro timer started for {work_time} minutes!"})



if __name__ == '__main__':
    app.run(debug=True)
