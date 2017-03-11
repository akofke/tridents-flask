from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# load config from this file
app.config.from_object(__name__)

# default config
app.config.update(
    SECRET_KEY="development key",
    SQLALCHEMY_DATABASE_URI="postgresql://localhost/tridents_dev",
    AUTH0_CALLBACK_URL="http://localhost:5000/callback"
)

# load additional config from the file at FLASK_CONFIG
app.config.from_envvar('FLASK_CONFIG', silent=False)

db = SQLAlchemy(app)

# import our modules
from tridents import views, models
