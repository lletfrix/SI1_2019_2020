#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session, flash
import json
import os
import sys
import random
import pickle
import hashlib
from datetime import date

USERS_FOLDER = 'usuarios'
DATA_FILE = 'datos.dat'
HIST_FILE = 'historial.json'
CATALOGUE_FILE = 'catalogue/catalogo.json'
DATE = '10/10/2019'
ADDR = 'C/Erasmo de Rotterdam'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    films = None

    if request.method == 'POST':
        # Get the search result
        title = request.form.get('title')
        category = request.form.get('category')

        if (not title) and category == 'Ninguno':
            return redirect(url_for('index'))

        with open(os.path.join(app.root_path, CATALOGUE_FILE), encoding="utf-8") as data_file:
            catalogue = json.loads(data_file.read())
            films = catalogue['peliculas']
            if category != 'Ninguno':
                films = list(filter(lambda f: category in f['categorias'], films))
            films = list(filter(lambda f: title.lower() in f['titulo'].lower(), films))

        if not title:
            title = 'Peliculas en la catergoría: '+category
        return render_template('index.html', title='Búsqueda', films=films, search_query=title)

    else:
        # Get the last films
        with open(os.path.join(app.root_path, CATALOGUE_FILE), encoding="utf-8") as data_file:
            catalogue = json.loads(data_file.read())
            films = catalogue['peliculas']
            films = sorted(films, key=(lambda m : m['anio']), reverse=True)[:10]

        return render_template('index.html', title='Home', films=films, search_query=None)


@app.route('/product/<id>', methods=['GET', 'POST'])
def product(id):
    with open(os.path.join(app.root_path, CATALOGUE_FILE), encoding="utf-8") as data_file:
        catalogue = json.loads(data_file.read())
        films = catalogue['peliculas']
        film = list(filter(lambda f: f['id'] == int(id), films))[0]

    if request.method == 'POST':
        if session.get('cart'):
            session['cart'][int(id)] = int(request.form.get('amount'))

            if(int(request.form.get('amount')) == 0):
                session['cart'].pop(int(id), None)
        else:
            session['cart'] = {int(id): int(request.form.get('amount'))}

    return render_template('product.html', title=film['titulo'], film=film)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Getting data from form
        nick = request.form.get('nickname')
        passwd = request.form.get('password')
        mail = request.form.get('mail')
        ccard = request.form.get('ccard')
        addr = request.form.get('address')
        # Validate fields
        if not (nick and passwd and mail and ccard and addr):
            flash('Por favor, rellene todos los campos')
            return render_template('register.html')
        # Check user is available
        users = next(os.walk(os.path.join(app.root_path, USERS_FOLDER)))[1]
        if nick in users:
            flash('Usuario no disponible')
            return render_template('register.html')
        # The username is available, so we store all the data
        # Hashing the password with md5
        md5 = hashlib.md5()
        md5.update(passwd.encode('utf-8'))
        encpwd = md5.hexdigest()
        # Preparing data to be stored
        ####### data = [nick, encpwd, mail, ccard, random.randint(0, 100)]
        data = {'nickname': nick, 'password': encpwd, 'mail': mail, 'ccard': ccard, 'address': addr, 'cash': random.randint(0, 100), 'cart':{}}
        # Writing user data file
        slug_nick = nick.lower()
        os.mkdir(os.path.join(app.root_path, USERS_FOLDER, slug_nick))
        with open(os.path.join(app.root_path, USERS_FOLDER, slug_nick, DATA_FILE), 'wb') as file:
            pickle.dump(data, file)
        # Initializing user history file
        with open(os.path.join(app.root_path, USERS_FOLDER, slug_nick, HIST_FILE), 'w') as file:
            history = {'historial': []}
            json.dump(history, file)

        return redirect(url_for('index'))
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Getting data from form
        nick = request.form.get('nickname')
        passwd = request.form.get('password')
        # Checking user data
        # Validate fields
        if not (nick and passwd):
            flash('Por favor, rellene todos los campos')
            return render_template('login.html')
        # Checking if the user is already registered
        slug_nick = nick.lower()
        users = next(os.walk(os.path.join(app.root_path, USERS_FOLDER)))[1]
        if slug_nick not in users:
            flash('Usuario no registrado')
            return render_template('login.html')
        # Checking the password
        md5 = hashlib.md5()
        md5.update(passwd.encode('utf-8'))
        encpwd = md5.hexdigest()
        with open(os.path.join(app.root_path, USERS_FOLDER, slug_nick, DATA_FILE), 'rb') as file:
            userdata = pickle.load(file)
        if encpwd != userdata['password']:
            flash('Contraseña incorrecta')
            return render_template('login.html')
        # Sessions
        session['nickname'] = userdata['nickname']
        session['mail'] = userdata['mail']
        session['ccard'] = userdata['ccard']
        session['cash'] = userdata['cash']
        session['address'] = userdata['address']
        if session.get('cart'):
            ### DEBUG PLS
            userdata['cart'].update(session['cart'])
            session['cart'].update(userdata['cart'])
        else:
            session['cart'] = userdata['cart']
        #########################################################
        # DEBUG:
        print(session['cash'])
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


def _update_userdata(*argv):
    slug_nick = session['nickname'].lower()
    # Reading userdata
    with open(os.path.join(app.root_path, USERS_FOLDER, slug_nick, DATA_FILE), 'rb') as file:
        userdata = pickle.load(file)
    # Updating
    for arg in argv:
        userdata[arg] = session[arg]
        userdata[arg] = session[arg]
    # Storing updates
    with open(os.path.join(app.root_path, USERS_FOLDER, slug_nick, DATA_FILE), 'wb') as file:
        pickle.dump(userdata, file)


@app.route('/logout', methods=['POST'])
def logout():
    # Storing current cart data into user data file
    _update_userdata('cash', 'cart', 'address')
    # Deleting user data at current session
    session.pop('nickname', None)
    # Deleting cart data in case another user logs in
    session.pop('cart', None)
    return redirect(url_for('index'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    total = 0
    if not session.get('cart'):
        session['cart'] = {}

    if request.method == 'POST':
        prod_id = request.form.get('prod_id')
        session['cart'].pop(int(prod_id), None)

    with open(os.path.join(app.root_path, CATALOGUE_FILE), encoding="utf-8") as data_file:
        catalogue = json.loads(data_file.read())
        films = catalogue['peliculas']
        films = list(filter(lambda f: int(f['id']) in session['cart'].keys(), films))

    for f in films:
        f['amount'] = session['cart'][f['id']]
        total += f['precio']*f['amount']

    total = round(total, 2)

    return render_template('cart.html', films=films, total=total)


@app.route('/purchase', methods=['POST'])
def purchase():
    if not session.get('nickname'):
        return redirect(url_for('login'))

    slug_nick = session['nickname'].lower()
    total = 0
    if not session.get('cart'):
        session['cart'] = {}

    with open(os.path.join(app.root_path, CATALOGUE_FILE), encoding="utf-8") as data_file:
        catalogue = json.loads(data_file.read())
        films = catalogue['peliculas']
        films = list(filter(lambda f: int(f['id']) in session['cart'].keys(), films))

    for f in films:
        f['amount'] = session['cart'][f['id']]
        total += f['precio']*f['amount']

    if session['cash'] >= total:
        session['cash'] -= total
        session['cash'] = round(session['cash'], 2)

        with open(os.path.join(app.root_path, USERS_FOLDER, slug_nick, HIST_FILE), encoding="utf-8") as data_file:
            history = json.loads(data_file.read())

        history['historial'].extend([{'id': f['id'], 'date': date.today().strftime("%d-%b-%Y"), 'address': session['address'], 'price': f['precio'], 'amount': f['amount']} for f in films])

        with open(os.path.join(app.root_path, USERS_FOLDER, slug_nick, HIST_FILE), 'w') as file:
            json.dump(history, file)

        session['cart'] = {}
        _update_userdata('cart', 'cash')
        return redirect(url_for('index'))

    else:
        flash('No dispone de saldo para esta compra.')
        return redirect(url_for('cart'));


@app.route('/history', methods=['GET'])
def history():
    if not session.get('nickname'):
        return redirect(url_for('login'))

    slug_nick = session.get('nickname').lower()

    with open(os.path.join(app.root_path, USERS_FOLDER, slug_nick, HIST_FILE), encoding="utf-8") as data_file:
        history = json.loads(data_file.read())
        history = history['historial']

    with open(os.path.join(app.root_path, CATALOGUE_FILE), encoding="utf-8") as data_file:
        catalogue = json.loads(data_file.read())
        films = catalogue['peliculas']

    for dh in history:
        for df in films:
            if dh['id'] == df['id']:
                dh.update(df)
                break

    return render_template('history.html', history=history)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('nickname'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        if request.form.get('address'):
            session['address'] = request.form.get('address')

        elif request.form.get('cash'):
            try:
                session['cash'] += float(request.form.get('cash'))
                session['cash'] = round(session['cash'], 2)
            except ValueError:
                flash('Por favor, introduzca un valor válido para el saldo')

    return render_template('profile.html')

@app.route('/connectedusers', methods=['GET'])
def connectedusers():
    return str(random.randint(10, 1000))
