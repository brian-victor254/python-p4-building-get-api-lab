from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# GET /bakeries: Returns a list of all bakeries
@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()  # Get all bakeries
    bakery_list = [bakery.to_dict() for bakery in bakeries]  # Convert to list of dicts
    return make_response(jsonify(bakery_list), 200)

# GET /bakeries/<int:id>: Returns a single bakery with its baked goods
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)  # Get bakery by id, 404 if not found
    bakery_data = bakery.to_dict(nested=True)  # Convert to dict with baked goods nested
    return make_response(jsonify(bakery_data), 200)

# GET /baked_goods/by_price: Returns baked goods sorted by price in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()  # Sorted by price
    baked_goods_list = [bg.to_dict() for bg in baked_goods]  # Convert to list of dicts
    return make_response(jsonify(baked_goods_list), 200)

# GET /baked_goods/most_expensive: Returns the most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()  # Get most expensive
    if most_expensive:
        return make_response(jsonify(most_expensive.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "No baked goods found"}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
