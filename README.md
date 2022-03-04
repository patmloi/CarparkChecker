# Installation

```
git clone <url> --depth=1
cd CarparkChecker

python -m venv venv 
venv\Scripts\activate
pip install -r requirements.txt
```

# Usage
## Starting the web application
The directory must be in the project root folder. 

```
uvicorn main:app --reload
```

## Using the APIs 
The API can be acccessed at 127.0.0.1:8000/docs. 

### 1. Registration

```
curl -X 'POST' \
  'http://127.0.0.1:8000/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "REPLACEME",
  "fName": "REPLACEME",
  "lName": "REPLACEME",
  "contactNo": "REPLACEME",
  "password": "REPLACEME"
}'
```

### 2. Login 
```
curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=REPLACEME&password=REPLACEME&scope=&client_id=&client_secret='
```

### 3. View member details
```
curl -X 'GET' \
  'http://localhost:8000/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer REPLACEME_JWTTOKEN '
```

### 4. Get carpark availability 
```
curl -X 'POST' \
  'http://localhost:8000/availability' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer REPLACEME_JWTTOKEN' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'dateTime=REPLACEME'
```

# Testing 
The directory must be in the project root folder. 

```
pytest
```

