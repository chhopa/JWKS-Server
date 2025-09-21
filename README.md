# Project 1 – JWKS Server (Flask)

**Student:** Tanchhopa Limbu Sanba  
**Course:** CSCE 3550  
**Assignment:** Project 1 – Implementing a Basic JWKS Server  

---

# Overview
This project implements a RESTful **JSON Web Key Set (JWKS) server** with JWT issuance.  
It demonstrates:
- RSA key pair generation with unique `kid` values and expiry times  
- JWKS endpoint serving only **non-expired keys**  
- Authentication endpoint issuing JWTs  
- Support for issuing **expired JWTs** when requested via query parameter  
- Proper RESTful API design with correct methods and status codes  

The implementation uses **Python 3, Flask, and PyJWT**, and follows best practices for organization, linting, and testing.

---

# Prerequisites
- Python **3.10+** (tested on 3.13.1)  
- pip (Python package manager)  
- macOS / Linux / Windows  
- Virtual environment (`venv`) recommended  
- [GradeBot](https://github.com/jh125486/CSCE3550/releases) (provided by professor)  

---


# Project Structure
```
jwks-server/
├── app.py
├── key_store.py
├── pytest.ini
├── requirements.txt
├── README.md
├── LICENSE
├── tests/
│   ├── test_auth.py
│   └── test_jwks.py
├── Test Client Screenshot.png
├── Test Suite Screenshot.png
```

---

# Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/chhopa/JWKS-Server.git

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

---

# Running the Server

Start the Flask app:
```bash
python app.py
```

By default, the server runs at http://localhost:8080.

---

## Endpoints
### 1. JWKS
GET `/jwks`

GET `/jwks.json`

GET `/.well-known/jwks.json`
Returns a JWKS with only active (non-expired) RSA keys.

### 2. Auth
POST `/auth`
Returns a valid JWT signed by the active key.

POST `/auth?expired=1`
Returns an expired JWT signed by an expired key.

---

## Testing

Open another terminal. Make sure to activate the virtual environement in this terminal before testing. 

Run tests with coverage:
```bash
pytest
```

Sample output:
```
============================= test session starts ==============================
platform darwin -- Python 3.13.1, pytest-8.4.2, pluggy-1.6.0
configfile: pytest.ini
plugins: cov-7.0.0
collected 3 items                                                              

tests/test_auth.py ..                                                    [ 66%]
tests/test_jwks.py .                                                     [100%]

================================ tests coverage ================================
_______________ coverage: platform darwin, python 3.13.1-final-0 _______________

Name           Stmts   Miss  Cover   Missing
--------------------------------------------
app.py            20      2    90%   16, 40
key_store.py      45      3    93%   48-50
--------------------------------------------
TOTAL             65      5    92%
Required test coverage of 80% reached. Total coverage: 92.31%
============================== 3 passed in 0.43s ===============================
```
---
## Testing the Server Manually

1. **Get a Valid JWT**
```bash
curl -X POST http://127.0.0.1:8080/auth
```
Sample output:
```
{
  "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ij....."
}
```

2. Get an Expired JWT
```bash
curl -X POST "http://127.0.0.1:8080/auth?expired=1"
```
Sample output:
```
{
  "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjVlZmQw......<expired>"
}
```

3. Get Public Keys (JWKS)
```bash
curl -X GET http://127.0.0.1:8080/.well-known/jwks.json
```
Sample output:
```
{
    "keys":[{"alg":"RS256",
    "e":"AQAB",
    "kid":"7e64e4c6-a21e-4bc5-b30f-998488edf59e",
    "kty":"RSA",
    "n":"qQqAzAK2KJ-5jfdKCVozlc-Yx1vidhDZ1yAmbs9mXjvaYLcr........",
    "use":"sig"
    }
  ]
}
```


## Linting

Run pylint:
```bash
pylint app.py key_store.py
```

Expected result:
-------------------------------------------------------------------
Your code has been rated at 10.00/10

---

## GradeBot
In one terminal, start the server:
```bash
python app.py
```

In another terminal, run:
```bash
./gradebot project1
```

Expected rubric result:
```
╭────────────────────────────────────────┬────────┬──────────┬─────────╮
│ RUBRIC ITEM                            │ ERROR? │ POSSIBLE │ AWARDED │
├────────────────────────────────────────┼────────┼──────────┼─────────┤
│ /auth valid JWT authN                  │        │       15 │      15 │
│ /auth?expired=true JWT authN (expired) │        │        5 │       5 │
│ Proper HTTP methods/Status codes       │        │       10 │      10 │
│ Valid JWK found in JWKS                │        │       20 │      20 │
│ Expired JWT is expired                 │        │        5 │       5 │
│ Expired JWK does not exist in JWKS     │        │       10 │      10 │
├────────────────────────────────────────┼────────┼──────────┼─────────┤
│                                        │  TOTAL │       65 │      65 │
╰────────────────────────────────────────┴────────┴──────────┴─────────╯
```











