from flask import Flask

app = Flask(__name__)
DBNAME = 'database.db'
def create_app():
    #app.config['SECRET_KEY'] = 'secret'
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.secret_key = "secret"
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DBNAME
    return app
