import os
import carapp
import unittest
import tempfile
from flask import json

class carappTestCase(unittest.TestCase):

    def setUp(self):
        self.db_file, self.db_name = tempfile.mkstemp()
        carapp.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + self.db_name
        carapp.app.testing = True
        self.app = carapp.app.test_client()
        with carapp.app.app_context():
            carapp.db.create_all()

    def tearDown(self):
        os.close(self.db_file)
        os.unlink(self.db_name)

    # Unit test case to test creating a car record
    def test_create_car_record(self):
        data = dict(make = 'Nissan',
	                model = 'Micra',
	                year = 2009,
	                chassis_id = '12345F',
                    price = 4100.23)
        response = self.app.post('/car',
		                         data=json.dumps(data),
		                         content_type='application/json')
        assert response.status_code == 201

        json_data = json.loads(response.get_data(as_text=True))
        assert json_data.get('id') == 1

    # Unit test case to test getting a car record
    def test_get_a_car(self):
        # setup a car record
        data = dict(make = 'Nissan',
	                model = 'Micra',
	                year = 2009,
	                chassis_id = '12345F',
                    price = 4100.23)
        response = self.app.post('/car',
                                 data=json.dumps(data),
                                 content_type='application/json')
        json_data = json.loads(response.get_data(as_text=True))
        car_id = json_data.get('id')

        # actual test
        response = self.app.get('/car/' + str(car_id))
        assert response.status_code == 200

        json_data = json.loads(response.get_data(as_text=True))
        assert json_data.get('make') == 'Nissan'
        assert json_data.get('model') == 'Micra'
        assert json_data.get('year') == 2009
        assert json_data.get('id') == 1
        assert json_data.get('price') == 4100.23
        assert json_data.get('last_updated') is not None
        # ensure the chassis id is not sent in the response
        assert json_data.get('chassis_id') is None

    # Unit test case to test getting a car that doesn't exist
    def test_get_a_car_not_exist(self):
        response = self.app.get('/car/23')
        assert response.status_code == 404

    # Unit test case to test getting all cars
    def test_get_all_cars(self):
        # setup up two car records
        data = dict(make='Nissan',
                    model='Micra',
                    year=2009,
                    chassis_id='12345F',
                    price=4100.23)
        self.app.post('/car',
                     data=json.dumps(data),
                     content_type='application/json')

        data = dict(make='Audi',
                    model='A4',
                    year=2011,
                    chassis_id='1234AF',
                    price=6000.32)
        self.app.post('/car',
                      data=json.dumps(data),
                      content_type='application/json')

        # actual test
        response = self.app.get('/car')
        assert response.status_code == 200

        json_data = json.loads(response.get_data(as_text=True))
        cars = json_data.get('cars')
        assert len(cars) == 2

        car_1 = cars[0]
        assert car_1.get('make') == 'Nissan'
        assert car_1.get('model') == 'Micra'
        assert car_1.get('year') == 2009
        assert car_1.get('id') == 1
        assert car_1.get('price') == 4100.23
        assert car_1.get('last_updated') is not None
        # ensure the chassis id is not sent in the response
        assert car_1.get('chassis_id') is None

        car_2 = cars[1]
        assert car_2.get('make') == 'Audi'
        assert car_2.get('model') == 'A4'
        assert car_2.get('year') == 2011
        assert car_2.get('id') == 2
        assert car_2.get('price') == 6000.32
        assert car_2.get('last_updated') is not None
        # ensure the chassis id is not sent in the response
        assert car_2.get('chassis_id') is None

    # Unit test case to test getting the average price
    def test_get_average_price(self):
        # setup up two car records
        data = dict(make='Nissan',
                    model='Micra',
                    year=2009,
                    chassis_id='12345F',
                    price=4100.23)
        self.app.post('/car',
                      data=json.dumps(data),
                      content_type='application/json')

        data = dict(make='Nissan',
                    model='Micra',
                    year=2011,
                    chassis_id='1234AF',
                    price=6000.32)
        self.app.post('/car',
                      data=json.dumps(data),
                      content_type='application/json')

        # actual test
        data = dict(make='Nissan',
                    model='Micra')
        response = self.app.post('/avgprice',
                                 data = json.dumps(data),
                                 content_type = 'application/json')
        assert response.status_code == 200

        json_data = json.loads(response.get_data(as_text=True))
        assert json_data.get('avg_price') == 5050.275
