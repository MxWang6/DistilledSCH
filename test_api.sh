#!/bin/bash
# Test the API to return a car record using a specified car id.
echo "Test returning a car record using a specified car id: "
curl http://localhost:5000/car/1

# Test the API to return records for all cars.
echo "Test returning records for all cars: "
curl http://localhost:5000/car

# Test the API to return an average price for specified cars.
echo "Test returning an average price for specified cars: "
curl -d '{"make":"Seat", "model":"Cordoba", "year":"2003"}' -H "Content-Type: application/json" -X POST http://localhost:5000/avgprice

# Test the API to create a new car record.
echo "Test creating a new car record: "
curl -d '{"make":"Seat", "model":"Cordoba", "year":"2003", "chassis_id":"12345F"}' -H "Content-Type: application/json" -X POST http://localhost:5000/car
