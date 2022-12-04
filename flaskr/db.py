import sqlite3

import click
from flask import current_app, g

db = current_app.db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Email(db.Model):
    uid = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    topic = db.Column(db.String(255), nullable=False, default='')
    mail_from = db.Column(db.String(100), nullable=False)
    mail_to = db.Column(db.String(100), nullable=False)
    sent = db.Column(db.DateTime, nullable=False)
    read = db.Column(db.DateTime, nullable=True)
    is_sent = db.Column(db.Integer, nullable=False)
    readcount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Email %r>' % self.uuid

class Constant(db.Model):
    name = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)