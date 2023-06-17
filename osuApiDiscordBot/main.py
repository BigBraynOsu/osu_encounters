from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from views import bp


# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.register_blueprint(bp)
# initialize the app with the extension
db.init_app(app)


with app.app_context():
    db.create_all()

app.run(debug=True)