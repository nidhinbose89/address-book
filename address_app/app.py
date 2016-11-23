from flask import Flask
from models import db


def create_app(db_name, testing):
    app = Flask(__name__)
    app.config['MONGOALCHEMY_DATABASE'] = db_name
    app.config['TESTING'] = testing
    from views import register_views
    register_views(app)
    db.init_app(app)
    return app
