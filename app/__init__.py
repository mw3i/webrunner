## python standard library
import json, random, datetime, os, importlib, sys

## external
from flask import Flask, redirect, url_for, request, render_template, make_response, jsonify, send_from_directory, Blueprint, session
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet # <-- for temporary encrypted message

## internal
import config

## Init environment
if os.path.isdir('./data/') == False: os.mkdir('./data/')
if os.path.isdir('./data/_consentforms_') == False: os.mkdir('./data/_consentforms_')
if os.path.isdir('./data/_exitsurveys_') == False: os.mkdir('./data/_exitsurveys_')

TEMP_KEY = Fernet.generate_key() # <-- use this to temporarily make a 
encryptor = Fernet(TEMP_KEY)


## init app
app = Flask(
    __name__,
    static_folder = 'static/',
    template_folder = 'templates/',
)

# app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = config.path_to_participants_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # <-- i keep getting warned to do this so i included it here; not sure what it does
app.config['SECRET_KEY'] = config.SECRET_KEY

login = LoginManager(app)

## init database
db = SQLAlchemy(app)

from app import routes, models
db.create_all()

## create data folders for all experiments
for exp in config.experiments:
    if os.path.isdir(os.path.join('data/experiments',config.experiments[exp]['data'])) == False:
        os.mkdir(os.path.join('data/experiments',config.experiments[exp]['data']))

