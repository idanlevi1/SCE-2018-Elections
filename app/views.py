# -*- coding: utf-8 -*-

import os

from flask import render_template, flash, redirect, url_for, request, g
from flask import send_from_directory
from flask_login import login_user, logout_user, current_user, login_required

from app import app, login_manager, db
from .models import User, Party
from sqlalchemy import update
from .forms import LoginForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def validateAndAdd(party_name):
    party = Party.query.filter_by(name=party_name).first()
    party.votes = party.votes + 1


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        value = request.form.getlist('party_name')
        if value:
            party_name =request.form['party_name']



            return redirect(url_for('confirm',party_name=party_name))

    g.user = current_user #global user parameter used by flask framwork
    parties = Party.query.all() #this is a demo comment
    return render_template('index.html',
                           title='Home',
                           user=g.user,
                           parties=parties)

@app.route('/confirm/<party_name>', methods=['GET', 'POST'])
@login_required
def confirm(party_name):
    if request.method == 'POST':
        if request.form['action'] == 'conf':
            validateAndAdd(party_name)
            user = User.query.filter_by(id=current_user.id).first()  # imp
            user.voted = True  # imp
            db.session.commit()  # imp
            logout_user()
            return redirect(url_for('index'))
        elif request.form['action'] == 'cancel':
            return redirect(url_for('index'))
    return render_template('confirm.html',
                           title='confirm',
                           party_name=party_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        ## Validate user
        _first_name = request.form['first_name']
        _last_name = request.form['last_name']
        _user_id = request.form['id']
        user = User.query.filter_by(first_name= _first_name, last_name= _last_name, id= _user_id).first()
        if user:
            if user.voted:
                error = u'משתמש זה הצביע כבר בעבר!'
            else:
                login_user(user)  ## built in 'flask login' method that creates a user session
                return redirect(url_for('index'))
        else:  ##validation error
            error = 'User not found!'

    return render_template('login.html', error=error)

## will handle the logout request
@app.route('/logout')
@login_required
def logout():
    logout_user() ## built in 'flask login' method that deletes the user session
    return redirect(url_for('index'))


## secret page that shows the user name
@app.route('/secret', methods=['GET'])
@login_required
def secret():
    return 'This is a secret page. You are logged in as {} {}'.format(current_user.first_name, current_user.last_name)


## will handle the site icon - bonus 2 points for creative new icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
