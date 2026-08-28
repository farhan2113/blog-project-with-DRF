# blog-project-with-DRF

This is a blog project that provides APIs for retrieving and creating posts and comments and delete theme or update theme and it provides APIs for sign up and login and refresh access token and logout.

## Requirements

* Python 
* PostgreSql

## Installing

1. copy the repository

```bash
git clone [https://github.com/farhan2113/blog-project-with-DRF.git](https://github.com/farhan2113/blog-project-with-DRF.git)
```

2. create virtual environment 

```bash
python3 -m venv .venv
```

3. Active virtual environment

the activation may differ between operating systems

4. install packages

* Django
```bash
pip install Django
```

* DRF
```bash
pip install djangorestframework
```
* python-dotenv
```bash
pip install python-dotenv
```

* psycopg
```bash
pip install "psycopg[binary]"
```

* djangorestframework-simplejwt
```bash
pip install djangorestframework-simplejwt
```

## setup .env

1. create .env file in blog folder

```bash
touch .env
```

2. add info to .env

```bash
DB_USER=the data base user
DB_NAME=the data base name 
DB_HOST=the data base host
DB_PORT=the data base port
DB_PASSWORD=the data base password
SECRET_KEY=the SECRET_KEY
```
