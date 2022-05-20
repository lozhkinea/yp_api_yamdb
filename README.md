# Yamdb, API-project

## Description

YaMDb project collects user feedback on the composition (books, movies, music)

## Technologies

- Python 3;
- Django REST Framework;
- SQLlite.

## Installation

Clone the repository and go to it on the command line:

```python
git clone ...
```

```python
cd api_yamdb
```

Create and activate a virtual environment:

```python
python -m venv venv
```

```python
source venv/bin/activate
```

Install dependencies from a file requirements.txt:

```python
python -m pip install --upgrade pip
```

```python
pip install -r requirements.txt
```

Perform migrations:

```python
python manage.py migrate
```

Launch a project:

```python
python manage.py runserver
```

## API request examples:

### Request method: GET

- Request URL: http://127.0.0.1:8000/api/v1/categories/

- Response sample:

```python
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

### Request method: POST

- Request URL: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

- Request sample:

```python
{
  "text": "string",
  "score": 1
}
```

- Response sample:

```python
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Request method: PATCH

- Request URL: http://127.0.0.1:8000/api/v1/users/{username}/

- Request sample:

```python
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

- Response sample:

```python
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

## The authors:

- [Эдуард Ложкин](https://github.com/lozhkinea)
- [Татьяна Ким](https://github.com/TatianaVKim)
- [Мария Борщева](https://github.com/Mashabor)
