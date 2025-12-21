# Benkyo Backend
Server for Japanese Language Project

## Setup Instructions

### Prerequisites
- Python 3.11+ (tested with Python 3.13)
- pip
- MongoDB database access
- Google Cloud Storage credentials (for file storage)

### Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Create a `.env` file in the root directory
   - Add the following variables:
   ```
   DB_USERNAME=your_mongodb_username
   DB_PASSWORD=your_mongodb_password
   DB_NAME=your_database_name
   TOKEN_PASS=your_jwt_secret_key
   PORT=5001  # Optional, defaults to 80
   ```

4. Start the server:
```bash
PORT=5001 python application.py
```

The API will be available at `http://localhost:5001`

### Notes
- On macOS, port 5000 is often used by AirPlay Receiver. Use port 5001 or another port for local development.
- The backend requires Python 3.11+ due to compatibility requirements with updated dependencies (numpy, pandas, google-cloud-storage).
- Make sure your MongoDB connection string and credentials are correctly configured in the `.env` file.

## API Requests
#### Test Request
----

* ##### URL

  /test

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `test=[string]`
   `test_int=[integer]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `"Hola"`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{error: "Missing JWT"}`

* **Sample Call:**

  `localhost:5001/test?test=hola&test_int=5`

* **Notes:**

  This endpoint needs an Authorization header with a valid JWT 
----

#### Login
----

* ##### URL

  /login

* **Method:**

  `POST`

*  **URL Params**

   **Required:**

   `username=[string]`
   `password=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```
    {
        "exp": 1583660993,
        "id": "5e5de203d5cee6f169926cc4",
        "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IlZpY3RvcjM0NiIsInR5cGUiOiJhZG1pbiIsInByb2ZpbGUiOiJhY2hpZXZlciIsImlkIjoiNWU1ZGUyMDNkNWNlZTZmMTY5OTI2Y2M0IiwiZXhwIjoxNTgzNjYwOTkzfQ.0_CGLZrMPY2eOIPS-QrwtvmfTCLiXRfqYMb6I3sly88",
        "profile": "achiever",
        "type": "admin",
        "username": "Victor346"
     }
     ```

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{error: "Wrong username or password"}`

* **Sample Call:**

  `localhost:5001/login?password=<password>&username=Victor346`

* **Notes:**
The response contains all the available info from the user (not only the one presented in the example). The jwt parameter returned can be used to authenticate all the following requests.
----

  #### User Creation
----

* ##### URL

  /users

* **Method:**

  `POST`

*  **URL Params**

   **Required:**

   `username=[string]`<br/>
   `password=[string]`<br/>
   `type=["admin", "regular"]`<br/>
   `profile=["seeker", "survivor", "daredevil", "mastermind", "conqueror", "socializer", "achiever"]`<br/>

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```
    {
        "id": "5e5de203d5cee6f169926cc4"
    }
    ```

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{error: "Username already exists"}`

* **Sample Call:**

  `localhost:5001/users?username=Victor346&password=<password>&type=admin&profile=achiever`

* **Notes:**

This endpoint is only for development purposes, the user creation process will change.

