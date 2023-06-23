from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries', methods=['GET', 'POST'])
def bakeries():
    if request.method == 'POST':
        
        data = request.form
        name = data.get('name')
        address = data.get('address')

        bakery = Bakery(name=name, address=address)
        db.session.add(bakery)
        db.session.commit()

        bakery_serialized = bakery.to_dict()

        response = make_response(
            jsonify(bakery_serialized),
            201
        )
    else:
        
        bakeries = Bakery.query.all()
        bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

        response = make_response(
            jsonify(bakeries_serialized),
            200
        )

    return response

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)

    if bakery is None:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)

    if request.method == 'PATCH':
        
        data = request.form
        name = data.get('name')

        bakery.name = name
        db.session.commit()

    bakery_serialized = bakery.to_dict()

    response = make_response(
        jsonify(bakery_serialized),
        200
    )
    return response

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    name = data.get('name')
    price = data.get('price')

    baked_good = BakedGood(name=name, price=price)
    db.session.add(baked_good)
    db.session.commit()

    baked_good_serialized = baked_good.to_dict()

    response = make_response(
        jsonify(baked_good_serialized),
        201
    )
    return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = db.session.get(BakedGood, id)

    if baked_good is None:
        return make_response(jsonify({'error': 'Baked good not found'}), 404)

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({'message': 'Baked good deleted successfully'})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
