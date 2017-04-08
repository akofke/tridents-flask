from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os


app = Flask(__name__)

# specify e.g. FLASK_CONFIG=config.DevConfig
app.config.from_object(os.environ['FLASK_CONFIG'])

db = SQLAlchemy(app)
from tridents import models

from .views.home import home
from .views.officers import officers
app.register_blueprint(home)
app.register_blueprint(officers, url_prefix='/officers')


migrate = Migrate(app, db)

