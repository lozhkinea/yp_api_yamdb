from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg

import datetime as dt

from users.models import User
from reviews.models import Title, Review, Category, Genre


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


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(required=False)
    # genre = GenreSerializer(many=True)
    # category = CategorySerializer()
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    
    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            'rating',
            "description",
            "genre",
            "category",
        )

    def get_rating(self, obj):
        if type(obj.reviews.aggregate(Avg('score'))['score__avg']) == float:
            rating = round(obj.reviews.aggregate(Avg('score'))['score__avg'])
            return rating
    
    def validate_year(self, value):
        year = dt.date.today().year
        if not value <= year:
            raise serializers.ValidationError('Проверьте год создания произведения!')
        return value 

    # Переопределите это для поддержки сериализации для операций чтения
    def to_representation(self, instance):
        data = super(TitleSerializer, self).to_representation(instance)
        return data
    # def get_genre(self, obj):
    #     genre=[]
    #     slugs = self.obj.get('genre')
    #     for slug in slugs:
    #         genre.append(Genre.objects.get(slug=slug))
    #     return genre
    # def validate(self, data):
    #     # получим список жанров
    #     genre_list=[]
    #     # из словаря запроса получим жанры по ключу genre
    #     # возвращается str!!!!!
    #     slugs = self.context['request'].data.get('genre')
    #     for slug in slugs:
    #         genre_list.append(Genre.objects.get(slug=slug))
    #     # сохраним жанры в словарь
    #     data['genre']=genre_list
    #     return data

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
