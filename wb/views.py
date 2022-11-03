from flask import Blueprint, Flask, redirect, url_for, render_template,request

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/commands')
def commands():
    return render_template("commands.html")

@views.route('/change-log')
def changelog():
    return render_template("change-log.html")