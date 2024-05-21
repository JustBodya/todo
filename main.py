from flask import Flask, request, jsonify, abort
from models import Task, db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Роут с методом GET, возвращает JSON-список задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


# Роут с методом POST, добавляет новую задачу в БД
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    if 'title' not in data:
        abort(400, description="Необходимо поле title")
    
    task = Task(title=data['title'], description=data.get('description'))
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


# Роут с методом GET, возвращает JSON-список определенной задачи
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())


# Роут с методом PUT, обновляет определенную задачу в БД
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']

    db.session.commit()
    return jsonify(task.to_dict())


# Роут с методом DELETE, удаляет определенную задачу в БД
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
