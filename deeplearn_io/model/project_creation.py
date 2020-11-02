from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  description = db.Column(db.String(200))
  task = db.Column(db.String(200),unique=True)
  library = db.Column(db.String(200))
  project_path = db.Column(db.String(256))
  # libraryr = db.Column(db.String(200))
  library_version = db.Column(db.String(200))

  def __init__(self, name, description, task, library,project_path,library_version):
    self.name = name
    self.description = description
    self.task = task
    self.library = library
    self.project_path = project_path
    self.library_version = library_version
