from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from project_io import project_main
from data_io import data_extraction, pre_processing_main
# from training_io import parameters, training_main
import os
from model.data_creation import DataCreation
from model.project_creation import Project

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Project Schema
class DataSchema(ma.Schema):
  class Meta:
    fields = ('id', 'data_directory', 'project_path', 'cls_name_list', 'random_img_list','statusmessage','train','test')

# Init schema
data_schema = DataSchema()
datas_schema = DataSchema()

# Project Class/Model

# Project Schema
class ProjectSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'task', 'library','project_path','library_version')

# Init schema
project_schema = ProjectSchema()
projects_schema = ProjectSchema()

# Create a Project
@app.route('/project', methods=['POST'])
def create_project():
  name = request.json['name']
  description = request.json['description']
  task = request.json['task']
  library = request.json['library']

  exits_task = db.session.query(Project.id).filter_by(task=task).scalar() is not None
  if exits_task:
    return {'message': "An project with task name '{}' already exists.".format(task)}, 400
    
  project_path, libr, library_version = project_main(name, task, library)

  new_project = Project(name, description, task, library, project_path, library_version)

  db.session.add(new_project)
  db.session.commit()

  return project_schema.jsonify(new_project)

# Get All Projects
@app.route('/project', methods=['GET'])
def get_projects():
  all_projects = Project.query.all()
  result = projects_schema.dump(all_projects,many=True)
  return jsonify(result)

# Get Single Project
@app.route('/project/<id>', methods=['GET'])
def get_project(id):
  project = Project.query.get(id)
  return project_schema.jsonify(project)

# Update a Project
@app.route('/project/<id>', methods=['PUT'])
def update_project(id):
  project = Project.query.get(id)

  name = request.json['name']
  description = request.json['description']
  task = request.json['task']
  library = request.json['library']

  project.name = name
  project.description = description
  project.task = task
  project.library = library

  db.session.commit()

  return project_schema.jsonify(project)

# Delete Project
@app.route('/project/<id>', methods=['DELETE'])
def delete_project(id):
  project = Project.query.get(id)
  db.session.delete(project)
  db.session.commit()

  return project_schema.jsonify(project)

# Create a Project and dataextract
@app.route('/extractd/<id>', methods=['POST'])
def dataextract(id):
  exits_project = db.session.query(Project.id).filter_by(id=id).scalar() is not None
  if not exits_project:
    return {'message': "An project with id '{}' doesnt exists.".format(id)}, 400
  project = Project.query.get(id)
  data_directory = request.json['data_directory']
  train = request.json['train']
  test = request.json['test']

  exits_task = db.session.query(DataCreation.id).filter_by(id=id).scalar() is not None
  if exits_task:
    return {'message': "An Dataextract with task name '{}' already exists.".format(id)}, 400

  cls_name_list, random_img_list, statusmessage= data_extraction(data_directory, project.project_path)
  pre_processing_main(project.library, project.project_path, train)
  project_path = project.project_path
  cls_name_list = ','.join(map(str, cls_name_list))
  random_img_list = ','.join(map(str, random_img_list))

  new_project = DataCreation(data_directory, project_path, cls_name_list, random_img_list,statusmessage,train,test)

  db.session.add(new_project)
  db.session.commit()

  return project_schema.jsonify(new_project)

# Run Server
if __name__ == '__main__':
  app.run(host="0.0.0.0",debug=True)