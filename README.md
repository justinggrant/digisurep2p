# digisureP2P

a basic P2P payment system

## Deployment

The Digisure P2P payment system was built using Django Rest Framework.  Before running the application, you will need to install the following:

### Prerequisites

* Python 3.10 or later (3.11 preferred) - https://www.python.org/downloads/
* Postgres - https://www.postgresql.org/download/

### Setup & Installation

1. Create a virtual environment for the project

   ```
   python3 -m venv <virtual env path>v
   ```
2. Activate the virtual environment

   ```
   source <virtual env path>/bin/activate
   ```
3. Install the required packages

   ```
   pip install -r requirements/local.txt
   ```
4. Create the database

   ```
   createdb --username=postgres digisurep2p
   ```
5. Add a .env file to the root of the project with the following:

   ```
    DJANGO_ENVIRONMENT=local

    # local database
    APP_DB_NAME=digisurep2p
    APP_DB_USER=postgres
    APP_DB_PASSWORD=<password for local postgres>
    APP_DB_HOST=127.0.0.1
    APP_DB_PORT=5432
    ```
6. Run the database migrations to set up the tables.

   ```
   python manage.py migrate
   ```

7. Start the server

   ```
    python manage.py runserver 0.0.0.0:8000
   ```

## Using the API

Once the server is running, you can access view the API documentation at http://localhost:8000/api/docs/.  This interface can also be used to test the API if desired.

### Registering a User

To register a user, you will need to make a POST request to the /api/register/ endpoint.  The request should include the following fields:

```
{
  "email": "user@example.com",
  "password": "string"
}
```

Registration will return a 201 response if successful.  If the email address is already in use, a 400 response will be returned.  It will also return a token for the user, which is needed for the authenticated APIs.

### Getting a Token

In addition to getting a token by registration, registered users can get a token by `POST /user/login/` route with their email and password.  This will return a token that can be used for authenticated APIs.

### Using a token to access authenticated APIs

To access the authenticated APIs, you will need to include the token in the Authorization header of the request.  The header should be in the following format:

```
curl -X 'GET' 'http://localhost:8000/<endpoint>/' \
  -H 'accept: */*' \
  -H 'Authorization: Token <generated token>'
```

In addition, the API docs support using the token with the "Authorize" button.  Clicking this button will open a dialog where you can enter the token.  Once entered, the token will be included in all requests made through the API docs.  As noted on the dialog, add the prefic 'Token' to the token value.

## Understanding and Navigating the Code

The digisure P2P payment system is built using Django Rest Framework.  There are two models used for this system: User and Transaction.

### User Model

 The User model is based on the standard Django user model. The model and related code can be found in `./digisurep2p/users/models.py`.  In addition to the models.py file which details the model, the key logic for users can be found in the following files:
 * `./digisurep2p/users/api/serializers.py` - this file contains the serializers for the User model.  The serializers are used to validate input and convert the model to/from JSON.
 * `./digisurep2p/users/api/views.py` - this file contains the views for the User model.  The views are used to handle the API requests and return the appropriate responses.

### Transaction Model
 The Transaction model is a custom model.  The model and related files can be found in `./digisurep2p/transactions/`.  The model includes the following fields:
* sender - the user sending the payment
* receiver - the user receiving the payment
* amount - the amount of the payment
* timestamp - the date/time the payment was sent

In addition to the model, the key logic for transactions can be found in the following files:
 * `./digisurep2p/transactions/api/serializers.py` - this file contains the serializers for the Transaction model.  The serializers are used to validate input and convert the model to/from JSON.
 * `./digisurep2p/transactions/api/views.py` - this file contains the views for the Transaction model.  The views are used to handle the API requests and return the appropriate responses.

### Other Key Files & Folders

* requirements - this folder contains the requirements files for the project.  The requirements files are used to install the required packages for the project.  For this project, there is a local.txt and a base.txt.  The base.txt is used for common installs across environments.  The local.txt is used for local development.  If other environments are added, they should have their own requirements file.
* config - this folder contains the configuration files for the project.  The settings.py file contains the settings for the project.  The urls.py file contains the urls for the project.


## Next High Priority Items

- email & communications
- UI
- testing
- async
- sending payments out of network
- add parameters to API for searching/filtering
