#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')
