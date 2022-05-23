import datetime as dt

from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()

    class Meta:
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать имя пользователя "me"!'
            )
        return value

    def validate(self, data):
        '''
        Возможность получить токен для существующей комбинации username и email
        и обеспечить уникальность username и email
        '''
        if (
            User.objects.filter(email=data['email'])
            .exclude(username=data['username'])
            .exists()
        ):
            raise serializers.ValidationError(
                'Указанный email уже существует!'
            )
        if (
            User.objects.filter(username=data['username'])
            .exclude(email=data['email'])
            .exists()
        ):
            raise serializers.ValidationError(
                'Указанный username уже существует!'
            )
        return data


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    confirmation_code = serializers.CharField(max_length=24, write_only=True)
    token = serializers.CharField(max_length=150, read_only=True)

    class Meta:
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        user = get_object_or_404(
            User,
            username=data['username'],
        )
        token = data['confirmation_code']
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                'Некорректный confirmation_code!'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(required=False)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        rating_agv = obj.reviews.aggregate(Avg('score'))['score__avg']
        if isinstance(rating_agv, float):
            rating = round(rating_agv)
            return rating


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )

    def validate_year(self, value):
        year = dt.date.today().year
        if not value <= year:
            raise serializers.ValidationError(
                'Проверьте год создания произведения!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            title_id = (self.context['view'].kwargs.get('title_id'),)
            author = self.context['request'].user
            if Review.objects.filter(title=title_id, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
