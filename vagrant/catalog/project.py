from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


engine = create_engine('sqlite:///category.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all categorys
@app.route('/')
@app.route('/catalog/')
def showCategories():
    return "Catalog"

@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    return "Make a new category"

@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    return str(category_id) + " Edit Category"

@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    return str(category_id) + " Delete Category"

@app.route('/category/<int:category_id>')
@app.route('/category/<int:category_id>/item/')
def showCategoryItems(category_id):
    return str(category_id) + " List of Category Items"

@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    return str(category_id) + " Create New Category Item"

@app.route('/category/<int:category_id>/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    return "Edit Item >>> Category " + str(category_id) + " " + "Item " + str(item_id)

@app.route('/category/<int:category_id>/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    return "Delete Item >>> Category " + str(category_id) + " " + "Item " + str(item_id)

if __name__ == '__main__':
    app.secret_key = 'this_is_secrete_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)