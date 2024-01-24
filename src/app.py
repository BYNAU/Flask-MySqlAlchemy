from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

app.app_context().push() #abriendo un contexto de manera manual si no no se puede usar db.create_all()
db = SQLAlchemy(app)
ma = Marshmallow(app)

## Creamos el modelo
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __init__(self,title,description):
        self.title = title
        self.description = description

##Lee todas las clases que sean db.Models.
##Crea todas las tablas que tengamos definidas como en este caso Task
db.create_all()

## Creamos un esquema para interactuar de forma facil con nuestros modelos.
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many = True)

## Ruta CREATE TASK - POST
@app.route('/tasks', methods=['POST'])
def create_task():
    
    title = request.json['title']
    description = request.json['description']

    ## Llamamos al constructor de Task para crear una nueva tarea.
    new_task = Task(title, description)
    print("Tarea creada con exito.")

    ## Almacenamos los datos en la base de datos.
    db.session.add(new_task)
    db.session.commit()
    print("Almacenamiento en la base de datos --> OK!")

    return task_schema.jsonify(new_task)

## Ruta READ ALL - GET
@app.route('/tasks', methods=['GET'])

def get_tasks():
    ## Nos devuelve todas las tareas
    all_tasks = Task.query.all()
    ## Lista con los datos
    result = tasks_schema.dump(all_tasks)
    ## Convertimos en JSON los resultados de select de la base de datos por el ORM.
    return jsonify(result)

@app.route('/task/<id>', methods=['GET'])
## Read Single Task - GET
def get_task(id):
    task = Task.query.get(id)

    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])

def update_task(id):
    task = Task.query.session.get(Task, id)
    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()

    return task_schema.jsonify(task)

## DELETE TASK ROUTE - DELETE

@app.route('/tasks/<id>', methods=['DELETE'])

def delete_task(id):
    task = Task.query.session.get(Task, id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

## Ruta de Landing Page 
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message':'Bienvenido a mi primer API con Pthon Flask y MySQL'})

@app.route('/tasks/delete', methods=['DELETE'])
def delete_tasks():
    db.session.query(Tasks).delete()
    db.session.commit()

    return jsonify({"message":"Todo borrado maricon"})

if __name__ == "__main__":
    app.run(debug = True)