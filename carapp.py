from flask import Flask,json,request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/mx/Documents/DistilledSCH/database.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Car(db.Model):
    __tablename__ = 'car'
    make = db.Column(db.TEXT, nullable = False)
    model = db.Column(db.TEXT, nullable = False)
    year = db.Column(db.Integer, nullable = True)
    chassis_id = db.Column(db.TEXT, nullable = False)
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.TEXT, nullable = False)
    price = db.Column(db.Float, nullable = True)


@app.route('/car',methods = ['GET'])
def get_all_cars():
    all_cars = Car.query.all()
    car_list = []
    for car in all_cars:
       car_dict = dict(make = car.make,
                   model = car.model,
                   year = car.year,
                   id = car.id,
                   last_updated = car.last_updated,
                   price = car.price)
       car_list.append(car_dict)
    return jsonify(cars=car_list)


@app.route('/car/<int:id>',methods=['GET'])
def get_car_by_id(id):
    car = Car.query.filter_by(id=id).first();
    if not car:
        abort(404)
    car_dict = dict(make = car.make,
                    model = car.model,
                    year = car.year,
                    id = car.id,
                    last_updated = car.last_updated,
                    price = car.price)
    return jsonify(car_dict)


@app.route('/avgprice',methods=['POST'])
def get_average_price():
    json_data = request.get_json(force=True)
    cars = Car.query.filter_by(**json_data).all()
    car_num = len(cars)
    if car_num == 0:
        return jsonify(avg_price = 0)

    total_price = 0.0
    for car in cars:
       if car.price:
           total_price += car.price
    avg_price = total_price / car_num
    return jsonify(avg_price = avg_price)


@app.route('/car',methods=['POST'])
def create_new_car_record():
    json_data = request.get_json(force=True)
    new_car = Car(make = json_data.get('make'),
                    model = json_data.get('model'),
                    year = json_data.get('year'),
                    price = json_data.get('price'),
                    chassis_id = json_data.get('chassis_id'),
                    last_updated = str(datetime.now()))
    db.session.add(new_car)
    db.session.commit()
    return jsonify(id=new_car.id), 201

