from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Datenbank festlegen

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    encounters = db.Column(db.Integer)



class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key=True)
    evaluated = db.Column(db.Boolean, default=False)
