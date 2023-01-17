# required packages.
import os

from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# application setup.

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"sqlite:///{os.path.join(basedir, 'menuhub.sqlite')}"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# class models.


class Dish(db.Model):

    __tablename__ = "dishes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Task: #{self.id}, description: {self.description}"

# applications routes.


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        dish = Dish(request.form["name"])
        try:
            db.session.add(dish)
            db.session.commit()
            return redirect('/')
        except:
            return "Houve um erro, ao inserir o Prato"
    else:
        dishes = Dish.query.order_by(Dish.price).all()
        return render_template('index.html', dishes=dishes)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/user/')
def test():
    return render_template('user.html')
