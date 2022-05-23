'''
Скрипт для загрузки данных из CSV-файлов.
'''
from csv import DictReader

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


def load_category():
    Category.objects.all().delete()
    for row in DictReader(
        open('static/data/category.csv', newline='', encoding='utf-8')
    ):
        print(row)
        obj, _ = Category.objects.get_or_create(
            id=row['id'], name=row['name'], slug=row['slug']
        )
        obj.save


def load_comments():
    Comment.objects.all().delete()
    for row in DictReader(
        open('static/data/comments.csv', newline='', encoding='utf-8')
    ):
        print(row)
        obj, _ = Comment.objects.get_or_create(
            id=row['id'],
            review_id=row['review_id'],
            text=row['text'],
            author_id=row['author_id'],
            pub_date=row['pub_date'],
        )
        obj.save


def load_genre():
    Genre.objects.all().delete()
    for row in DictReader(
        open('static/data/genre.csv', newline='', encoding='utf-8')
    ):
        print(row)
        obj, _ = Genre.objects.get_or_create(
            id=row['id'],
            name=row['name'],
            slug=row['slug'],
        )
        obj.save


def load_genre_title():
    for row in DictReader(
        open('static/data/genre_title.csv', newline='', encoding='utf-8')
    ):
        print(row)
        genre, _ = Genre.objects.get_or_create(id=row['genre_id'])
        title, _ = Title.objects.get_or_create(id=row['title_id'])
        title.genre.add(genre)


def load_review():
    Review.objects.all().delete()
    for row in DictReader(
        open('static/data/review.csv', newline='', encoding='utf-8')
    ):
        print(row)
        obj, _ = Review.objects.get_or_create(
            id=row['id'],
            text=row['text'],
            score=row['score'],
            pub_date=row['pub_date'],
            author_id=row['author_id'],
            title_id=row['title_id'],
        )
        obj.save


def load_titles():
    Title.objects.all().delete()
    for row in DictReader(
        open('static/data/titles.csv', newline='', encoding='utf-8')
    ):
        print(row)
        obj, _ = Title.objects.get_or_create(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category_id=row['category_id'],
        )
        obj.save


def load_users():
    User.objects.all().delete()
    for row in DictReader(
        open('static/data/users.csv', newline='', encoding='utf-8')
    ):
        print(row)
        obj, _ = User.objects.get_or_create(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name'],
        )
        obj.save


class Command(BaseCommand):
    help = 'Загрузка данных из csv-файлов'

    def handle(self, *args, **options):
        load_users()
        load_category()
        load_genre()
        load_titles()
        load_genre_title()
        load_review()
        load_comments()
