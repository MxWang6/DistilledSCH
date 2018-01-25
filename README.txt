                                   Car App
                                   
                 an application developed for DistilledSCH's coding test



Project Description
---------------------
This project implements a simple Python Flask API using a Sqlite database.


How to Run and Deploy?
---------------------
Before you run and deploy this application, please make sure you have the following installed on your computer.
  1. Python (>=2.7)
  2. Flask (http://flask.pocoo.org/)
  3. SQLAlchemy (https://www.sqlalchemy.org/)
  4. Flask-SQLAlchemy (http://flask-sqlalchemy.pocoo.org/)
A recommended way to install Flask, SQLAlchemy and Flask-SQLAlchemy is through Python's pip.

Now follow the instructions below to run and deploy it:
  1. Clone this repository onto your local computer.
  2. Open a terminal and go to the root directory of the clone repository. (Mac OS or Linux)
  3. Run and deploy it on Flask server using the following command in terminal.
  
     $ FLASK_APP=carapp.py flask run
     
     If you have start the application successfully, you will see the following message:
     
       * Serving Flask app "carApp"
       * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     
  4. Open a new terminal, run the bash script test_api.sh in the root directory to test the Flask APIs from this application.
     $ ./test_api.sh
     
     Or you can use the following curl commands to test the APIs:
     $ curl http://localhost:5000/car
     $ curl http://localhost:5000/car/id
     $ curl -d '{"year":"2004"}' -H "Content-Type: application/json" -X POST http://localhost:5000/avgprice
     $ curl -d '{"make":"Seat", "model":"Cordoba", "year":"2003", "chassis_id":"12345F"}' -H "Content-Type: application/json" -X POST http://localhost:5000/car

How to Run Unit Tests?
---------------------
  1. Install pytest (http://pytest.org, recommend to install through Python's pip)
  2. Open a terminal and execute all unit tests from this project as below:
     $ pytest -q carapp_test_case.py



