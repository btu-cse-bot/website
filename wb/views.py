from flask import Blueprint, Flask, redirect, url_for, render_template,request,jsonify
import requests

views = Blueprint('views', __name__)

dc_auth = "https://discord.com/api/oauth2/authorize?client_id=1024735385865175180&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect%2F&response_type=code&scope=identify"
#code M5oroPyTLgWqQFCVXgKjxTX5EESdJI
@views.route('/')
def home():

    return render_template("index.html",oauth2 = dc_auth)

@views.route('/commands')
def commands():
    return render_template("commands.html")

@views.route('/change-log')
def changelog():
    return render_template("change-log.html")

@views.route('/oauth2/login/redirect/')
def oauth2_login_redirect():
    code = request.args.get('code')
    print(code)
    user = exchange_code(code)
    return redirect(url_for('views.profile',user=user))
  
@views.route('/me')
def profile():
    user = request.args.get('user')
    return render_template("profile.html",user=user)
def exchange_code(code:str):
  data = {
    "client_id": "1024735385865175180",
    "client_secret": "pJN0iD0-dZb4VhpkSmODh9iknsvEajcl",
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": "http://localhost:8000/oauth2/login/redirect/",
    "scope": "identify"
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
  print(response)
  credentials = response.json()
  print(credentials)
  access_token = credentials['access_token']
  response = requests.get("https://discord.com/api/v6/users/@me", headers={
    "Authorization": "Bearer %s" % access_token
    })
  print(response)
  user = response.json()
  print(user)
  return user