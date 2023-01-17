# required packages.
import os
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# application setup.

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
Bootstrap(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"sqlite:///{os.path.join(basedir, 'menuhub.sqlite')}"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

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
        return f"Dish: #{self.id}, name: {self.name}"

# applications routes.


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        dish = Dish(name=request.form['name'].upper(),
                    category=request.form['category'],
                    price=float(request.form['price']))
        try:
            db.session.add(dish)
            db.session.commit()
            return redirect('/')
        except:
            return "Houve um erro, ao inserir o Prato"
    else:
        dishes = Dish.query.order_by(Dish.price).all()
        return render_template('index.html', dishes=dishes)

@app.route('/delete/<int:id>')
def delete(id):
    """delete a dish"""
    dish = Dish.query.get_or_404(id)
    try:
        db.session.delete(dish)
        db.session.commit()
        return redirect('/')
    except:
        return "Houve um erro, ao inserir o prato"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """update route"""
    dish = Dish.query.get_or_404(id)
    if request.method == 'POST':
        dish.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Houve um erro, ao atualizar o prato"
    else:
        return render_template('update.html', dish=dish)