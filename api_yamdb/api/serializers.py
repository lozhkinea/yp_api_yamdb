from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
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
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    
    class Meta:
        model = Title
        fields = (
            "name",
            "year",
            'rating',
            "description",
            "genre",
            "category",
        )

    def get_rating(self, obj):
        rating = round(obj.reviews.aggregate(Avg('score'))['score__avg'])
        return rating

    def validate_year(self, value):
        year = dt.date.today().year
        if not value <= year:
            raise serializers.ValidationError('Проверьте год создания произведения!')
        return value 

    def perform_create(self, serializer):
        


