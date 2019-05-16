from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Decoration(db.Model):
    id = db.Column(db.Integer,  nullable=False,  primary_key=True, autoincrement=True)
    country = db.Column(db.String(70), nullable=False, unique=False)
    price = db.Column(db.Integer, nullable=False, unique=False)
    manufacturer = db.Column(db.String(70), nullable=False, unique=False)

    def __init__(self, country, price, manufacturer):
        self.country = country
        self.price = price
        self.manufacturer = manufacturer


class DecorationSchema(ma.Schema):
    class Meta:
        fields = ('country', 'price', 'manufacturer')


decoration_schema = DecorationSchema()
decorations_schema = DecorationSchema(many=True)
db.create_all()


@app.route("/decoration", methods=["POST"])
def add_decoration():
    country = request.json['country']
    price = request.json['price']
    manufacturer = request.json['manufacturer']

    new_decoration = Decoration(country, price, manufacturer)

    db.session.add(new_decoration)
    db.session.commit()

    return decoration_schema.jsonify(new_decoration)


@app.route("/decoration", methods=["GET"])
def get_decoration():
    all_decorations = Decoration.query.all()
    result = decorations_schema.dump(all_decorations)
    return jsonify(result.data)


@app.route("/decoration/<id>", methods=["GET"])
def decoration_detail(id):
    decoration = Decoration.query.get(id)
    return decoration_schema.jsonify(decoration)


@app.route("/decoration/<id>", methods=["PUT"])
def decoration_update(id):
    decoration = Decoration.query.get(id)
    country = request.json['country']
    price = request.json['price']
    manufacturer = request.json['manufacturer']

    decoration.country = country
    decoration.price = price
    decoration.manufacturer = manufacturer

    db.session.commit()
    return decoration_schema.jsonify(decoration)


@app.route("/decoration/<id>", methods=["DELETE"])
def decoration_delete(id):
    decoration = Decoration.query.get(id)
    db.session.delete(decoration)
    db.session.commit()

    return decoration_schema.jsonify(decoration)


if __name__ == '__main__':
    app.run()
