# api_wine

### Wine API

## Table of contents

-   [General info](#general-info)
-   [Features](#features)
-   [API Endpoints](#api-endpoints)
-   [Technologies](#technologies)
-   [Setup](#setup)

## General info<a name="general-info"></a>

Wine API is a REST API built with Flask & SQLAlchemy to operate CRUD operation on the database. The different routes are described below in the API Endpoint section.

## Features<a name="features"></a>

### User features

-   Allow user to create an account
-   Allow user to login
-   Allow user to disconnect
-   Allow user to save information in the database
-   Allow the user to update or delete their information (name, password, address, etc…)
-   Allow user to delete their account
-   Allow user to reset their password through Email
-   Allow user to upload a profile picture
-   Allow user to save setting in the database
-   Allow user to update or delete their settings (theme, default currency)

## API Endpoints<a name="api-endpoints"></a>

After running the server, consult Documentation at :

> http://127.0.0.1:5000/

-   Product
    -   Return JSON with all products
    -   Return JSON selected product

Database schema:

![DB Screenshot](https://github.com/antoineratat/github_docs/blob/main/wine_api/1.png?raw=true)

## Technologies<a name="technologies"></a>

Project is created with:

- astroid v2.6.2
- click v8.0.1
- Flask v2.0.1
- Flask-Cors v3.0.10
- Flask-SQLAlchemy v2.5.1
- greenlet v1.1.0
- isort v5.9.2
- itsdangerous v2.0.1
- Jinja2 v3.0.1
- lazy-object-proxy v1.6.0
- MarkupSafe v2.0.1
- mccabe v0.6.1
- pylint v2.9.3
- six v1.16.0
- SQLAlchemy v1.4.21
- toml v0.10.2
- Werkzeug v2.0.1
- wrapt v1.12.1

## Setup<a name="setup"></a>

### Import project

```
$ git clone https://github.com/antoineratat/api_wine.git
$ py -3 -m venv venv
$ venv\Script\Activate (Unix: source env/bin/activate)
$ cd wine_api
$ pip install -r requirements.txt
```

### Create Environnement Variable

```
$ SECRET_KEY = '12345678912345678912345678912312'
$ DATABASE_URL = 'postgres://myurl:port/dbname'
```

### Initialize Database

```
$ venv\Script\Activate
$ python
$ from run import db
$ db.create_all()
$ exit()
```

### Run project

```
$ python run.py
```
