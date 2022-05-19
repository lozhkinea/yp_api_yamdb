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
    # аргумент self замещается экземпляром объекта Genre
    def to_representation(self, value):
       # data=[]
        # genres_count=Genre.objects.all().count()
        # for i in range(0,genres_count):
        #     # genre = Genre.objects.all()[i]
        #     data.append(get_object_or_404(Genre, id=i))
        #     # data.append(super(GenreSerializer, get_object_or_404(Genre, id=i)).to_representation(value))
        # return data
        return value
    # При записи (в запросе "genre": ["string"])
    def to_internal_value(self, data):
        genre_list=[{slug: get_object_or_404(Genre, slug=slug).name} for slug in data]
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


class TitleListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(required=False)
    # genre = Slug2DictGenre()
    # category = Slug2DictCategory()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
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

    # def validate_year(self, value):
    #     year = dt.date.today().year
    #     if not value <= year:
    #         raise serializers.ValidationError(
    #             "Проверьте год создания произведения!"
    #         )
    #     return value


class TitleSerializer(serializers.ModelSerializer):
    # rating = serializers.SerializerMethodField(required=False)
    # genre = Slug2DictGenre()
    # category = Slug2DictCategory()
    # rating = serializers.SerializerMethodField(required=False)
    # genre = GenreSerializer(many=True)
    # category = CategorySerializer()
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            # "rating",
            "description",
            "genre",
            "category",
        )

    
    # def get_rating(self, obj):
    #     if type(obj.reviews.aggregate(Avg('score'))['score__avg']) == float:
    #         rating = round(obj.reviews.aggregate(Avg("score"))["score__avg"])
    #         return rating

    def validate_year(self, value):
        year = dt.date.today().year
        if not value <= year:
            raise serializers.ValidationError(
                "Проверьте год создания произведения!"
            )
        return value
