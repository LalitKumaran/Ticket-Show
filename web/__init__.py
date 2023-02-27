from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB_NAME="database.db"

db = SQLAlchemy()

DB_NAME = "database.db"
def createapp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ticketshow'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    with app.app_context():
        db.create_all()
    return app