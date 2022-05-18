import datetime as dt

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Genre, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError('Cannot create user "me"')
        return data


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "confirmation_code",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )


class Slug2DictGenre(serializers.Field):
    # При чтении
    def to_representation(self, value):
        return value
    # При записи (в запросе "genre": ["string"])
    def to_internal_value(self, data):
        genre_list=[{slug: get_object_or_404(Genre, slug=slug).name} for slug in data]
        # genre={}
        # genre_list=[]
        # for i in data:
        #     name = get_object_or_404(Genre, slug=i).name
        #     genre = {'name':name, 'slug':i}
        #     genre_list.append(genre)
        return genre_list


class Slug2DictCategory(serializers.Field):
    # При чтении
    def to_representation(self, value):
        return value
    # При записи (в запросе "category": "string")
    def to_internal_value(self, data):
        name = get_object_or_404(Category, slug=data).name
        category = {'name':name, 'slug':data}
        return category


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(required=False)
    genre = Slug2DictGenre()
    category = Slug2DictCategory()
    rating = serializers.SerializerMethodField(required=False)
    # genre = GenreSerializer(many=True)
    # category = CategorySerializer()
    # genre = serializers.SlugRelatedField(
    #     queryset=Genre.objects.all(), slug_field="slug", many=True
    # )
    # category = serializers.SlugRelatedField(
    #     queryset=Category.objects.all(), slug_field="slug"
    # )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    
    def get_rating(self, obj):
        if type(obj.reviews.aggregate(Avg('score'))['score__avg']) == float:
            rating = round(obj.reviews.aggregate(Avg("score"))["score__avg"])
            return rating

    def validate_year(self, value):
        year = dt.date.today().year
        if not value <= year:
            raise serializers.ValidationError(
                "Проверьте год создания произведения!"
            )
        return value

    # Переопределите это для поддержки сериализации для операций чтения
    # instance - набор записей для сериализации
    # у каждого поля сериалайзера есть собственный метод to_representation.
    # Задача метода — представить извлечённые из записи данные в определённом виде
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['genre'] = GenreSerializer(many=True)
    #     representation['category'] = CategorySerializer()
    #     return representation
