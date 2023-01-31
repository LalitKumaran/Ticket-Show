from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB_NAME="database.db"

app = Flask(__name__)

db = SQLAlchemy()
#mail=Mail()
DB_NAME = "database.db"
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gughan'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #app.config['MAIL_SERVER'] ='smtp.gmail.com'
    #app.config['MAIL_PORT'] =465
    #app.config['MAIL_USERNAME']='kiruthickkumark.20cse@kongu.edu'
    #app.config['MAIL_PASSWORD']="k16072003k"
    #app.config['MAIL_USE_TLS'] =False
    #app.config['MAIL_USE_SSL']=True
    #mail.init_app(app)
    db.init_app(app)
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    with app.app_context():
        db.create_all()

    return app