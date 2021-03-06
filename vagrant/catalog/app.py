#!/usr/bin/env python3
from flask import Flask, render_template
from flask import request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client import client
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


engine = create_engine(
    'sqlite:///movie_catalog.db',
    connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

"""
Google Signin
"""


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # If this request does not have `X-Requested-With` header,
    # this could be a CSRF
    if not request.headers.get('X-Requested-With'):
        response = make_response(json.dumps('Forbidden'), 403)
        response.headers['Content-Type'] = 'application/json'
        return response
    # State check
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code

    auth_code = request.data
    # Set path to the Web application
    # client_secret_*.json file you downloaded from the
    CLIENT_SECRET_FILE = 'client_secrets.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE, ['profile', 'email'], auth_code)

    # Check that the access token is valid.
    access_token = credentials.access_token
    baseurl = 'https://www.googleapis.com/oauth2/v1/tokeninfo'
    url = (baseurl + '?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Welcome, " + login_session['username'])
        return redirect(url_for('showCategories'))

    # Get profile info from ID token
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    flash("Welcome, " + login_session['username'])
    return redirect(url_for('showCategories'))


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            if 'access_token' in login_session.keys():
                del login_session['access_token']
            if 'google_id' in login_session.keys():
                del login_session['google_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You are not logged in.")
        return redirect(url_for('showCategories'))


def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(
        email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/login/')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


"""
JSON APis
"""


@app.route('/category/JSON')
def showCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[i.serialize for i in categories])


@app.route('/category/<string:category_name>/JSON')
@app.route('/category/<string:category_name>/items/JSON')
def showCategoryItemsJSON(category_name):
    category = session.query(Category).filter_by(
        name=category_name.upper()).one()
    items = session.query(CategoryItem).filter_by(
        category_id=category.id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])


@app.route('/category/<string:category_name>/item/<int:item_id>/JSON')
def showCategoryItemJSON(category_name, item_id):
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    return jsonify(CategoryItem=item.serialize)


"""
Web APIs
"""


@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).all()
    items = session.query(CategoryItem).order_by(
        CategoryItem.id.desc()).limit(10)
    return render_template('catalog.html', categories=categories, items=items)


@app.route('/category/<string:category_name>/')
@app.route('/category/<string:category_name>/items/')
def showCategoryItems(category_name):
    category = session.query(Category).filter_by(
        name=category_name.upper()).one()
    categories = session.query(Category).all()
    items = session.query(CategoryItem).filter_by(
        category_id=category.id).all()
    return render_template(
        'category.html',
        category_name=category_name.upper(),
        categories=categories, items=items)


@app.route('/category/<string:category_name>/item/<int:item_id>/')
def showCategoryItem(category_name, item_id):
    categories = session.query(Category).all()
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    is_loggedin = 'username' in login_session
    return render_template(
        'categoryitem.html',
        categories=categories,
        item=item,
        is_loggedin=is_loggedin)


@app.route('/category/item/new/', methods=['GET', 'POST'])
def newCategoryItem():
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    if request.method == 'POST':
        item_name = request.form['name']
        item_description = request.form['description']
        category_name = request.form['category_name']
        if item_name is None or item_description is None:
            if category_name == 'Choose...':
                return redirect(url_for('newCategoryItem'))
        category = session.query(Category).filter_by(name=category_name).one()
        newItem = CategoryItem(
            name=item_name,
            description=item_description,
            category_id=category.id,
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("New Item Created!!")
        return redirect(url_for('showCategories'))
    return render_template('categoryitemnew.html', categories=categories)


@app.route(
    '/category/<string:category_name>/item/<int:item_id>/edit/',
    methods=['GET', 'POST'])
def editCategoryItem(category_name, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    item_to_edit = session.query(CategoryItem).filter_by(id=item_id).one()
    if item_to_edit.user_id != login_session['user_id']:
        msg = "You are not authorized to edit this item"
        return """<script>function myFunction() {
            alert('""" + msg + """'); window.location.href = '/category';}
            </script><body onload='myFunction()'>"""
    if request.method == 'POST':
        item_name = request.form['name']
        item_description = request.form['description']
        category_name = request.form['category_name']
        if item_name is None or item_description is None:
            if category_name == 'Choose...':
                flash("You should feel the fields")
                return render_template(
                    'categoryitemedit.html', categories=categories, item=item)
        item_to_edit.name = item_name
        item_to_edit.description = item_description
        session.commit()
        flash("Your item edited!")
        return redirect(url_for('showCategories'))
    else:
        return render_template(
            'categoryitemedit.html', categories=categories, item=item_to_edit)


@app.route(
    '/category/<string:category_name>/item/<int:item_id>/delete/',
    methods=['GET', 'POST'])
def deleteCategoryItem(category_name, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    item_to_delete = session.query(CategoryItem).filter_by(id=item_id).one()
    if item_to_delete.user_id != login_session['user_id']:
        msg = "You are not authorized to delete this item"
        return """<script>function myFunction()
        {alert('""" + msg + """'); window.location.href = '/category';}
        </script><body onload='myFunction()'>"""
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        flash("Item successfully deleted!")
        return redirect(url_for('showCategories'))
    return render_template('categoryitemdelete.html', item=item_to_delete)


if __name__ == '__main__':
    app.secret_key = 'this_is_secrete_key'
    app.debug = True
    app.run(host='localhost', port=5000)
