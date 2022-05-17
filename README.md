<p align="center"><img src="yatube_api\static\img\logo.png" alt="Yatube API" width="100" height="100"></p>

<h1 align="center">Yatube API</h1>

## Features

This API features the basic operations of the [Yatube]() project.

##### Authentication

Yatube API offers JSON Web Token ([JWT](https://jwt.io))

##### List of operations

| Posts                      | Comments                      | Groups                      | Follow     | Token                |
| -------------------------- | ----------------------------- | --------------------------- | ---------- | -------------------- |
| Getting posts              | Getting comments              | List of groups              | Followings | Get a JWT token      |
| Creating a post            | Adding a comment              | Information about the group | Following  | Update the JWT token |
| Getting a post             | Getting a comment             |                             |            | Check the JWT token  |
| Updating the post          | Updating the comment          |                             |            |                      |
| Partial update of the post | Partial update of the comment |                             |            |                      |
| Deleting a post            | Deleting a comment            |                             |            |                      |

## Installation

Clone the repository and go to it on the command line:

```bash
git clone https://github.com/lozhkinea/api_final_yatube.git
```

```bash
cd api_final_yatube
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

Install dependencies from a file requirements.txt:

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Perform migrations:

```bash
python manage.py migrate
```

Launch a project:

```bash
python manage.py runserver
```

## Usage

You can use [curl](https://curl.se/) to issue requests.

Get a JWT token:

```bash
$ curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"username": "user", "password": "P@ssword"}' \
    http://localhost:8000/api/v1/jwt/create/

. . .

{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MDgwMzQwMywianRpIjoiMmIxYjI1YWI1MTQxNDc4MGE5MWZhMWFlNzQ4MDhmYzgiLCJ1c2VyX2lkIjozfQ.TNdPUCZtDbDDp1fOs0ab1zKmWom1R0AagYTkc2lNWas","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwODAzNDAzLCJqdGkiOiI5OTI0OTExMGRkNjY0Yjc4ODIyMWQxMjIyNDU5MGE1YiIsInVzZXJfaWQiOjN9.KG2PrpJ4elbpmFCU0TpacHmQKjabIIvGEHS4HZwrpKI"}
```

Creating a post:

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwODAzNDAzLCJqdGkiOiI5OTI0OTExMGRkNjY0Yjc4ODIyMWQxMjIyNDU5MGE1YiIsInVzZXJfaWQiOjN9.KG2PrpJ4elbpmFCU0TpacHmQKjabIIvGEHS4HZwrpKI" \
  -d '{"text":"Test post"}' \
  http://localhost:8000/api/v1/posts/

  . . .

  {"id":1,"author":"user","text":"Test post","pub_date":"2022-04-23T12:40:11.522939Z","image":null,"group":null}
```

Getting posts:

```bash
curl \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwODAzNDAzLCJqdGkiOiI5OTI0OTExMGRkNjY0Yjc4ODIyMWQxMjIyNDU5MGE1YiIsInVzZXJfaWQiOjN9.KG2PrpJ4elbpmFCU0TpacHmQKjabIIvGEHS4HZwrpKI" \
  http://localhost:8000/api/v1/posts/

  . . .

  [{"id":1,"author":"user","text":"Test post","pub_date":"2022-04-23T12:40:11.522939Z","image":null,"group":null}]
```
