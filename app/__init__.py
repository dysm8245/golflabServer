from flask import Flask
from .api.routes import api
from helpers import JSONEncoder
from config import Config
from models import db as root_db, ma
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.register_blueprint(api)

app.json_encoder = JSONEncoder
app.config.from_object(Config)
root_db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)

