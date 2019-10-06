#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys

@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    movies = None
    if request.method == 'POST':
        # Get the search result
        title = request.form.get('title')
        filter = request.form.get('filter')
        with open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8") as data_file:
            catalogue = json.loads(data_file.read())
            movies = catalogue['peliculas']
            # movies = list(filter(, movies))
        return render_template('index.html', title='Búsqueda', movies=movies)
        
    else:
        # Get the last movies
        with open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8") as data_file:
            catalogue = json.loads(data_file.read())
            movies = catalogue['peliculas']
            # movies = list(filter(, movies))
        return render_template('index.html', title='Home', movies=movies)

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')
