from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

app = Flask(__name__)

# specify e.g. FLASK_CONFIG=config.DevConfig
app.config.from_object(os.environ['FLASK_CONFIG'])

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# import our modules
from tridents import views, models
