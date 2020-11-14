from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def __repr__(self): #for debug proporse
    return f'<Todo {self.id} {self.description}'

db.create_all() #sync database

@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description, completed=False)
    db.session.add(todo)
    db.session.commit()
    body['id'] = todo.id
    body['completed'] = todo.completed
    body['description'] = todo.description
    
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      abort(400)
    else:
      return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = Todo.query.get(todo_id)
    print('todo', todo)
    todo.completed = completed
    print('todo.completed', todo.completed)

    
    db.session.commit()
    print('todo', todo)
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))



@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.order_by('id').all())
