# Intro
Service to manage discount codes

## Steps to execute
Python version 3.10
### > virtualenv venv
### > source venv/Scripts/activate or ./venv/Scripts/activate
### > pip install -r requirements.txt
### > python main.py

## Test
### > pytest

## Steps to execute using docker container
### > make clean
### > make docker-build
### > make docker-run

To run tests
### > make test

## access end point 
If ran without docker file then : **http://localhost:5000/
If ran with docker container : **http://localhost:8080/

1- POST (**/createCode**) - Create dicsount codes - HTTP Response Code: **200**
```javascript
    HTTP/1.1 200
    Content-Type: application/json

    {
    "noOfDiscountCodes": 10
    }
```

2- GET (**/fetchDiscCode**) - Get dicsount code for an user - HTTP Response Code: **200**
```javascript
    HTTP/1.1 200
    Content-Type: application/json
    Authorization: 'Bearer {token}'
```

RESPONSE:
```javascript
    { 
        'code' : idrtshos, 
        'percentage': 10%
    }
```