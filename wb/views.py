from flask import Blueprint, Flask, redirect, url_for, render_template,request,jsonify, session,flash
import requests

views = Blueprint('views', __name__)

#dc_auth = "https://discord.com/api/oauth2/authorize?client_id=1024735385865175180&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect%2F&response_type=code&scope=identify"
dc_auth = "https://discord.com/api/oauth2/authorize?client_id=1024735385865175180&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect%2F&response_type=code&scope=identify%20guilds"
#code M5oroPyTLgWqQFCVXgKjxTX5EESdJI
@views.route('/')
def home():
    return render_template("index.html",oauth2 = dc_auth)
@views.route('/logout')
def logout():
  session.clear()
  flash("Çıkış yapıldı","merror")
  return redirect(url_for('views.home'))
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
    user,guilds = exchange_code(code)
    session['user'] = user
    session["guilds"] = guilds
    return redirect(url_for('views.profile'))
  
@views.route('/me')
def profile():
  # get user info from database - roles etc
  # add column to database in user table for roles and sign in with discord code
  if 'guilds' in session and "user" in session:
    user = session['user']
    user_info = {
      "username": user['username'],
      "fullname": f"{user['username']}#{user['discriminator']}",
      "avatar_path": f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png?size=1024",
      "banner_color": user["banner_color"]
      #banner-avatar_decoration
    }
    guild_session = session["guilds"]
    isSign = True #database control for signup in the server
    for servers in guild_session:
      if servers["name"] == "BTÜ Bilgisayar Mühendisliği" and isSign:
        return render_template("profile.html",user=user_info,guilds=session['guilds'])
    else:
      flash("Sunucuya giriş yapmadınız","m-error")
      return redirect(url_for('views.home'))
  else:
    flash("You need to login first","error")
    return redirect(url_for('views.home'))
  
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
  response1 = requests.get("https://discord.com/api/v6/users/@me/guilds", headers={
    "Authorization": "Bearer %s" % access_token
    })
  print(f"{response1.json()}")
  print(response)
  user = response.json()
  guilds = response1.json()
  print(user)
  return user, guilds