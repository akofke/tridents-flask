from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

from tridents import models
from tridents.views import home, officers

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(officers, url_prefix='officers')

# specify e.g. FLASK_CONFIG=config.DevConfig
app.config.from_object(os.environ['FLASK_CONFIG'])

db = SQLAlchemy(app)

migrate = Migrate(app, db)
