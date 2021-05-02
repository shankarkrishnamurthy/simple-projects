Author: Shankar, K
Date: 2021

Description:
    1. python app.py
    2. localhost:3142/login
        -> enter login/passwd
        -> returns token
    3. curl -X GET -H "Accept: application/json" -H "x-access-token: <token>" localhost:3142/
