from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DataCreation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  data_directory = db.Column(db.String(256))
  project_path = db.Column(db.String(256))
  # cls_name_list = db.Column(db.String(200),unique=True)
  cls_name_list = db.Column(db.String(200))
  random_img_list = db.Column(db.String(256))
  statusmessage = db.Column(db.String(200))
  train = db.Column(db.Integer)
  test = db.Column(db.Integer)

  def __init__(self, data_directory, project_path, cls_name_list, random_img_list,statusmessage,train,test):
    self.data_directory = data_directory
    self.project_path = project_path
    self.cls_name_list = cls_name_list
    self.random_img_list = random_img_list
    self.statusmessage = statusmessage
    self.train = train
    self.test = test
