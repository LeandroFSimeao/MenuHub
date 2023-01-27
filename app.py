# required packages.
import os

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# application setup.
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize hte Flask object passing the script name with the path
app = Flask(__name__)
Bootstrap(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"sqlite:///{os.path.join(basedir, 'menuhub.sqlite')}"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize the login Manager
login = LoginManager()
login.init_app(app)

# class models


class User:
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __str__(self):
        return f'{self.name}'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

# class Dbs models.


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return f'<User {self.name}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    restaurantId = db.relationship(
        'Restaurant', backref='Dish owner', lazy=True)

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        'restaurant.id'), nullable=False)

    def __repr__(self):
        return f"Task: #{self.id}, description: {self.description}"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# applications routes.
# Declare the aplication default route


@app.route("/index")
@app.route("/home")
@login_required
def index():
    return render_template("index.html")

# Login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        registered_user = User.get(username)
        if registered_user is None:
            return 'Invalid username'
        if registered_user.password != password:
            return 'Invalid password'
        login_user(registered_user)
        return redirect(url_for('index'))
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template('register.html')


# @app.route('/', methods=["POST", "GET"])
# def index():
#     if request.method == "POST":
#         dish = Dish(request.form["name"])
#         try:
#             db.session.add(dish)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return "Houve um erro, ao inserir o Prato"
#     else:
#         dishes = Dish.query.order_by(Dish.price).all()
#         return render_template('index.html', dishes=dishes)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/user/')
def test():
    return render_template('user.html')
