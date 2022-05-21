import datetime as dt

from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


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


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['title']

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
        fields = '__all__'
        read_only_fields = ['review']


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()

    class Meta:
        fields = (
            'username',
            'email',
        )

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Нельзя создать пользователя "me"!'
            )
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

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        if created:
            user.is_active = False
            user.save()
        code = default_token_generator.make_token(user)
        subject = 'Код подтверждения регистрации на YaMDb'
        message = f'Привет {user}, твой код подтверждения: {code}'
        user.email_user(subject, message)
        return user


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    confirmation_code = serializers.CharField(max_length=24, write_only=True)

    class Meta:
        fields = ('username', 'confirmation_code', 'token')

    def create(self, validated_data):
        return get_object_or_404(
            User,
            username=validated_data['username'],
        )

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

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
        if type(obj.reviews.aggregate(Avg('score'))['score__avg']) == float:
            rating = round(obj.reviews.aggregate(Avg('score'))['score__avg'])
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
